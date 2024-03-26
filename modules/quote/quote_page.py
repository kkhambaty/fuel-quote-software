from flask import flash, Blueprint, render_template, request, redirect, url_for, session


quote_bp = Blueprint('quote', __name__)

#The quote form is meant to retrieve the delivery address from the user's profile information from a Database.
#These sample profiles are here as substitutes to represent information from a Database for the time being
retrieved_profile = {
    1: { 'fullName': 'John Doe', 'address1': '123 Elm St', 'address2' : 'Suite 200', 'city' : 'San Diego', 'state': 'CA', 'zipcode' : '12345-6789'},
    2: { 'fullName': 'Clair Boyle', 'address1': '123 Fire St', 'address2' : 'Suite 300', 'city' : 'San Diego', 'state': 'CA', 'zipcode' : '12234-4321'}
}
#This pricing rate is a substitute as well until the pricing module is created
pricing_rate = {
    1: { 'rate': '4.00'},
    2: { 'rate': '3.00'}
}

@quote_bp.route('/<int:user_id>', methods=['GET', 'POST'])
def quoteForm(user_id):
    #An example case where a user_id does not exist
    if user_id != 1 and user_id != 2:
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
            return render_template('fuelQuoteForm.html', user=user_id, result=result, userAddr=userAddr, rate=rate), 200


def getUserAddr(user_id):
    return retrieved_profile[user_id]['address1'] + " " + retrieved_profile[user_id]['address2']

def getPricingRate(user_id):
    return pricing_rate[user_id]['rate']
