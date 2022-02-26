import json

import pytest
import requests

from apps.blackbox.endpoints import AuthEnums, ReceiptEnums
from faker import Faker

fake = Faker()

TEST_USER_EMAIL = ''
TEST_USER_PASSWORD = ''

auth = AuthEnums
receipt = ReceiptEnums


@pytest.fixture(scope='session', autouse=True)
def get_token():
    response = requests.post(auth.LOGIN.value+"/", data=json.dumps({
        'email': TEST_USER_EMAIL,
        'password': TEST_USER_PASSWORD,
    }), headers={'Content-Type': 'application/json; charset=utf8'})
    data = response.json()
    return data.get('token').get('access')


class TestReceipt:
    def test_create_receipt(self, get_token):
        """
        TEST CREATE RECEIPT ENDPOINT TO VALIDATE IF IT RETURN 200
        :param get_token:
        :return:
        """
        token = get_token
        payload = {
            "name": fake.name(),
            "email": fake.email(),
            "mobile": fake.phone_number(),
            "address": fake.address(),
            "orders": [
                {
                    "name": fake.name(),
                    "price": fake.random_number()
                },
                {
                    "name": fake.name(),
                    "price": fake.random_number()
                }
            ]
        }
        response = requests.post(receipt.RECEIPT.value+"/", data=json.dumps(payload),
                                 headers={'Content-Type': 'application/json; charset=utf8',
                                          'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
