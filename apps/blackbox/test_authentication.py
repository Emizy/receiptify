import json

import pytest
import requests

from apps.blackbox.endpoints import AuthEnums
from faker import Faker

fake = Faker()
TEST_USER_EMAIL = ''
TEST_USER_PASSWORD = ''


class TestAuth:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.payload = {
            "email": fake.email(),
            "mobile": fake.phone_number(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": fake.password()
        }
        self.endpoint = AuthEnums
        self.headers = {'Content-Type': 'application/json; charset=utf8'}

    def test_register(self):
        """
        this method test register endpoint and check if its return 201 status
        """
        response = requests.post(self.endpoint.REGISTER.value + "/", data=self.payload)
        data = response.json()
        assert response.status_code == 201
        assert 'message' in data

    def test_login(self):
        """
        this method handles if user created above can login
        """
        payload = {
            'email': TEST_USER_EMAIL,
            'password': TEST_USER_PASSWORD,
        }
        response = requests.post(self.endpoint.LOGIN.value + "/", data=json.dumps(payload),
                                 headers=self.headers)
        data = response.json()
        assert response.status_code == 200
