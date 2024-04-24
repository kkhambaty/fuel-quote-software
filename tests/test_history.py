import pytest
from flask.testing import FlaskClient
from database import db
from models import User, Profile, FuelQuoteForm

@pytest.fixture
def create_user_with_quotes():
    # Create test user and profile
    new_user = User(ID = 999, username='testuser', password='testpass')
    db.session.add(new_user)
    db.session.commit()
    
    test_profile = Profile(UserID=new_user.ID, FullName='John Doe', Address1='123 Elm St', Address2='Apt 1', City='Springfield', State='IL', Zipcode='12345')
    db.session.add(test_profile)
    db.session.commit()

    # Create multiple fuel quotes for the test user
    quotes = [
        FuelQuoteForm(UserID=new_user.ID, GallonsRequested='100', DeliveryAddress='123 Elm St Springfield, IL 12345', DeliveryDate='2024-01-01', PricePerGallon='2.50', TotalAmountDue='250.00'),
        FuelQuoteForm(UserID=new_user.ID, GallonsRequested='150', DeliveryAddress='123 Elm St Springfield, IL 12345', DeliveryDate='2024-02-01', PricePerGallon='2.50', TotalAmountDue='375.00')
    ]
    db.session.add_all(quotes)
    db.session.commit()

    yield new_user

    # Cleanup
    db.session.delete(test_profile)
    FuelQuoteForm.query.filter_by(UserID=new_user.ID).delete()
    db.session.delete(new_user)
    db.session.commit()

def test_get_fuel_quote_history_empty(client: FlaskClient, create_user_with_quotes):
    """Ensure it handles no history correctly."""
    user_id_str = str(create_user_with_quotes.ID)
    response = client.get(f'quote/fuelQuoteHistory/{user_id_str}')
    assert response.status_code == 200

def test_get_fuel_quote_history_non_empty(client: FlaskClient, create_user_with_quotes):
    """Ensure it retrieves and displays fuel quote history correctly."""
    user_id_str = str(create_user_with_quotes.ID)
    response = client.get(f'/quote/fuelQuoteHistory/{user_id_str}')
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert '100' in data and '150' in data  # Check for gallons from quotes
    assert '250.00' in data and '375.00' in data  # Check for total amounts from quotes
