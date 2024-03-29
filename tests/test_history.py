import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_fuel_quote_history(client):
    response = client.get('/fuelQuoteHistory')
    assert response.status_code == 200
    
    # Check if response is in JSON format
    assert response.headers['Content-Type'] == 'application/json'
    
    # Check if response data is a list
    data = response.json
    assert isinstance(data, list)
    
    # Check if each item in the list has the expected keys
    for item in data:
        assert 'Name' in item
        assert 'Gallons Requested' in item
        assert 'Delivery Address' in item
        assert 'Delivery Date' in item
        assert 'Suggested Price/Gallon' in item
        assert 'Total Amount Due' in item