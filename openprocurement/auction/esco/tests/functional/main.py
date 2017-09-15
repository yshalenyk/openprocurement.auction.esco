# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import os
import datetime
import json
import contextlib
import tempfile
from dateutil.tz import tzlocal
from gevent.subprocess import check_output, sleep


PWD = os.path.dirname(os.path.realpath(__file__))
CWD = os.getcwd()

@contextlib.contextmanager
def update_auctionPeriod(path, auction_type, time_shift=datetime.timedelta(seconds=120)):
    new_start_time = (datetime.datetime.now(tzlocal()) + time_shift).isoformat()
    with open(path) as file:
        data = json.loads(file.read())
    if auction_type == 'multilot':
        for lot in data['data']['lots']:
            lot['auctionPeriod']['startDate'] = new_start_time
    else:
        data['data']['auctionPeriod']['startDate'] = new_start_time

    with tempfile.NamedTemporaryFile(delete=False) as auction_file:
        json.dump(data, auction_file)
        auction_file.seek(0)
    yield auction_file.name
    auction_file.close()


def run_esco(auction_id):
    tender_file_path = os.path.join(PWD, 'data', 'tender_esco.json')
    with update_auctionPeriod(tender_file_path, auction_type='esco') as auction_file:
        check_output('{0}/bin/auction_esco planning {1}'
                     ' {0}/etc/auction_worker_esco.yaml --planning_procerude partial_db --auction_info {2}'.format(CWD, auction_id, auction_file).split())
    sleep(5)


def includeme(actions):
    actions['all'] = actions.get('all', [])
    actions['esco'] = (
        {'runner': run_esco,
         'data_file': os.path.join(PWD, 'data', 'tender_esco.json'),
         'auction_worker_defaults': 'auction_worker_defaults:{0}/etc/auction_worker_esco.yaml'.format(CWD)},
    )
    actions['all'] += actions['esco']
