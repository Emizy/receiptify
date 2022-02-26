import enum
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = 'http://127.0.0.1:8000'


class AuthEnums(enum.Enum):
    LOGIN = f'{BASE_URL}/v1/api/auth/login'
    REGISTER = f'{BASE_URL}/v1/api/auth/register'


class ReceiptEnums(enum.Enum):
    RECEIPT = f'{BASE_URL}/v1/api/receipt'
