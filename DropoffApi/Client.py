import binascii
import datetime
import hashlib
import hmac
import httplib
import urllib


class Client:
    def __init__(self, api_url, base_path, host, private_key, public_key):
        self._api_url = api_url
        self._base_path = base_path
        self._host = host
        self._private_key = private_key
        self._public_key = public_key
        self._client = httplib.HTTPSConnection(api_url)
        # localhost testing needs these last 2 lines
        # self._client = httplib.HTTPConnection(api_url)
        # self._client.set_debuglevel(1)
        self._client.connect()

    @staticmethod
    def get_dropoff_date():
        return datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

    @staticmethod
    def to_hex(bytes_to_encode):
        return binascii.hexlify(bytes_to_encode.encode('utf8')).replace('-', '')

    @staticmethod
    def do_hmac(data_to_encrypt, key):
        hash_message = hmac.new(key, data_to_encrypt, hashlib.sha512).hexdigest()
        return hash_message.lower().replace('-', '')

    def do_request(self, http_method, path, resource, query=None, payload=None):
        today = self.get_dropoff_date()

        uri = self._base_path + path
        if query is not None:
            queries = []
            for key, value in query.iteritems():
                queries.append(key + '=' + urllib.quote_plus(value))

            if len(queries) > 0:
                print queries
                uri += '?' + '&'.join(queries)

        api_headers = {'x-dropoff-date': today,
                       'accept': 'application/json',
                       'host': self._host,
                       'user-agent': 'DropoffBrawndo/1.0'}

        if payload is not None:
            api_headers['content-type'] = 'application/json'

        header_string = '\n'.join("%s:%s" % item for item in sorted(api_headers.iteritems()))
        header_key_string = ';'.join("%s" % item for item in sorted(api_headers.keys()))

        authorization_body = http_method + '\n' + path + '\n\n' + header_string + '\n\n' + header_key_string + '\n'

        body_hash = self.do_hmac(authorization_body, self._private_key)

        final_string_to_hash = 'HMAC-SHA512\n' + today + '\n' + resource + '\n' + body_hash

        first_key = 'dropoff' + self._private_key
        final_hash = self.do_hmac(today[:8], first_key)
        final_hash_hmac = self.do_hmac(resource, final_hash)
        auth_hash = self.do_hmac(final_string_to_hash, final_hash_hmac)

        header_auth_string = ''.join(['Authorization: HMAC-SHA512 Credential=', self._public_key, ',SignedHeaders=',
                                      header_key_string, ',Signature=', auth_hash])

        api_headers['authorization'] = header_auth_string

        if payload is not None:
            encoded_payload = payload.encode('utf8')
            self._client.request(http_method, uri, encoded_payload, api_headers)
        else:
            self._client.request(http_method, uri, headers=api_headers)

        req = self._client.getresponse()

        data = req.read()
        return data

    def do_get(self, path, resource, query=None):
        return self.do_request('GET', path, resource, query)

    def do_post(self, path, resource, query=None, payload=None):
        return self.do_request('POST', path, resource, query, payload)

    def do_delete(self, path, resource, query=None):
        return self.do_request('DELETE', path, resource, query)
