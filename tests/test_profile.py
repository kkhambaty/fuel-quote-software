
def test_get_profile_success(client):
    """Ensure profile retrieval works."""
    response = client.get('/profile/1')  # Assuming you have a profile with ID 1
    assert response.status_code == 200
    assert 'John Doe' in response.json['fullName']

def test_update_profile_success(client):
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