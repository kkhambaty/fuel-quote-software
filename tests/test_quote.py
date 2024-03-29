
from flask.testing import FlaskClient


def test_form_initialization_failure(client: FlaskClient):
    """Ensure form page is not rendered when the user has an invalid ID."""
    response = client.get('/quote/3')
    assert response.status_code == 404

def test_form_initialization_success(client: FlaskClient):
    """Ensure form page is rendered when authentic user ID is used."""
    response = client.get('/quote/1')
    assert response.status_code == 200

def test_invalid_form_submission_gallons(client: FlaskClient):
    """Ensure form won't accept invalid gallon input"""
    test_data = {
        'gallons': 0,  # Invalid number of gallons
        'address': '123 Example St, City, State',  # Example, real address comes from user profile
        'delivery': '2024-12-31',  # Valid delivery date
        'pricing': 4.00  # Example, real price would come from the pricing module. Will be implemented in a later assignment
    }
    response = client.post('/quote/1', data=test_data)
    assert response.status_code == 400

def test_invalid_form_submission_delivery_date(client: FlaskClient):
    """Ensure form won't accept invalid delivery date input"""
    test_data = {
        'gallons': 1,  # Valid number of gallons
        'address': '123 Example St, City, State',  # Example, real address comes from user profile
        'delivery': '',  # Invalid delivery date
        'pricing': 4.00  # Example, real price would come from the pricing module. Will be implemented in a later assignment
    }
    response = client.post('/quote/1', data=test_data)
    assert response.status_code == 400

def test_valid_form_submission(client: FlaskClient):
    """Ensure form can accept valid form input"""
    test_data = {
        'gallons': 1,  # Valid number of gallons
        'address': '123 Example St, City, State',  # Example, real address comes from user profile
        'delivery': '2024-12-31',  # Valid delivery date
        'pricing': 4.00  # Example, real price would come from the pricing module. Will be implemented in a later assignment
    }
    response = client.post('/quote/1', data=test_data)
    assert response.status_code == 200