# -*- coding: utf-8 -*-
import operator
from flask import request, session, current_app as app
from fractions import Fraction
from datetime import datetime
from pytz import timezone
from wtforms import Form, DecimalField, StringField, IntegerField
from wtforms.validators import InputRequired, ValidationError, StopValidation, NumberRange
from wtforms_json import init; init()
from dateutil import parser

from openprocurement.auction.esco.utils import to_decimal
from openprocurement.auction.esco.constants import DAYS_IN_YEAR, MAX_CONTRACT_DURATION
from openprocurement.auction.utils import prepare_extra_journal_fields
from esculator import npv

def append_error_to_form(form, message):
    errors = form.errors.get('form', [])
    errors.append(message)
    form.errors['form'] = errors

def validate_bidder_id_on_bidding(form, field):
    stage_id = form.document['current_stage']
    if field.data != form.document['stages'][stage_id]['bidder_id']:
        form[field.name].errors.append(u'Not valid bidder')
        raise StopValidation(u'Not valid bidder')


def validate_value(form, field):
    data = Fraction(field.data)
    if data <= Fraction('0') and data != -1:
        form[field.name].errors.append(u'To low value')
        raise ValidationError(u'To low value')


def validate_yearly_payments_percentage(form, field):
    data = field.data
    yearly_payments_percentage_range = app.config['auction'].auction_document['yearlyPaymentsPercentageRange']
    if not (Fraction(str(yearly_payments_percentage_range)) <= Fraction(data) <= Fraction(1)):
        message = u'Percentage value must be between {} and 100'.format(yearly_payments_percentage_range*100)
        raise ValidationError(message)


def validate_contract_duration(form, field):
    if field.data and form.contractDuration.data:
        if (Fraction(field.data, DAYS_IN_YEAR) + form.contractDuration.data) > MAX_CONTRACT_DURATION:
            raise ValidationError(u'Maximun contract duration is 15 years')


def validate_bid_change_on_bidding(form, amount_npv):
    """
    Bid must be higher then previous bidder bid amount minus minimalStep amount
    """
    stage_id = form.document['current_stage']
    if form.auction.features:
        max_bid = reduce(operator.mul, map(Fraction, [
            form.document['stages'][stage_id]['amount_features'],
            form.auction.bidders_coeficient[form.data['bidder_id']]
        ]))
        if amount_npv < sum(
                max_bid,
                Fraction(form.document['minimalStepPercentage'])):
            message = u'Amount NPV: Too low value'
            append_error_to_form(form, message)
            raise ValidationError(message)
    else:
        max_bid = Fraction(form.document['stages'][stage_id]['amount'])
        if amount_npv < sum([
                max_bid,
                max_bid * Fraction(form.document['minimalStepPercentage'])]):
            message = u'Amount NPV: Too low value'
            append_error_to_form(form, message)
            raise ValidationError(message)


class BidsForm(Form):
    bidder_id = StringField(
        'bidder_id',
        [InputRequired(message=u'No bidder id')]
    )

    yearlyPaymentsPercentage = DecimalField(
        'yearlyPaymentsPercentage',
        validators=[
            validate_yearly_payments_percentage,
            InputRequired(message=u'Provide yearlyPaymentsPercentage')
        ]
    )
    contractDuration = IntegerField(
        'contractDuration',
        validators=[
            NumberRange(
                0,
                MAX_CONTRACT_DURATION,
                'contractDuration must be between %(min)s and %(max)s.'
            )]
    )
    contractDurationDays = IntegerField(
        'contractDurationDays',
        validators=[
            validate_contract_duration,
            NumberRange(
                0,
                DAYS_IN_YEAR-1,
                'contractDurationDays must be between %(min)s and %(max)s.'
            )
        ]
    )

    def validate_bidder_id(self, field):
        stage_id = self.document['current_stage']
        if self.document['stages'][stage_id]['type'] == 'bids':
            validate_bidder_id_on_bidding(self, field)

    def validate(self):
        if super(BidsForm, self).validate():
            try:
                if (str(self.yearlyPaymentsPercentage.data ) == "-1") and (self.contractDurationDays.data == 0) and (self.contractDuration.data == 0):
                    return -1

                if self.contractDuration.data == 0 and self.contractDurationDays.data == 0:
                    message = u'You can\'t bid 0 days and 0 years'
                    append_error_to_form(self, message)
                    raise ValidationError(message)
                nbu_rate = self.auction.auction_document['NBUdiscountRate']
                annual_costs_reduction = [
                    bid['annualCostsReduction']
                    for bid in self.document['initial_bids']
                    if bid['bidder_id'] == self.bidder_id.data
                ][0]
                amount = npv(self.contractDuration.data,    
                             self.contractDurationDays.data,
                             self.yearlyPaymentsPercentage.data,
                             annual_costs_reduction,
                             parser.parse(self.auction.auction_document['noticePublicationDate']), # XXX TODO TEMP!!!!!
                             nbu_rate)
                stage_id = self.document['current_stage']
                if self.document['stages'][stage_id]['type'] == 'bids':
                    validate_bid_change_on_bidding(self, amount)
                else:
                    message = u'Stage not for bidding'
                    append_error_to_form(self, message)
                    raise ValidationError(message)
                return amount
            except ValidationError:
                return False
        return False


def form_handler():
    auction = app.config['auction']
    raw_data = {field: str(data) for field, data in request.json.items()}
    with auction.bids_actions:
        form = app.bids_form.from_json(raw_data)
        form.auction = auction
        form.document = auction.db.get(auction.auction_doc_id)
        current_time = datetime.now(timezone('Europe/Kiev'))
        total_amount = form.validate()
        if total_amount:
            # write data
            auction.add_bid(form.document['current_stage'], {
                'bidder_id': form.data['bidder_id'],
                'amount': total_amount,
                'contractDurationYears': form.data['contractDuration'],
                'contractDurationDays': form.data['contractDurationDays'],
                'yearlyPaymentsPercentage': float(form.data['yearlyPaymentsPercentage']),
                'time': current_time.isoformat()
            })
            if form.data['yearlyPaymentsPercentage']:
                app.logger.info(
                    "Bidder {} with client_id {} canceled bids in "
                    "stage {} in {}".format(form.data['bidder_id'],
                                            session['client_id'],
                                            form.document['current_stage'],
                                            current_time.isoformat()), 
                    extra=prepare_extra_journal_fields(request.headers)
                )
            else:
                app.logger.info("Bidder {} with client_id {} placed bid {} in {}".format(
                    form.data['bidder_id'], session['client_id'],
                    form.data['bid'], current_time.isoformat()
                ), extra=prepare_extra_journal_fields(request.headers))
            return {'status': 'ok', 'data': form.data}
        else:
            app.logger.info("Bidder {} with client_id {} wants place bid {} in {} with errors {}".format(
                request.json.get('bidder_id', 'None'), session['client_id'],
                request.json.get('bid', 'None'), current_time.isoformat(),
                repr(form.errors)
            ), extra=prepare_extra_journal_fields(request.headers))
            return {'status': 'failed', 'errors': form.errors}
