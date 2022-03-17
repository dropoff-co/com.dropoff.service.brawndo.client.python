import requests


class Bulk:
    def __init__(self, client):
        self._client = client

    def create(self, bulk_create_params):
        query = {}
        if 'company_id' in bulk_create_params:
            query['company_id'] = bulk_create_params.get('company_id')
        payload = file.open('./shortest copy.csv')
        return self._client.do_post('/bulkupload', 'bulkupload', query, payload)

    def cancel(self, bulk_cancel_params):
        if 'bulk_id' not in bulk_cancel_params:
            raise ValueError('Bulk.cancel: bulk_id must be defined')

        path = '/bulkupload/' + bulk_cancel_params.get('bulk_id')
        return self._client.do_put(path, 'bulkupload')