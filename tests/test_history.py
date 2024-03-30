import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_fuel_quote_history(client):
    response = client.get('/quote/fuelQuoteHistory')
    assert response.status_code == 200
    
    # Check if response is in JSON format
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
   # Check if response contains the expected content
    assert b'Fuel Quote History' in response.data
    assert b'Name' in response.data
    assert b'Gallons Requested' in response.data
    assert b'Delivery Address' in response.data
    assert b'Delivery Date' in response.data
    assert b'Suggested Price/Gallon' in response.data
    assert b'Total Amount Due' in response.data