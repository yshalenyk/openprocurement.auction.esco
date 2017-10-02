# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import os
import json
from gevent.subprocess import check_output, sleep
from openprocurement.auction.tests.utils import update_auctionPeriod


PWD = os.path.dirname(os.path.realpath(__file__))
CWD = os.getcwd()


def run_esco(tender_file_path):
    with open(tender_file_path) as _file:
        auction_id = json.load(_file).get('data', {}).get('id')
        if auction_id:
            with update_auctionPeriod(tender_file_path, auction_type='simple')\
                    as auction_file:
                check_output(
                        '{0}/bin/auction_esco planning {1}'
                        ' {0}/etc/auction_worker_esco.yaml'
                        ' --planning_procerude partial_db --auction_info {2}'
                        .format(CWD, auction_id, auction_file).split())
        sleep(30)


def includeme(tests):
    tests['esco'] = {
        "worker_cmd": '{0}/bin/auction_esco planning {1}'
                      ' {0}/etc/auction_worker_esco.yaml'
                      ' --planning_procerude partial_db --auction_info {2}',
        "runner": run_esco,
        'auction_worker_defaults': 'auction_worker_defaults:{0}/etc/auction_worker_esco.yaml',
        'suite': PWD
    }
