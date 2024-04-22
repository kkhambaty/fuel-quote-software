
from flask.testing import FlaskClient
from database import db
from models import User, Profile
import pytest


@pytest.fixture
def create_user_and_profile():
    # Create test user
    new_user = User(ID = 999, username='testuser', password='testpass')
    db.session.add(new_user)
    db.session.commit()
    # Create a test profile for the test user
    test_profile = Profile(UserID=new_user.ID, FullName='John Doe', Address1='123 Elm St', Address2 = 'Apt 1', City='Springfield', State='IL', Zipcode='12345')
    db.session.add(test_profile)
    db.session.commit()
    yield test_profile
    # Delete test user and profile
    db.session.delete(test_profile)
    db.session.delete(new_user)
    db.session.commit()


def test_form_initialization_failure(client: FlaskClient):
    """Ensure form page is not rendered when the user has an invalid ID."""
    response = client.get('/quote/0')
    assert response.status_code == 404

def test_form_initialization_success(client: FlaskClient, create_user_and_profile):
    """Ensure form page is rendered when authentic user ID is used."""
    temp_profile = create_user_and_profile
    user_id_str = str(temp_profile.UserID)
    url_path = '/quote/' + user_id_str
    response = client.get(url_path)
    assert response.status_code == 200

def test_invalid_form_submission_gallons(client: FlaskClient, create_user_and_profile):
    """Ensure form won't accept invalid gallon input"""
    temp_profile = create_user_and_profile
    test_data = {
        'gallons': 0,  # Invalid number of gallons
        'address': '123 Example St, City, State',  # Example, real address comes from user profile
        'delivery': '2024-12-31',  # Valid delivery date
        'pricing': 4.00  # Example, real price would come from the pricing module. Will be implemented in a later assignment
    }
    response = client.post('/quote/' + str(temp_profile.UserID), data=test_data)
    assert response.status_code == 400

def test_invalid_form_submission_delivery_date(client: FlaskClient, create_user_and_profile):
    """Ensure form won't accept invalid delivery date input"""
    temp_profile = create_user_and_profile
    test_data = {
        'gallons': 1,  # Valid number of gallons
        'address': '123 Example St, City, State',  # Example, real address comes from user profile
        'delivery': '',  # Invalid delivery date
        'pricing': 4.00  # Example, real price would come from the pricing module. Will be implemented in a later assignment
    }
    response = client.post('/quote/' + str(temp_profile.UserID), data=test_data)
    assert response.status_code == 400

def test_valid_form_submission(client: FlaskClient, create_user_and_profile):
    """Ensure form can accept valid form input"""
    temp_profile = create_user_and_profile
    test_data = {
        'gallons': 1,  # Valid number of gallons
        'address': '123 Example St, City, State',  # Example, real address comes from user profile
        'delivery': '2024-12-31',  # Valid delivery date
        'pricing': 4.00  # Example, real price would come from the pricing module. Will be implemented in a later assignment
    }
    response = client.post('/quote/' + str(temp_profile.UserID), data=test_data)
    assert response.status_code == 200