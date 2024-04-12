import pytest
from app import app
from models import FuelQuoteForm
from database import db
from flask.testing import FlaskClient


@pytest.fixture
def create_fuel_quote_history():
    # create some sample fuel quote instances
    fuel_quote1 = FuelQuoteForm(GallonsRequested=100, DeliveryAddress='123 Main St', DeliveryDate='2024-04-15', PricePerGallon=3.50, TotalAmountDue=350)
    fuel_quote2 = FuelQuoteForm(GallonsRequested=150, DeliveryAddress='456 Elm St', DeliveryDate='2024-04-20', PricePerGallon=3.75, TotalAmountDue=562.50)
    db.session.add_all([fuel_quote1, fuel_quote2])
    db.session.commit()

    yield [fuel_quote1, fuel_quote2]

    # Teardown: Delete the fuel quotes from the database
    db.session.delete(fuel_quote1)
    db.session.delete(fuel_quote2)
    db.session.commit()

def test_get_fuel_quote_history_success(client: FlaskClient, create_fuel_quote_history):
    """Ensure fuel quote history retrieval works when data is available."""
    response = client.get('/quote/fuelQuoteHistory')

    assert response.status_code == 200

    # Check if the response contains the expected data
    assert b'123 Main St' in response.data
    assert b'456 Elm St' in response.data
    assert b'100' in response.data
    assert b'150' in response.data
    assert b'350.00' in response.data
    assert b'562.50' in response.data

def test_get_fuel_quote_history_no_data(client: FlaskClient):
    """Ensure correct response when there is no fuel quote history."""
    response = client.get('/quote/fuelQuoteHistory')
    assert response.status_code == 200
    assert b'No fuel quote history available.' in response.data