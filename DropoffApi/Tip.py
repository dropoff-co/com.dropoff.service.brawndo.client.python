
class Tip:
    def __init__(self, client):
        self._client = client

    def create(self, tip_create_params):
        if 'order_id' not in tip_create_params:
            raise ValueError('Tip.create: order_id must be defined')

        if 'amount' not in tip_create_params:
            raise ValueError('Tip.create: amount must be defined')

        query = {}
        if 'company_id' in tip_create_params:
            query['company_id'] = tip_create_params.get('company_id')

        path = '/order/' + tip_create_params.get('order_id') + '/tip/' + str(tip_create_params.get('amount'))

        return self._client.do_post(path, 'order', query)

    def get(self, tip_params):
        if 'order_id' not in tip_params:
            raise ValueError('Tip.get: order_id must be defined')

        query = {}
        if 'company_id' in tip_params:
            query['company_id'] = tip_params.get('company_id')

        path = '/order/' + tip_params.get('order_id') + '/tip'
        return self._client.do_get(path, 'order', query)

    def delete(self, tip_delete_params):
        if 'order_id' not in tip_delete_params:
            raise ValueError('Tip.delete: order_id must be defined')

        query = {}
        if 'company_id' in tip_delete_params:
            query['company_id'] = tip_delete_params.get('company_id')

        path = '/order/' + tip_delete_params.get('order_id') + '/tip'
        return self._client.do_delete(path, 'order', query)
