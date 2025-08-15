import pytest
from app.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_post_operation_deposit(client):
    wallet_uuid = "e1989086-4220-4937-9f32-cc9158eff303"
    
    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": 20},
    )
    assert response.status_code == 200
    assert "balance" in response.json

def test_post_operation_withdraw(client):
    wallet_uuid = "e1989086-4220-4937-9f32-cc9158eff303"
    
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