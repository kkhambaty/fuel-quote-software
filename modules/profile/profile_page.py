import re
from flask import Blueprint, jsonify, render_template, request
from models import Profile, User
from database import db
profile_bp = Blueprint('profile', __name__)

# profiles = {
#     1: { 'fullName': 'Mohammed Bhai', 'address1': '123 Elm St', 'address2' : 'Suite 200', 'city' : 'San Diego', 'state': 'CA', 'zipcode' : '12345-6789'},
#     2: { 'fullName': 'Clair Boyle', 'address1': '123 Fire St', 'address2' : 'Suite 300', 'city' : 'San Diego', 'state': 'CA', 'zipcode' : '12234-4321'}
# }


@profile_bp.route('/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if request.method == 'GET':
        user_profile = find_profile_by_id(user_id)  # This function would fetch profile data
        if user_profile:
            profile_data = {
                "fullName": user_profile.FullName,
                "address1": user_profile.Address1,
                "address2": user_profile.Address2,
                "city": user_profile.City,
                "state": user_profile.State,
                "zipcode": user_profile.Zipcode,
            }
            response = jsonify(profile_data)
            return response, 200
        else:
            return jsonify({"error": "Profile not found"}), 404
        
    elif request.method == 'POST':
        user_profile = find_profile_by_id(user_id)
        profile_data = request.json    
        if not valid_profile_data(profile_data):
            return jsonify({"error": "Invalid profile data"}), 400   
        if not user_profile:
            # If the profile does not exist, return a 404 error instead of creating a new one
            add_profile(user_id, profile_data)
            return jsonify({"message": "New Profile Created"}), 200 
            # return jsonify({"error": "Profile not found"}), 404

        # if not valid_profile_data(profile_data):
        #     return jsonify({"error": "Invalid profile data"}), 400

        success = update_profile_by_id(user_id, profile_data)
        if success:
            return jsonify({"message": "Profile updated successfully"}), 200
        else:
            # If update fails for reasons other than non-existence, return a generic error message
            return jsonify({"error": "Profile update failed"}), 400


def add_profile(user_id, profile_data):
    new_profile = Profile(
        UserID=user_id,
        FullName=profile_data.get('fullName'), 
        Address1=profile_data.get('address1'),
        Address2=profile_data.get('address2'),
        City=profile_data.get('city'),
        State=profile_data.get('state'),
        Zipcode=profile_data.get('zipcode')
    )
    db.session.add(new_profile)
    db.session.commit()

def find_profile_by_id(user_id):
    profile = Profile.query.filter_by(UserID=user_id).first()
    return profile

def update_profile_by_id(user_id, profile_data):
    profile = Profile.query.filter_by(UserID=user_id).first()
    if profile:
        profile.FullName = profile_data.get('fullName', profile.FullName) 
        profile.Address1 = profile_data.get('address1', profile.Address1)
        profile.Address2 = profile_data.get('address2', profile.Address2)
        profile.City = profile_data.get('city', profile.City)
        profile.State = profile_data.get('state', profile.State)
        profile.Zipcode = profile_data.get('zipcode', profile.Zipcode)
        db.session.commit()
        return True
    else:
        return False
    
# def profile_exists(user_id):
#     return user_id in profiles

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