import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('AMO_TOKEN')
domain = os.getenv('AMOCRM_SUBDOMAIN')
redirect_url = os.getenv('AMOCRM_REDIRECT_URL')
client_id = os.getenv('AMOCRM_CLIENT_ID')


headers = {
    'Authorization': f'Bearer {TOKEN}',
    'User-Agent': 'amoCRM-oAuth-client/1.0',
    'Content-Type': 'application/json'
}


def get_data_for_create(data):
    return [
        {
            "name": data['name'],
            "first_name": "",
            "last_name": "",
            "entity_type": "contacts",
            "custom_fields_values": [
                {
                    "field_id": 2105315,
                    "field_name": "phone",
                    "values": [
                        {
                            "value": data['phone']
                        }
                    ]
                }
            ]
        }
    ]


def get_data_for_update(ids):
    return [{
        "id": ids,
        "custom_fields_values": [
            {
                "field_id": 2105315,
                "field_name": "phone",
                "values": [
                    {
                        "value": "79999999999"
                    }
                ]
            }
        ]

    }]

