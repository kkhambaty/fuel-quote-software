from flask import Flask, jsonify, request, render_template, session, redirect, url_for
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
    # Check if user is logged in
    if 'username' in session:
        return f'Hello, {session["username"]}! <a href="/logout">Logout</a>'
    else:
        return redirect(url_for('login'))

@app.route('/profile-page')
def profile_page():
    return render_template('profilePage.html')

@app.route('/quote-page')
def quote_page():
    return redirect('quote/1')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve username and password from form
        username = request.form['username']
        password = request.form['password']
        
        # Example validation (replace with your actual validation logic)
        if username == 'example_user' and password == 'example_password':
            # Store username in session
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'

    # If GET request, render login form
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    # Clear session data
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5000)
