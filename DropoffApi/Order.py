import json

import Tip


#Line item constants
LINE_ITEM_DISABLED = 0
LINE_ITEM_OPTIONAL = 1
LINE_ITEM_REQUIRED = 2

TEMP_NA = 0
TEMP_AMBIENT = 100
TEMP_REFRIGERATED = 200
TEMP_FROZEN = 300

CONTAINER_NA = 0
CONTAINER_BAG = 100
CONTAINER_BOX = 200
CONTAINER_TRAY = 300
CONTAINER_PALLET = 400
CONTAINER_BARREL = 500
CONTAINER_BASKET = 600
CONTAINER_BUCKET = 700
CONTAINER_CARTON = 800
CONTAINER_CASE = 900
CONTAINER_COOLER = 1000
CONTAINER_CRATE = 1100
CONTAINER_TOTE = 1200


class Order:
    def __init__(self, client):
        self._client = client
        self.tip = Tip.Tip(client)

    def available_items(self, items_params):
        query = {}

        if 'company_id' in items_params:
            query['company_id'] = items_params.get('company_id')

        path = '/order/items'
        return self._client.do_get(path, 'order', query)

    def estimate(self, estimate_params):
        query = {}

        if 'origin' in estimate_params:
            query['origin'] = estimate_params.get('origin')
        else:
            raise ValueError('Order.estimate: origin must be defined')

        if 'destination' in estimate_params:
            query['destination'] = estimate_params.get('destination')
        else:
            raise ValueError('Order.estimate: destination must be defined')

        if 'utc_offset' in estimate_params:
            query['utc_offset'] = estimate_params.get('utc_offset')
        else:
            raise ValueError('Order.estimate: utc_offset must be defined')

        if 'ready_timestamp' in estimate_params:
            query['ready_timestamp'] = estimate_params.get('ready_timestamp')

        if 'company_id' in estimate_params:
            query['company_id'] = estimate_params.get('company_id')

        return self._client.do_get('/estimate', 'estimate', query)

    def get(self, order_get_params):
        query = {}
        if 'company_id' in order_get_params:
            query['company_id'] = order_get_params.get('company_id')

        if 'last_key' in order_get_params:
            query['last_key'] = order_get_params.get('last_key')

        path = '/order'

        if 'order_id' in order_get_params:
            path += '/' + order_get_params['order_id']

        return self._client.do_get(path, 'order', query)

    def signature(self, order_get_params):
        query = {}
        if 'company_id' in order_get_params:
            query['company_id'] = order_get_params.get('company_id')

        path = '/order/signature'

        if 'order_id' in order_get_params:
            path += '/' + order_get_params.get('order_id')

        return self._client.do_get(path, 'order', query)

    def pickup_signature(self, order_get_params):
        query = {}
        if 'company_id' in order_get_params:
            query['company_id'] = order_get_params.get('company_id')

        path = '/order/pickup_signature'

        if 'order_id' in order_get_params:
            path += '/' + order_get_params.get('order_id')

        return self._client.do_get(path, 'order', query)

    def driver_actions_meta(self, driver_actions_meta_params):
        query = {}
        if 'company_id' in driver_actions_meta_params:
            query['company_id'] = driver_actions_meta_params.get('company_id')

        path = '/order/driver_actions_meta'

        return self._client.do_get(path, 'order', query)

    def create(self, order_create_params):
        query = {}
        if 'company_id' in order_create_params:
            query['company_id'] = order_create_params.get('company_id')

        payload = json.dumps(order_create_params)

        return self._client.do_post('/order', 'order', query, payload)

    def cancel(self, order_cancel_params):
        if 'order_id' not in order_cancel_params:
            raise ValueError('Order.cancel: order_id must be defined')

        query = {}
        if 'company_id' in order_cancel_params:
            query['company_id'] = order_cancel_params.get('company_id')

        path = '/order/' + order_cancel_params.get('order_id') + '/cancel'
        return self._client.do_post(path, 'order', query)

    def available_properties(self, available_properties_params):
        query = {}
        if 'company_id' in available_properties_params:
            query['company_id'] = available_properties_params.get('company_id')

        path = '/order/properties'
        return self._client.do_get(path, 'order', query)

    def simulate(self, simulate_params):
        query = {}

        if 'company_id' in simulate_params:
            query['company_id'] = simulate_params.get('company_id')

        if 'market' in simulate_params:
            path = '/order/simulate/' + simulate_params.get('market')
        elif 'order_id' in simulate_params:
            path = '/order/simulate/order/' + simulate_params.get('order_id')

        return self._client.do_get(path, 'order', query)
