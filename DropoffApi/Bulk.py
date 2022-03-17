import requests
import urllib

class Bulk:
    def __init__(self, client):
        self._client = client

    def create(self, bulk_create_params):
        query = {}
        if 'company_id' in bulk_create_params:
            query['rate_card_id'] = bulk_create_params.get('company_id')
        if 'notification_email' in bulk_create_params:
            query['notification_email'] = bulk_create_params.get('notification_email')

        today = self._client.get_dropoff_date()
        uri = self._client._base_path + '/bulkupload'
        print '***************************'
        print today, uri
        if query is not None:
            queries = []
            for key, value in query.iteritems():
                queries.append(key + '=' + urllib.quote_plus(value))

            if len(queries) > 0:
                print queries
                uri += '?' + '&'.join(queries)

        api_headers = {'x-dropoff-date': today,
                       'accept': 'application/json',
                       'host': self._client._host,
                       'user-agent': 'DropoffBrawndo/1.0'}

        header_string = '\n'.join("%s:%s" % item for item in sorted(api_headers.iteritems()))
        header_key_string = ';'.join("%s" % item for item in sorted(api_headers.keys()))

        authorization_body = 'POST' + '\n' + '/bulkupload' + '\n\n' + header_string + '\n\n' + header_key_string + '\n'

        body_hash = self._client.do_hmac(authorization_body, self._client._private_key)

        final_string_to_hash = 'HMAC-SHA512\n' + today + '\n' + 'bulkupload' + '\n' + body_hash

        first_key = 'dropoff' + self._client._private_key
        final_hash = self._client.do_hmac(today[:8], first_key)
        final_hash_hmac = self._client.do_hmac('bulkupload', final_hash)
        auth_hash = self._client.do_hmac(final_string_to_hash, final_hash_hmac)

        header_auth_string = ''.join(['Authorization: HMAC-SHA512 Credential=', self._client._public_key, ',SignedHeaders=',
                                      header_key_string, ',Signature=', auth_hash])

        api_headers['authorization'] = header_auth_string

        r = requests.post('http://localhost:9094/v1/bulkupload', headers=api_headers, files={'file': open('./shortest copy.csv', 'rb')})
        return r.json()


    def cancel(self, bulk_cancel_params):
        if 'bulk_id' not in bulk_cancel_params:
            raise ValueError('Bulk.cancel: bulk_id must be defined')

        path = '/bulkupload/' + bulk_cancel_params.get('bulk_id')
        return self._client.do_put(path, 'bulkupload')