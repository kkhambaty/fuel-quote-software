from flask import Flask, jsonify, request, render_template, session, redirect
from modules.login.login import login_bp
from modules.profile.profile_page import profile_bp 
from modules.quote.quote_page import quote_bp
from flask_sqlalchemy import SQLAlchemy
from database import db
import logging
# from flask_cors import CORS

app = Flask(__name__)
# new mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password123@localhost/fuelQuoteAppData'
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
app.config['TESTING'] = True
app.secret_key = 'frenchfries'
# app(CORS)

app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(quote_bp, url_prefix='/quote')
app.register_blueprint(login_bp)

@app.route('/')
def home():
    return 'Fuel Quote Server is up and running!'

@app.route('/profile-page')
def profile_page():
    return render_template('profilePage.html')

@app.route('/quote-page')
def quote_page():
    return redirect('quote/1')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5000)
