import datetime
import time
import json

import ApiV1

api = ApiV1.ApiV1('localhost:9094', '/v1', 'localhost:9094',
                  '74ac377c478a9fbd05203b3125db3f6402ead2d2ce1b9fa936c04fce43d8c168',
                  '11981f9d4c223a598fd2a550568064a259c08c367ce6d46cde2a47026b5e4bcb')

print '*** Getting API Info ***'
info = json.loads(api.info())
print info
print '************************'

print '*** Getting Order Page ***'
order_get_params = {}
page = json.loads(api.order.get(order_get_params))
print page
print '**************************'

print '*** Getting Order Page 2 ***'
page1_last_key = page['last_key']
if page1_last_key is not None:
    order_get_params['last_key'] = page1_last_key

page = json.loads(api.order.get(order_get_params))
print page

page2_last_key = page['last_key']

print 'page1_last_key: ' + page1_last_key
print 'page2_last_key: ' + page2_last_key
print 'last keys are equal? ' + str(page1_last_key == page2_last_key)
print '*****************************'

order_id = page['data'][0]['details']['order_id']
print '*** Getting Order Id: ' + order_id + ' ***'
order_get_params = {'order_id': order_id}

order = json.loads(api.order.get(order_get_params))
print order
print '******************************************'

print '*** Getting Order Estimate ***'
utc_offset = time.strftime('%z')
estimate_params = {'origin': '117 San Jacinto Blvd, Austin, TX 78701',
                   'destination': '901 S MoPac Expy, Austin, TX 78746',
                   'utc_offset': utc_offset}

estimate = json.loads(api.order.estimate(estimate_params))
print estimate
print '******************************'

print '*** Getting Order Estimate 2 ***'
t = datetime.datetime.now()
tomorrow = t.replace(hour=10, minute=0, second=0) + datetime.timedelta(days=1)

# print tomorrow.strftime('%s')
# print calendar.timegm(tomorrow.timetuple())

# estimate_params['ready_timestamp'] = str(calendar.timegm(tomorrow.timetuple()))
estimate_params['ready_timestamp'] = tomorrow.strftime('%s')
estimate = json.loads(api.order.estimate(estimate_params))
print estimate
print '*******************************'

print '*** Creating Order ***'
origin_params = {'company_name': "Gus's Fried Chicken",
                 'first_name': 'Napoleon',
                 'last_name': 'Bonner',
                 'address_line_1': '117 San Jacinto Blvd',
                 'address_line_2': '',
                 'city': 'Austin',
                 'state': 'TX',
                 'zip': '78701',
                 'phone': '5125555555',
                 'email': 'cluckcluck@gusfriedchicken.com',
                 'lat': 30.263706,
                 'lng': -97.741703,
                 'remarks': 'Origin Remarks'}

destination_params = {'company_name': 'Dropoff',
                      'first_name': 'Jason',
                      'last_name': 'Kastner',
                      'address_line_1': '901 S MoPac Expy',
                      'address_line_2': '#150',
                      'city': 'Austin',
                      'state': 'TX',
                      'zip': '78746',
                      'phone': '512-555-5555',
                      'email': 'jkastner+python+dropoff@dropoff.com',
                      'lat': 30.264573,
                      'lng': -97.782073,
                      'remarks': 'Please use the front entrance. The back one is guarded by cats!'}
distance = estimate['data']['Distance']
eta = estimate['data']['ETA']
price = estimate['data']['two_hr']['Price']
details_params = {'ready_date': tomorrow.strftime('%s'),
                  'type': 'two_hr',
                  'quantity': 10,
                  'weight': 20,
                  'distance': distance,
                  'eta': eta,
                  'price': price}

create_params = {'origin': origin_params,
                 'destination': destination_params,
                 'details': details_params}

order_create = json.loads(api.order.create(create_params))
print order_create
print '**********************'

print '*** Creating Tip ***'
created_order_id = order_create['data']['order_id']

tip_params = {'order_id': created_order_id,
              'amount': 4.44}

tip = json.loads(api.order.tip.create(tip_params))
print tip
print '********************'

print '*** Getting Tip ***'
tip = json.loads(api.order.tip.get(tip_params))
print tip
print '*******************'

print '*** Deleting Tip ***'
tip = json.loads(api.order.tip.delete(tip_params))
print tip
print '********************'

print '*** Cancelling Order ***'
order_cancel_params = {'order_id': created_order_id}
cancel = json.loads(api.order.cancel(order_cancel_params))
print cancel
print '************************'
