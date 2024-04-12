import pytest
from app import app
from models import FuelQuoteForm
from database import db
from flask.testing import FlaskClient


@pytest.fixture

def test_get_fuel_quote_history_with_data(client):
    # Assuming you have some test data in your database
    user_id = 1
    fuel_quote1 = FuelQuoteForm(DeliveryAddress='123 Main St', GallonsRequested=100, DeliveryDate='2024-04-01', PricePerGallon=3.50, TotalAmountDue=350.00, UserID=user_id)
    fuel_quote2 = FuelQuoteForm(DeliveryAddress='456 Elm St', GallonsRequested=150, DeliveryDate='2024-04-02', PricePerGallon=3.75, TotalAmountDue=562.50, UserID=user_id)
    db.session.add_all([fuel_quote1, fuel_quote2])
    db.session.commit()

    # Making a GET request to the route with the test user ID
    response = client.get(f'/fuelQuoteHistory/{user_id}')
    
    # Asserting that the response is successful
    assert response.status_code == 200
    
    # Asserting that the response contains the fuel quote history data
    assert b'123 Main St' in response.data
    assert b'456 Elm St' in response.data
    assert b'100' in response.data
    assert b'150' in response.data
    assert b'2024-04-01' in response.data
    assert b'2024-04-02' in response.data
    assert b'3.50' in response.data
    assert b'3.75' in response.data
    assert b'350.00' in response.data
    assert b'562.50' in response.data

def test_get_fuel_quote_history_empty(client):
    # Assuming the database is empty

    # Making a GET request to the route with a test user ID
    user_id = 1
    response = client.get(f'/fuelQuoteHistory/{user_id}')
    
    # Asserting that the response is successful
    assert response.status_code == 404

def test_get_fuel_quote_history_error_handling(client):
    # Making a GET request to the route with an invalid request (e.g., wrong HTTP method)
    response = client.post('/fuelQuoteHistory')
    
    # Asserting that the response status code indicates a bad request
    assert response.status_code == 404

def test_get_fuel_quote_history_empty_history(client):
    # Assuming there is a user with no fuel quote history
    user_id = 2  # Assuming this user ID exists but has no fuel quote history
    response = client.get(f'/fuelQuoteHistory/{user_id}')
    
    # Asserting that the response status code indicates success (if the user exists) or not found (if the user doesn't exist)
    assert response.status_code in [200, 404]
def test_get_fuel_quote_history_max_user_id(client):
    # Making a GET request to the route with the maximum possible user ID
    user_id = 2147483647  # Assuming this is the maximum user ID
    response = client.get(f'/fuelQuoteHistory/{user_id}')
    
    # Asserting that the response status code indicates success (if the user exists) or not found (if the user doesn't exist)
    assert response.status_code in [200, 404]


