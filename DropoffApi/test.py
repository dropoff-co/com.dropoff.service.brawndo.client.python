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

print '*** Getting API Info ***'
info = json.loads(api.info())
print info
print '************************'


print '*** Getting Company Available Items ***'
company_available_items = json.loads(api.order.available_items({'company_id': info['data']['client']['id']}))

print company_available_items
print api.order.available_items({})

print '************************'


print '*** Creating Order With Items ***'

#temperature, container, sku, weight, person_name, quantity, description, unit, height, width, depth, price

order_items = [
    {"sku": "123456123456",
    "container": CONTAINER_BOX,
    "weight": 5,
    "person_name": "milller jack",
    "quantity": 2,
    "description": "this order is very important, ok, they're just cupcakes",
    "unit": "ft",
     "height": 4,
     "width": 4,
     "depth": 5,
     "price": "10.55",
     "temperature": "NA"},

    {"sku": "1234561523456",
     "container": "Box",
     "weight": 5,
     "person_name": "milller jack2",
     "quantity": 2,
     "description": "this order is very important, ok, they're just cupcakes",
     "unit": "ft",
     "height": 4,
     "width": 4,
     "depth": 5,
     "price": "10.55",
     "temperature": "NA"},

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
distance = 5
eta = 5
price = 5
t = datetime.datetime.now()
order_props = [2, 4]

tomorrow = t.replace(hour=10, minute=0, second=0) + datetime.timedelta(days=1)
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

create_params_with_items = {'origin': origin_params,
                 'destination': destination_params,
                 'details': details_params,
                 'properties': order_props,
                 'items': order_items}
order_create_with_items = json.loads(api.order.create(create_params_with_items))
print order_create_with_items
print '**********************'

print '*** Getting order info ***'
orderGetParams = {"order_id": "7816aed9d6653c7c360a8e21425273c5"}
orderGetReturn = api.order.get(orderGetParams)
print orderGetReturn

