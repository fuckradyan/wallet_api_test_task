# wallet api app

**Wallet API App** is a Flask-based application providing a simple wallet service. It exposes two endpoints: one to check the wallet balance and another to perform wallet operations (deposit and withdraw). The app uses PostgreSQL as its database, running in a separate container from the Flask application. Additionally, it includes tests to ensure the correctness of the endpoints and wallet operations.


## Installation
Clone a repository
```bash
git clone https://github.com/fuckradyan/wallet_api_test_task.git
```

Install docker and docker-compose if not installed
```bash
sudo apt install docker docker-compose
```
Create .env file and fill in following variables:

    POSTGRES_USER=<username>
    POSTGRES_PASSWORD=<password>
    POSTGRES_DB=<dbname>

Create config.py in app/ folder and fill in the following variable:

    import os
    db_addr = os.getenv('DB_NAME','localhost')
    SQLALCHEMY_DATABASE_URI=f'postgresql://<username>:<password>@{db_addr}:5432/<dbname>'

## Launch

Inside project diretory run a command:
```bash
docker-compose up -d
```
After building and running app wiil be able at ***localhost:5000***
## Usage

There are 3 endpoints you can interact with

### Create wallet [GET]
Endpoint will generate a wallet with random uuid and randint(1,10000) balance.

*Example request:*
```bash
curl localhost:5000/addwallet
```
*Example response:*
```bash
{"balance":5537,"id":38,"uuid":"2ffe685a-7150-4dea-93d0-ecc3f6d1f52a"}
```
### Show wallet balance [GET]
Endpoint returns the balance of a specific wallet.

*Example request:*
```bash
curl localhost:5000/api/v1/wallets/<wallet_uuid>
```
*Example response:*
```bash
{"balance":5537}
```
### Make operation with wallet [POST]
Make a deposit or withdraw operation with a specific wallet.

*Example request:*
```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data "{\"operation_type\":\"DEPOSIT\" or \"WITHDRAW\", \"amount\":100}" \
  localhost:5000/api/v1/wallets/<wallet_uuid>/operation
```
*Example response:*
```bash
{"balance":5537,"id":38,"uuid":"2ffe685a-7150-4dea-93d0-ecc3f6d1f52a"}
```

## Run tests

Create a virtual enviroment and activate it.

    python3 -m venv ve
    source /ve/Bin/activate
Install all dependencies.

    pip3 install -r requirements.txt
Paste in config.py variable ***test_wallet_uuid***  with existing wallet from database.

    test_wallet_uuid  =  "dca8063a-543d-42da-b045-40dbcbee7c0e"

Run tests.

    pytest -v -s

Expected output:

    tests/test_wallet.py::test_create_wallet PASSED
    tests/test_wallet.py::test_balance_wallet_valid PASSED
    tests/test_wallet.py::test_balance_wallet_invalid PASSED
    tests/test_wallet.py::test_post_operation_deposit PASSED
    tests/test_wallet.py::test_post_operation_withdraw PASSED
    tests/test_wallet.py::test_post_operation_invalid PASSED
