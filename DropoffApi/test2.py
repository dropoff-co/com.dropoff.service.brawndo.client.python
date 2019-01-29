import datetime
import time
import json

import ApiV1

# api = ApiV1.ApiV1('sandbox-brawndo.dropoff.com', '/v1', 'sandbox-brawndo.dropoff.com',
#                   '',
#                   '')

api = ApiV1.ApiV1('localhost:9094', '/v1', 'http://localhost:9094',
                  '78ca06d0601c23751a642eed60acf69c65206ab825bbd10f81dde5fb370fac28',
                  '771f764454130af2c086e243e316feffe06d7f0aace18ad4ab16e47608efb625')

# print '*** Getting API Info ***'
# info = json.loads(api.info())
# print info
# print '************************'
#

print '*** Getting Company Available Items ***'
print {'company_id': '7df2b0bdb418157609c0d5766fb7fb12'}
company_available_items = json.loads(api.order.available_items({'company_id': '7df2b0bdb418157609c0d5766fb7fb12'}))

print company_available_items
print api.order.available_items({})

print '************************'
