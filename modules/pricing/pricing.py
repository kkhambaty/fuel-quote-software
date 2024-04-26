from flask import flash, Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import Profile, FuelQuoteForm
from database import db


pricing_bp = Blueprint('pricing', __name__)

@pricing_bp.route('/<int:user_id>', methods=['GET', 'POST'])
def pricingModule(user_id):
        requested_gallons = float(request.form['gallons'])
        current_price_per_gallon = 1.50
        location_factor = 0.02 if getUserState(user_id).lower() == 'tx' else 0.04
        rate_history_factor = 0.01 if has_previous_quotes(user_id) else 0
        gallons_requested_factor = 0.02 if requested_gallons > 1000 else 0.03
        company_profit_factor = 0.10
        margin = current_price_per_gallon * (location_factor - rate_history_factor + gallons_requested_factor + company_profit_factor)
        suggested_price_per_gallon = 1.50 + margin
        total_due = requested_gallons * suggested_price_per_gallon
        # due = float(request.form['gallons']) * float(request.form['pricing'])
        format_num = "{:.2f}".format(total_due)
        return jsonify({
        'pricing_rate': suggested_price_per_gallon,
        'total_due': total_due
        })
 


def getUserState(user_id):
    user_profile = Profile.query.filter_by(UserID=user_id).first()
    # If a profile exists, return the state, otherwise return None or a default value
    return user_profile.State if user_profile else None

def has_previous_quotes(user_id):
    previous_quotes = FuelQuoteForm.query.filter_by(UserID=user_id).first()
    # If any previous quotes exist, return True, otherwise return False
    return True if previous_quotes else False


