import pytest
from app.app import app
from app.config import test_wallet_uuid

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_wallet(client):

    response = client.get(
        "/addwallet",
    )
    assert response.status_code == 200
    assert "balance" in response.json and "id" in response.json and "uuid" in response.json

def test_balance_wallet_valid(client):
    wallet_uuid = test_wallet_uuid

    response = client.get(
        f"/api/v1/wallets/{wallet_uuid}",
    )
    assert response.status_code == 200
    assert "balance" in response.json
    
    
def test_balance_wallet_invalid(client):
    wallet_uuid = "test-uuid-123"

    response = client.get(
        f"/api/v1/wallets/{wallet_uuid}",
    )
    assert response.status_code == 404


def test_post_operation_deposit(client):
    wallet_uuid = test_wallet_uuid
    
    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": 20},
    )
    assert response.status_code == 200
    assert "balance" in response.json

def test_post_operation_withdraw(client):
    wallet_uuid = test_wallet_uuid
    
    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": 10},
    )
    assert response.status_code == 200
    assert "balance" in response.json

def test_post_operation_invalid(client):
    wallet_uuid = "test-uuid-123"
    
    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "INVALID", "amount": 1000},
    )
    assert response.status_code == 400

    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": -100},
    )
    assert response.status_code == 400
    
    