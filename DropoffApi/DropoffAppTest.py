import datetime
import json
import time
import Order

import ApiV1

# api = ApiV1.ApiV1('sandbox-brawndo.dropoff.com', '/v1', 'sandbox-brawndo.dropoff.com',
#                   '',
#                   '')

api = ApiV1.ApiV1('localhost:9094', '/v1', 'http://localhost:9094',
                  '78ca06d0601c23751a642eed60acf69c65206ab825bbd10f81dde5fb370fac28',
                  '771f764454130af2c086e243e316feffe06d7f0aace18ad4ab16e47608efb625')

print '*** Getting API Info ***'
info = json.loads(api.info())
print info
print '************************'

print '*** Getting Company Properties Available ***'
#company_id = info['data']['client']['id']
#print company_id
#available_properties_params = {'company_id': company_id}
available_properties_params = {}
properties = json.loads(api.order.available_properties(available_properties_params))
print properties
print '************************'

print '*** Getting Company Available Items ***'
company_available_items = json.loads(api.order.available_items({'company_id': info['data']['client']['id']}))
print company_available_items
print api.order.available_items({})
company_available_items = json.loads(api.order.available_items({}))
print company_available_items
print '************************'

print '*** Getting Order Signature ***'
order_get_params = {'order_id': '01de44f7a46be2d6cda526dda87742a0'}
signature = json.loads(api.order.signature(order_get_params))
print signature
print '************************'

print '*** Getting Order Page ***'
order_get_params = {}
page = json.loads(api.order.get(order_get_params))
print page
print '**************************'

print '*** Getting Order Page 2 ***'
if 'last_key' in page:
    page1_last_key = page['last_key']
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

print '*** Creating Order with Items***'
order_items = [
    {"sku": "123456123456",
     "container": Order.CONTAINER_BOX,
     "weight": 5,
     "person_name": "milller jack",
     "quantity": 2,
     "description": "This order is very important.",
     "unit": "ft",
     "height": 4,
     "width": 4,
     "depth": 5,
     "price": "10.55",
     "temperature": Order.TEMP_FROZEN},

    {"sku": "1234561523456",
     "container": Order.CONTAINER_BAG,
     "weight": 5,
     "person_name": "milller jack2",
     "quantity": 2,
     "description": "This order is very important. Please be quick",
     "unit": "ft",
     "height": 4,
     "width": 4,
     "depth": 5,
     "price": "10.55",
     "temperature": Order.TEMP_NA},

]
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
                 'details': details_params,
                 'items': order_items}

order_create_with_items = json.loads(api.order.create(create_params))
print order_create_with_items
print '**********************'

print '*** Getting an order with items ***'
created_order_with_items_id = order_create_with_items['data']['order_id']
orderGetParams = {"order_id": created_order_with_items_id}
orderGetReturn = api.order.get(orderGetParams)
print orderGetReturn
print '**********************'

print '*** Creating Order With Properties ***'
order_props = [2, 4]
create_params_with_properties = {'origin': origin_params,
                 'destination': destination_params,
                 'details': details_params,
                 'properties': order_props}
order_create_with_properties = json.loads(api.order.create(create_params_with_properties))
print order_create_with_properties
print '**********************'

print '*** Creating Tip ***'

tip_params = {'order_id': created_order_with_items_id,
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

print '*** Cancelling Test Order(s) ***'
order_cancel_params = {'order_id': created_order_with_items_id}
cancel = json.loads(api.order.cancel(order_cancel_params))
print cancel
print '************************'

created_order_with_properties_id = order_create_with_properties['data']['order_id']
order_cancel_params = {'order_id': created_order_with_properties_id}
cancel_order_with_properties = json.loads(api.order.cancel(order_cancel_params))
print cancel_order_with_properties
print '************************'

