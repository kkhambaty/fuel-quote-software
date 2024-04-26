from flask import flash, Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import Profile, FuelQuoteForm
from database import db


quote_bp = Blueprint('quote', __name__)


@quote_bp.route('/<int:user_id>', methods=['GET', 'POST'])
def quoteForm(user_id):
    #An example case where a user_id does not exist
    if not user_id:
        return 'User ID does not exist or is not recognized', 404
    userAddr = getUserAddr(user_id)
    #Case where the quote form is correctly rendered with the user's profile address and current fuel rate
    if request.method == 'GET':
        return render_template('fuelQuoteForm.html', user=user_id, userAddr=userAddr), 200
    elif request.method == 'POST':
        #Case where the form is submitted with invalid fields. A flash message is displayed to notify the user
        # if (not request.form['gallons'] or float(request.form['gallons']) <= 0) or (not request.form['address']) or (not request.form['delivery']) or (not request.form['pricing'] or float(request.form['pricing']) <= 0.00):
        if (not request.form['gallons'] or float(request.form['gallons']) <= 0) or (not request.form['address']) or (not request.form['delivery']):
            flash('ERROR: Missing or invalid form data. Quote not generated.', 'error')
            return render_template('fuelQuoteForm.html', user=user_id, userAddr=userAddr), 400
        else:
        #Case where the form is valid and a quote is generated. The quote will be stored in the Database when it is finally implemented
            new_quote = FuelQuoteForm(
                UserID = user_id,
                GallonsRequested = request.form['gallons'],
                DeliveryAddress = request.form['address'],
                DeliveryDate = request.form['delivery'],
                PricePerGallon = request.form['pricing'],
                TotalAmountDue = request.form['totalAmount']
            )
            db.session.add(new_quote)
            db.session.commit()
            return render_template('fuelQuoteForm.html', user=user_id, result=request.form['totalAmount'], userAddr=request.form['address'], suggested_price_per_gallon=request.form['pricing']), 200

        
@quote_bp.route('/fuelQuoteHistory/<int:user_id>', methods=['GET'])
def get_fuel_quote_history(user_id):
    # query database to retrieve fuel quote history data
    fuel_quote_history = FuelQuoteForm.query.filter_by(UserID=user_id).all()

    # check if there is any data retrieved 
    if not fuel_quote_history:
        return render_template('fuelQuoteHistory.html', fuel_quote_history=[])
    
    # pass the fuel quote history to the template
    return render_template('fuelQuoteHistory.html', fuel_quote_history=fuel_quote_history)

def getUserAddr(user_id):
    retrieved_profile = Profile.query.filter_by(UserID=user_id).first()
    if not retrieved_profile:
        flash('You must create your profile before requesting a fuel quote')
        return render_template('profilePage.html', user_id=user_id)
    return retrieved_profile.Address1 + " " + retrieved_profile.Address2 + " " + retrieved_profile.City + ", " + retrieved_profile.State + " " + retrieved_profile.Zipcode

