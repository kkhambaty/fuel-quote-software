from flask import flash, Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import Profile, FuelQuoteForm
from database import db


quote_bp = Blueprint('quote', __name__)

#This pricing rate is a substitute until the pricing module is created
pricing_rate = {
    1: { 'rate': '4.00'}
}

@quote_bp.route('/<int:user_id>', methods=['GET', 'POST'])
def quoteForm(user_id):
    #An example case where a user_id does not exist
    if not user_id:
        return 'User ID does not exist or is not recognized', 404
    userAddr = getUserAddr(user_id)
    rate = getPricingRate(user_id)
    #Case where the quote form is correctly rendered with the user's profile address and current fuel rate
    if request.method == 'GET':
        return render_template('fuelQuoteForm.html', user=user_id, userAddr=userAddr, rate=rate), 200
    elif request.method == 'POST':
        #Case where the form is submitted with invalid fields. A flash message is displayed to notify the user
        if (not request.form['gallons'] or float(request.form['gallons']) <= 0) or (not request.form['address']) or (not request.form['delivery']) or (not request.form['pricing'] or float(request.form['pricing']) <= 0.00):
            flash('ERROR: Missing or invalid form data. Quote not generated.', 'error')
            return render_template('fuelQuoteForm.html', user=user_id, userAddr=userAddr, rate=rate), 400
        else:
        #Case where the form is valid and a quote is generated. The quote will be stored in the Database when it is finally implemented
            due = float(request.form['gallons']) * float(request.form['pricing'])
            format_num = "{:.2f}".format(due)
            result = "Total amount due: $" + str(format_num)
            new_quote = FuelQuoteForm(
                UserID = user_id,
                GallonsRequested = request.form['gallons'],
                DeliveryAddress = request.form['address'],
                DeliveryDate = request.form['delivery'],
                PricePerGallon = rate,
                TotalAmountDue = format_num
            )
            db.session.add(new_quote)
            db.session.commit()
            return render_template('fuelQuoteForm.html', user=user_id, result=result, userAddr=userAddr, rate=rate), 200
        
@quote_bp.route('/fuelQuoteHistory', methods=['GET'])
def get_fuel_quote_history():
    # query database to retrieve fuel quote history data
    fuel_quote_history = FuelQuoteForm.query.all()

    # check if there is any data retrieved 
    if not fuel_quote_history:
        return render_template('fuelQuoteHistory.html', fuelQuoteHistory=[])
    
    # pass the fuel quote history to the template
    return render_template('fuelQuoteHistory.html', fuel_quote_history=fuel_quote_history)

def getUserAddr(user_id):
    retrieved_profile = Profile.query.filter_by(UserID=user_id).first()
    return retrieved_profile.Address1 + " " + retrieved_profile.Address2 + " " + retrieved_profile.City + ", " + retrieved_profile.State + " " + retrieved_profile.Zipcode

def getPricingRate(user_id):
    return pricing_rate[user_id]['rate']
