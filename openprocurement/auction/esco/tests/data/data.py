# -*- coding: utf-8 -*-

ESCO_TENDER_ID = '2' * 32
ESCO_TENDER_MULTILOT_ID = '3' * 32
ESCO_MEAT_TENDER_ID = '4' * 32
ESCO_MEAT_MULTILOT_TENDER_ID = '5' * 32


tender_data = {u'data': {u'NBUdiscountRate': 0.22,
                         u'auctionPeriod': {u'endDate': None,
                                            u'startDate': u'2017-10-03T11:17:21.076354+03:00'},
                         u'bids': [{u'date': u'2017-09-19T08:22:21.726234+00:00',
                                    u'id': u'd3ba84c66c9e4f34bfb33cc3c686f137',
                                    u'value': {u'amount': 9752.643835616438,
                                               u'amountPerformance': 850.1281928765416,
                                               u'annualCostsReduction': [400.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0,
                                                                         900.0],
                                               u'contractDuration': {u'days': 200,
                                                                     u'years': 12},
                                               u'currency': u'UAH',
                                               u'valueAddedTaxIncluded': True,
                                               u'yearlyPaymentsPercentage': 0.85}},
                                   {u'date': u'2017-09-19T08:22:24.038426+00:00',
                                    u'id': u'5675acc9232942e8940a034994ad883e',
                                    u'value': {u'amount': 9023.638356164383,
                                               u'amountPerformance': 672.4650719957199,
                                               u'annualCostsReduction': [200.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0,
                                                                         800.0],
                                               u'contractDuration': {u'days': 40,
                                                                     u'years': 13},
                                               u'currency': u'UAH',
                                               u'valueAddedTaxIncluded': True,
                                               u'yearlyPaymentsPercentage': 0.86}}],
                         u'complaintPeriod': {u'endDate': u'2017-09-19T00:00:00+03:00',
                                              u'startDate': u'2017-08-23T11:17:21.076354+03:00'},
                         u'date': u'2017-10-03T11:17:57.282540+03:00',
                         u'dateModified': u'2017-10-03T11:17:57.882744+03:00',
                         u'guarantee': {u'amount': 8.0, u'currency': u'USD'},
                         u'id': u'11111111111111111111111111111111',
                         u'items': [{u'additionalClassifications': [{
                                                                        u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                                                        u'id': u'17.21.1',
                                                                        u'scheme': u'\u0414\u041a\u041f\u041f'}],
                                     u'classification': {u'description': u'Test',
                                                         u'id': u'37810000-9',
                                                         u'scheme': u'\u0414\u041a021'},
                                     u'deliveryAddress': {u'countryName': u'\u0423\u043a\u0440\u0430\u0457\u043d\u0430',
                                                          u'locality': u'\u043c. \u041a\u0438\u0457\u0432',
                                                          u'postalCode': u'79000',
                                                          u'region': u'\u043c. \u041a\u0438\u0457\u0432',
                                                          u'streetAddress': u'\u0432\u0443\u043b. \u0411\u0430\u043d\u043a\u043e\u0432\u0430 1'},
                                     u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                     u'description_en': u'Services in school canteens',
                                     u'id': u'896096667a4146ae990a6f6872fa66e5',
                                     u'unit': {u'code': u'44617100-9', u'name': u'item'}},
                                    {u'additionalClassifications': [{
                                                                        u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                                                        u'id': u'17.21.1',
                                                                        u'scheme': u'\u0414\u041a\u041f\u041f'}],
                                     u'classification': {u'description': u'Test',
                                                         u'id': u'37810000-9',
                                                         u'scheme': u'\u0414\u041a021'},
                                     u'deliveryAddress': {u'countryName': u'\u0423\u043a\u0440\u0430\u0457\u043d\u0430',
                                                          u'locality': u'\u043c. \u041a\u0438\u0457\u0432',
                                                          u'postalCode': u'79000',
                                                          u'region': u'\u043c. \u041a\u0438\u0457\u0432',
                                                          u'streetAddress': u'\u0432\u0443\u043b. \u0411\u0430\u043d\u043a\u043e\u0432\u0430 1'},
                                     u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                     u'description_en': u'Services in school canteens',
                                     u'id': u'1484c360c4f446e08fb8b563c4dae36d',
                                     u'unit': {u'code': u'44617100-9', u'name': u'item'}}],
                         u'minimalStepPercentage': 0.006,
                         u'noticePublicationDate': u'2017-10-03T11:17:51.420717+03:00',
                         u'numberOfBids': 2,
                         u'owner': u'broker',
                         u'procurementMethod': u'open',
                         u'procurementMethodType': u'esco',
                         u'status': u'active.auction',
                         u'submissionMethod': u'electronicAuction',
                         u'tenderID': u'UA-11111',
                         u'tenderPeriod': {u'endDate': u'2017-09-23T11:17:21.076354+03:00',
                                           u'startDate': u'2017-08-23T11:17:21.076354+03:00'},
                         u'title': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                         u'title_en': u'Services in school canteens',
                         u'yearlyPaymentsPercentageRange': 0.8}}

lot_tender_data = {u'data': {u'NBUdiscountRate': 0.22,
                         u'auctionPeriod': {u'endDate': None,
                                            u'startDate': u'2017-10-03T11:17:21.076354+03:00'},
                         u'bids': [{u'date': u'2017-09-19T08:22:21.726234+00:00',
                                    u'id': u'd3ba84c66c9e4f34bfb33cc3c686f137',
                                    u'lotValues': [{u'date': u'2017-09-19T08:22:22.726234+00:00',
                                                                u'relatedLot': u'f2b79975568642559e0f0283effa50d4',
                                                                u'status': u'active',
                                                    u'value': {u'amount': 9752.643835616438,
                                                               u'amountPerformance': 850.1281928765416,
                                                               u'annualCostsReduction': [400.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0,
                                                                                         900.0],
                                                               u'contractDuration': {u'days': 200, u'years': 12},
                                                               u'currency': u'UAH',
                                                               u'valueAddedTaxIncluded': True,
                                                               u'yearlyPaymentsPercentage': 0.85}}],
                                    u'status': u'active'},
                                   {u'date': u'2017-09-19T08:22:24.038426+00:00',
                                    u'id': u'5675acc9232942e8940a034994ad883e',
                                    u'lotValues': [{u'date': u'2017-09-19T08:22:25.038426+00:00',
                                                    u'relatedLot': u'f2b79975568642559e0f0283effa50d4',
                                                    u'status': u'active',
                                                    u'value': {u'amount': 9023.638356164383,
                                                               u'amountPerformance': 672.4650719957199,
                                                               u'annualCostsReduction': [200.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0,
                                                                                         800.0],
                                                               u'contractDuration': {u'days': 40, u'years': 13},
                                                               u'currency': u'UAH',
                                                               u'valueAddedTaxIncluded': True,
                                                               u'yearlyPaymentsPercentage': 0.86}}],
                                    u'status': u'active'}],
                         u'complaintPeriod': {u'endDate': u'2017-09-19T00:00:00+03:00',
                                              u'startDate': u'2017-08-23T11:17:21.076354+03:00'},
                         u'date': u'2017-10-03T11:17:57.282540+03:00',
                         u'dateModified': u'2017-10-03T11:17:57.882744+03:00',
                         u'guarantee': {u'amount': 8.0, u'currency': u'USD'},
                         u'id': u'11111111111111111111111111111111',
                         u'items': [{u'additionalClassifications': [{
                                                                        u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                                                        u'id': u'17.21.1',
                                                                        u'scheme': u'\u0414\u041a\u041f\u041f'}],
                                     u'classification': {u'description': u'Test',
                                                         u'id': u'37810000-9',
                                                         u'scheme': u'\u0414\u041a021'},
                                     u'deliveryAddress': {u'countryName': u'\u0423\u043a\u0440\u0430\u0457\u043d\u0430',
                                                          u'locality': u'\u043c. \u041a\u0438\u0457\u0432',
                                                          u'postalCode': u'79000',
                                                          u'region': u'\u043c. \u041a\u0438\u0457\u0432',
                                                          u'streetAddress': u'\u0432\u0443\u043b. \u0411\u0430\u043d\u043a\u043e\u0432\u0430 1'},
                                     u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                     u'description_en': u'Services in school canteens',
                                     u'id': u'896096667a4146ae990a6f6872fa66e5',
                                     u'unit': {u'code': u'44617100-9', u'name': u'item'}},
                                    {u'additionalClassifications': [{
                                                                        u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                                                        u'id': u'17.21.1',
                                                                        u'scheme': u'\u0414\u041a\u041f\u041f'}],
                                     u'classification': {u'description': u'Test',
                                                         u'id': u'37810000-9',
                                                         u'scheme': u'\u0414\u041a021'},
                                     u'deliveryAddress': {u'countryName': u'\u0423\u043a\u0440\u0430\u0457\u043d\u0430',
                                                          u'locality': u'\u043c. \u041a\u0438\u0457\u0432',
                                                          u'postalCode': u'79000',
                                                          u'region': u'\u043c. \u041a\u0438\u0457\u0432',
                                                          u'streetAddress': u'\u0432\u0443\u043b. \u0411\u0430\u043d\u043a\u043e\u0432\u0430 1'},
                                     u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                     u'description_en': u'Services in school canteens',
                                     u'id': u'1484c360c4f446e08fb8b563c4dae36d',
                                     u'unit': {u'code': u'44617100-9', u'name': u'item'}}],
                         u'minimalStepPercentage': 0.006,
                         u'noticePublicationDate': u'2017-10-03T11:17:51.420717+03:00',
                         u'numberOfBids': 2,
                         u'owner': u'broker',
                         u'procurementMethod': u'open',
                         u'procurementMethodType': u'esco',
                         u'status': u'active.auction',
                         u'submissionMethod': u'electronicAuction',
                         u'tenderID': u'UA-11111',
                         u'tenderPeriod': {u'endDate': u'2017-09-23T11:17:21.076354+03:00',
                                           u'startDate': u'2017-08-23T11:17:21.076354+03:00'},
                         u'lots': [{u'auctionPeriod': {u'shouldStartAfter': u'2017-10-10T00:00:00+03:00',
                                                       u'startDate': u'2017-10-09T11:31:20.062011+03:00'},
                                    u'date': u'2017-10-09T11:31:26.750789+03:00',
                                    u'description': u'lot description',
                                    u'fundingKind': u'other',
                                    u'id': u'f2b79975568642559e0f0283effa50d4',
                                    u'minValue': {u'amount': 0.0,
                                                  u'currency': u'UAH',
                                                  u'valueAddedTaxIncluded': True},
                                    u'minimalStepPercentage': 0.025,
                                    u'status': u'active',
                                    u'title': u'lot title',
                                    u'yearlyPaymentsPercentageRange': 0.8}],
                         u'title': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                         u'title_en': u'Services in school canteens',
                         u'yearlyPaymentsPercentageRange': 0.8}}

features_tender_data = {u'data': {u'NBUdiscountRate': 0.22,
                                  u'auctionPeriod': {u'endDate': None,
                                                     u'startDate': u'2017-10-03T11:17:21.076354+03:00'},
                                  u'bids': [{u'date': u'2017-09-19T08:22:21.726234+00:00',
                                             u'id': u'd3ba84c66c9e4f34bfb33cc3c686f137',
                                             u'value': {u'amount': 9752.643835616438,
                                                        u'amountPerformance': 850.1281928765416,
                                                        u'annualCostsReduction': [400.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0,
                                                                                  900.0],
                                                        u'contractDuration': {u'days': 200,
                                                                              u'years': 12},
                                                        u'currency': u'UAH',
                                                        u'valueAddedTaxIncluded': True,
                                                        u'yearlyPaymentsPercentage': 0.85},
                                             u'parameters': [
                                                 {u'code': u'OCDS-123454-AIR-INTAKE', u'value': 0.03},
                                                 {u'code': u'OCDS-123454-YEARS', u'value': 0.03}
                                             ]},
                                            {u'date': u'2017-09-19T08:22:24.038426+00:00',
                                             u'id': u'5675acc9232942e8940a034994ad883e',
                                             u'value': {u'amount': 9023.638356164383,
                                                        u'amountPerformance': 672.4650719957199,
                                                        u'annualCostsReduction': [200.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0,
                                                                                  800.0],
                                                        u'contractDuration': {u'days': 40,
                                                                              u'years': 13},
                                                        u'currency': u'UAH',
                                                        u'valueAddedTaxIncluded': True,
                                                        u'yearlyPaymentsPercentage': 0.86},
                                             u'parameters': [
                                                 {u'code': u'OCDS-123454-AIR-INTAKE', u'value': 0.07},
                                                 {u'code': u'OCDS-123454-YEARS', u'value': 0.07}
                                             ]}],
                                  u'complaintPeriod': {u'endDate': u'2017-09-19T00:00:00+03:00',
                                                       u'startDate': u'2017-08-23T11:17:21.076354+03:00'},
                                  u'date': u'2017-10-03T11:17:57.282540+03:00',
                                  u'dateModified': u'2017-10-03T11:17:57.882744+03:00',
                                  u'features': [{u'code': u'OCDS-123454-AIR-INTAKE',
                                                 u'description': u'\u0415\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u0430 \u043f\u043e\u0442\u0443\u0436\u043d\u0456\u0441\u0442\u044c \u0432\u0441\u043c\u043e\u043a\u0442\u0443\u0432\u0430\u043d\u043d\u044f \u043f\u0438\u043b\u043e\u0441\u043e\u0441\u0430, \u0432 \u0432\u0430\u0442\u0430\u0445 (\u0430\u0435\u0440\u043e\u0432\u0430\u0442\u0430\u0445)',
                                                 u'enum': [{u'title': u'\u0414\u043e 1000 \u0412\u0442',
                                                            u'value': 0.03},
                                                           {
                                                               u'title': u'\u0411\u0456\u043b\u044c\u0448\u0435 1000 \u0412\u0442',
                                                               u'value': 0.07}],
                                                 u'featureOf': u'item',
                                                 u'relatedItem': u'1',
                                                 u'title': u'\u041f\u043e\u0442\u0443\u0436\u043d\u0456\u0441\u0442\u044c \u0432\u0441\u043c\u043e\u043a\u0442\u0443\u0432\u0430\u043d\u043d\u044f',
                                                 u'title_en': u'Air Intake'},
                                                {u'code': u'OCDS-123454-YEARS',
                                                 u'description': u'\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u0440\u043e\u043a\u0456\u0432, \u044f\u043a\u0456 \u043e\u0440\u0433\u0430\u043d\u0456\u0437\u0430\u0446\u0456\u044f \u0443\u0447\u0430\u0441\u043d\u0438\u043a \u043f\u0440\u0430\u0446\u044e\u0454 \u043d\u0430 \u0440\u0438\u043d\u043a\u0443',
                                                 u'enum': [{u'title': u'\u0414\u043e 3 \u0440\u043e\u043a\u0456\u0432',
                                                            u'value': 0.03},
                                                           {
                                                               u'title': u'\u0411\u0456\u043b\u044c\u0448\u0435 3 \u0440\u043e\u043a\u0456\u0432, \u043c\u0435\u043d\u0448\u0435 5 \u0440\u043e\u043a\u0456\u0432',
                                                               u'value': 0.05},
                                                           {
                                                               u'title': u'\u0411\u0456\u043b\u044c\u0448\u0435 5 \u0440\u043e\u043a\u0456\u0432',
                                                               u'value': 0.07}],
                                                 u'featureOf': u'tenderer',
                                                 u'title': u'\u0420\u043e\u043a\u0456\u0432 \u043d\u0430 \u0440\u0438\u043d\u043a\u0443',
                                                 u'title_en': u'Years trading'}],
                                  u'guarantee': {u'amount': 8.0, u'currency': u'USD'},
                                  u'id': u'11111111111111111111111111111111',
                                  u'items': [{u'additionalClassifications': [{
                                                                                 u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                                                                 u'id': u'17.21.1',
                                                                                 u'scheme': u'\u0414\u041a\u041f\u041f'}],
                                              u'classification': {u'description': u'Test',
                                                                  u'id': u'37810000-9',
                                                                  u'scheme': u'\u0414\u041a021'},
                                              u'deliveryAddress': {
                                                  u'countryName': u'\u0423\u043a\u0440\u0430\u0457\u043d\u0430',
                                                  u'locality': u'\u043c. \u041a\u0438\u0457\u0432',
                                                  u'postalCode': u'79000',
                                                  u'region': u'\u043c. \u041a\u0438\u0457\u0432',
                                                  u'streetAddress': u'\u0432\u0443\u043b. \u0411\u0430\u043d\u043a\u043e\u0432\u0430 1'},
                                              u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                              u'description_en': u'Services in school canteens',
                                              u'id': u'896096667a4146ae990a6f6872fa66e5',
                                              u'unit': {u'code': u'44617100-9', u'name': u'item'}},
                                             {u'additionalClassifications': [{
                                                                                 u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                                                                 u'id': u'17.21.1',
                                                                                 u'scheme': u'\u0414\u041a\u041f\u041f'}],
                                              u'classification': {u'description': u'Test',
                                                                  u'id': u'37810000-9',
                                                                  u'scheme': u'\u0414\u041a021'},
                                              u'deliveryAddress': {
                                                  u'countryName': u'\u0423\u043a\u0440\u0430\u0457\u043d\u0430',
                                                  u'locality': u'\u043c. \u041a\u0438\u0457\u0432',
                                                  u'postalCode': u'79000',
                                                  u'region': u'\u043c. \u041a\u0438\u0457\u0432',
                                                  u'streetAddress': u'\u0432\u0443\u043b. \u0411\u0430\u043d\u043a\u043e\u0432\u0430 1'},
                                              u'description': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                              u'description_en': u'Services in school canteens',
                                              u'id': u'1484c360c4f446e08fb8b563c4dae36d',
                                              u'unit': {u'code': u'44617100-9', u'name': u'item'}}],
                                  u'minimalStepPercentage': 0.006,
                                  u'noticePublicationDate': u'2017-10-03T11:17:51.420717+03:00',
                                  u'numberOfBids': 2,
                                  u'owner': u'broker',
                                  u'procurementMethod': u'open',
                                  u'procurementMethodType': u'esco',
                                  u'status': u'active.auction',
                                  u'submissionMethod': u'electronicAuction',
                                  u'tenderID': u'UA-11111',
                                  u'tenderPeriod': {u'endDate': u'2017-09-23T11:17:21.076354+03:00',
                                                    u'startDate': u'2017-08-23T11:17:21.076354+03:00'},
                                  u'title': u'\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0448\u043a\u0456\u043b\u044c\u043d\u0438\u0445 \u0457\u0434\u0430\u043b\u0435\u043d\u044c',
                                  u'title_en': u'Services in school canteens',
                                  u'yearlyPaymentsPercentageRange': 0.8}}
