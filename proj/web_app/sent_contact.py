import json
import requests
from .config import headers, domain, get_data_for_create, get_data_for_update


def create_contact(data):
    response = requests.post(domain + 'contacts', headers=headers, data=json.dumps(data))
    if ids := check_response(response):
        return ids
    return False


def update_custom_filed(ids):
    response = requests.patch(domain + 'contacts', headers=headers, data=json.dumps(get_data_for_update(ids)))


def check_response(response):
    if response.status_code == 200:
        response = response.json()
        return response['_embedded']['contacts'][0]['id']
    else:
        print(f'Error: {response.status_code}, {response.text}')
        return False


def add_client(data):
    create_contact(get_data_for_create(data))