
from flask import url_for
from flask.testing import FlaskClient
from modules.profile.profile_page import valid_profile_data


def test_get_profile_success(client: FlaskClient):
    """Ensure profile retrieval works."""
    response = client.get('/profile/1')  # Assuming you have a profile with ID 1
    assert response.status_code == 200
    assert 'John Doe' in response.json['fullName']

def test_update_profile_success(client: FlaskClient):
    """Ensure profile update works."""
    new_data = {
        'fullName': 'Jane Doe',
        'address1': '123 Maple St',
        'city': 'Springfield',
        'state': 'IL',
        'zipcode': '12345'
    }
    response = client.post('/profile/1', json=new_data)  # Make sure your endpoint supports JSON
    assert response.status_code == 200
    assert response.json['message'] == 'Profile updated successfully'


def test_get_profile_not_found(client: FlaskClient):
    """Ensure correct response when a profile is not found."""
    response = client.get('/profile/999')  # Assuming 999 does not exist
    assert response.status_code == 404
    assert 'Profile not found' in response.json['error']

def test_update_profile_invalid_data(client: FlaskClient):
    """Ensure profile update fails with invalid data."""
    invalid_data = {'fullName': '', 'address1': '123 Maple St'}  # fullName cannot be empty
    response = client.post('/profile/1', json=invalid_data)
    assert response.status_code == 400
    assert 'Invalid profile data' in response.json['error']

def test_update_non_existing_profile(client: FlaskClient):
    """Ensure updating a non-existing profile fails."""
    new_data = {'fullName': 'Jane Doe', 'address1': '456 Pine St', 'address2': 'Apt 101', 'city': 'Anytown', 'state': 'TX', 'zipcode': '12345'}
    response = client.post('/profile/999', json=new_data)  # Assuming 999 does not exist
    assert response.status_code == 404
    assert 'Profile not found' in response.json['error']

def test_update_profile_missing_fields(client):
    """Ensure profile update fails when required fields are missing."""
    incomplete_data = {'fullName': 'Jane Doe'}  # Assuming other fields are required
    response = client.post('/profile/1', json=incomplete_data)
    assert response.status_code == 400
    assert 'Invalid profile data' in response.json['error']

def test_valid_profile_data():
    """Ensure profile data validation works as expected."""
    valid_data = {'fullName': 'John Doe', 'address1': '123 Elm St', 'city': 'San Diego', 'state': 'CA', 'zipcode': '12345'}
    assert valid_profile_data(valid_data) is True

    invalid_data = {'fullName': 'John Doe', 'address1': '123 Elm St', 'city': 'San Diego', 'state': 'XY', 'zipcode': '12345'}
    assert valid_profile_data(invalid_data) is False

def test_add_new_profile(client: FlaskClient):
    """Ensure adding a new profile through POST request is successful."""
    new_data = {
        'fullName': 'Jane Doe',
        'address1': '456 Pine St',
        'address2': 'Apt 101',
        'city': 'Anytown',
        'state': 'TX',
        'zipcode': '12345'
    }
    # Assuming user_id 3 does not exist yet
    response = client.post(url_for('profile.create_profile', user_id=3), json=new_data)
    assert response.status_code == 201
    assert 'Profile created successfully' in response.json['message']
