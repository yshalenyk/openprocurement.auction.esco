# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import os
from gevent.subprocess import check_output, sleep
from openprocurement.auction.tests.utils import update_auctionPeriod
from openprocurement.auction.esco.tests.data.data import ESCO_TENDER_ID


PWD = os.path.dirname(os.path.realpath(__file__))
CWD = os.getcwd()


def run_esco(worker_cmd, tender_file_path, auction_id):
    with update_auctionPeriod(tender_file_path, auction_type='simple')\
            as auction_file:
        check_output(worker_cmd.format(CWD, auction_id, auction_file).split())
    sleep(10)


def includeme():
    return {'esco': {
        'worker_cmd': '{0}/bin/auction_esco planning {1}'
                      ' {0}/etc/auction_worker_esco.yaml'
                      ' --planning_procerude partial_db --auction_info {2}',
        'runner': run_esco,
        'tender_file_path': '{0}/data/tender_esco.json'.format(PWD),
        'auction_id': ESCO_TENDER_ID,
        'auction_worker_defaults': 'auction_worker_defaults:{0}/etc/auction_worker_esco.yaml',
        'suite': PWD}
    }
