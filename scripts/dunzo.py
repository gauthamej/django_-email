import os
import dotenv
import requests
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.read_dotenv(BASE_DIR, '.env')

DUNZO_CLIENT_ID = os.environ.get('DUNZO_CLIENT_ID')
DUNZO_SECRET = os.environ.get('DUNZO_SECRET')
DUNZO_URL = os.environ.get('DUNZO_URL')

url = f'{DUNZO_URL}/api/v1/token'
headers = {
    'client-id': DUNZO_CLIENT_ID,
    'client-secret': DUNZO_SECRET,
    'Accept_Language': 'en_US',
    'Content-Type': 'application/json'
}
response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text)

headers = {
    'Authorization': response.json()['token']
}
response = requests.get(f'{DUNZO_URL}/api/v1/quote', headers=headers)
print(response.json())
