from Client import Client
from Order import Order


class ApiV1:
    def __init__(self, api_url, base_path, host, private_key, public_key):
        self.client = Client(api_url, base_path, host, private_key, public_key)
        self.order = Order(self.client)

    def info(self):
        return self.client.do_get('/info', 'info')
