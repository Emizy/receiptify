# RECEIPT APP

Tasks Background
The product designer has just shared some mockups with us. On the mockup, the user is able generate receipts for a given transaction. Due to regulatory requirements, our system needs to generate and save 10 different PDF copies of receipts each time the user clicks on the button to generate receipt for the transaction. Ideally, the receipts would all look different. But for the sake of this test, you can write a very simple receipt template that can be used for all of the 10 receipt generation operations.

## APP REFERENCE

This project divided into module ``blackbox`` ``core`` and ``util`` 

### APPS AND FUNCTIONS

- blackbox : This contains test suite for ```authentication section``` , ``recipients``
- core: This contains e core functionalities of the system
- UTILS: This contains globally used methods on the system

## Run Locally

Clone the project

```bash
  git clone https://github.com/Emizy/receiptify.git
```

Go to the project directory

```bash
  cd receiptify
```

Install dependencies

```bash
  pip install -r requirements.txt
```

TEST SETUP ENVIRONMENT VARIABLE
## parameters must be set inside test_receipt.py and test_authentication.py
TEST_USER_EMAIL = ''
TEST_USER_PASSWORD = ''

RUN TEST SUITE

```bash
  pytest
```
