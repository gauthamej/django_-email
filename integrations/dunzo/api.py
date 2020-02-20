import requests
from django.conf import settings

BASE_URL = settings.DUNZO_URL
TOKEN_URL = f'{BASE_URL}/api/v1/token'
CREATE_TASK_URL = f'{BASE_URL}/api/v1/tasks'

class DunzoApi:

    def __init__(self):
        self.client_id = settings.DUNZO_CLIENT_ID
        self.secret_key = settings.DUNZO_SECRET
        self.token = None

    def get_headers(self, generate_token=True):
        if not self.token and generate_token:
            self.generate_token()
        return {
            'Accept_Language': 'en_US',
            'Content-Type': 'application/json',
            'Authorization': self.token
        }

    def make_request(self, url, method='get', data=None, headers=None):
        request_method = getattr(requests, method)
        if not headers:
            headers = self.get_headers()
        print(headers)
        response = request_method(url, headers=headers, data=data)
        print(response.status_code)
        print(response.text)
        if response.status_code < 300:
            return True, response.json()
        try:
            return False, response.json()
        except:
            return False, response.text

    def generate_token(self):
        headers = self.get_headers(generate_token=False)
        headers.pop('Authorization')
        headers.update({
            'client-id': self.client_id,
            'client-secret': self.secret_key,
        })
        print(headers)
        success, response = self.make_request(TOKEN_URL, headers=headers)
        if success:
            self.token = response['token']

    def get_quote(self):
        self.make_request(BASE_URL + '/api/v1/quote')

    def create_order(payload):
        url = CREATE_TASK_URL
        return self.make_request(url, data=payload)
