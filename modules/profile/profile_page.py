import re
from flask import Blueprint, jsonify, render_template, request
profile_bp = Blueprint('profile', __name__)

profiles = {
    1: { 'fullName': 'Mohammed Bhai', 'address1': '123 Elm St', 'address2' : 'Suite 200', 'city' : 'San Diego', 'state': 'CA', 'zipcode' : '12345-6789'},
    2: { 'fullName': 'Clair Boyle', 'address1': '123 Fire St', 'address2' : 'Suite 300', 'city' : 'San Diego', 'state': 'CA', 'zipcode' : '12234-4321'}
}


@profile_bp.route('/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if request.method == 'GET':
        user_profile = find_profile_by_id(user_id)  # This function would fetch profile data
        if user_profile:
            response = jsonify(profiles[user_id])
            return response, 200
        else:
            return jsonify({"error": "Profile not found"}), 404
        
    elif request.method == 'POST':       
        if not profile_exists(user_id):
            # If the profile does not exist, return a 404 error instead of creating a new one
            return jsonify({"error": "Profile not found"}), 404

        profile_data = request.json
        if not valid_profile_data(profile_data):
            return jsonify({"error": "Invalid profile data"}), 400

        success = update_profile_by_id(user_id, profile_data)
        if success:
            return jsonify({"message": "Profile updated successfully"}), 200
        else:
            # If update fails for reasons other than non-existence, return a generic error message
            return jsonify({"error": "Profile update failed"}), 400
    

def find_profile_by_id(user_id):
    return profiles.get(user_id)

def update_profile_by_id(user_id, profile_data):
    if user_id in profiles:
        profiles[user_id].update(profile_data)
        return True
    else:
        return False
    
def profile_exists(user_id):
    return user_id in profiles

def valid_profile_data(profile_data):
    
    zipcode_pattern = re.compile(r'^\d{5}(-\d{4})?$')

    if not (profile_data.get('fullName') and len(profile_data['fullName']) <= 50):
        return False
    
    if not (profile_data.get('address1') and len(profile_data['address1']) <= 100):
        return False
    
    if not (profile_data.get('city') and len(profile_data['city']) <= 100):
        return False
    
    if not (profile_data.get('state') and profile_data['state'] in [state['value'] for state in get_states()]):
        return False

    if not (profile_data.get('zipcode') and zipcode_pattern.match(profile_data['zipcode'])):
        return False
    
    return True


def get_states():
    # Returns a list of dictionaries containing state abbreviations
    return [
        {"value": "AL"}, {"value": "AK"}, {"value": "AZ"}, {"value": "AR"},
        {"value": "CA"}, {"value": "CO"}, {"value": "CT"}, {"value": "DE"},
        {"value": "FL"}, {"value": "GA"}, {"value": "HI"}, {"value": "ID"},
        {"value": "IL"}, {"value": "IN"}, {"value": "IA"}, {"value": "KS"},
        {"value": "KY"}, {"value": "LA"}, {"value": "ME"}, {"value": "MD"},
        {"value": "MA"}, {"value": "MI"}, {"value": "MN"}, {"value": "MS"},
        {"value": "MO"}, {"value": "MT"}, {"value": "NE"}, {"value": "NV"},
        {"value": "NH"}, {"value": "NJ"}, {"value": "NM"}, {"value": "NY"},
        {"value": "NC"}, {"value": "ND"}, {"value": "OH"}, {"value": "OK"},
        {"value": "OR"}, {"value": "PA"}, {"value": "RI"}, {"value": "SC"},
        {"value": "SD"}, {"value": "TN"}, {"value": "TX"}, {"value": "UT"},
        {"value": "VT"}, {"value": "VA"}, {"value": "WA"}, {"value": "WV"},
        {"value": "WI"}, {"value": "WY"}
    ]