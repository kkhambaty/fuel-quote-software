from flask import Flask, flash, jsonify, request, render_template, session, redirect, url_for
from modules.login.login import login_bp
from modules.profile.profile_page import profile_bp 
from modules.quote.quote_page import quote_bp
from flask_sqlalchemy import SQLAlchemy
from database import db
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import User
import logging
# from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)

# new mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password123@localhost/fuelQuoteAppData'
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
app.config['TESTING'] = True
# app.secret_key = 'frenchfries'
# app(CORS)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(quote_bp, url_prefix='/quote')
app.register_blueprint(login_bp)

@app.route('/home')
@login_required
def home():
    # Check if user is logged in
    if current_user.is_authenticated:
        return render_template('homepage.html', username=current_user.username)
    # return render_template('homepage.html', username='123445')
    else:
        return redirect(url_for('login'))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/profile-page')
@login_required
def profile_page():
    print("Rendering profilePage.html for user_id:", current_user.ID)
    return render_template('profilePage.html', user_id=current_user.ID)

@app.route('/quote-page')
@login_required
def quote_page():
    return redirect('quote')

@app.route('/logi', methods=['GET','POST'])
def login():
    # print("hello")
    print(request.method)
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        print("bello")
        # username = request.get_json('username')
        # password = request.get_json('password')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        print("username: ", username)
        print("user: ", str(user))
        print("password: ", password)
        
        if bcrypt.check_password_hash(user.password, password):
            # Logic to log the user in
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # else:
        #     return 'Invalid username or password'
    
    # If GET request, render login form
    

# @app.route('/logi', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
        
#         user = User.query.filter_by(username=username).first()
        
#         if user and bcrypt.check_password_hash(user.password, password):
#             # Logic to log the user in
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
    
#     return render_template('index.html')

@app.route('/logout', methods=['POST'])
def logout():
    # Clear session data
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login')) # May need to make this homepage.html

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # data = request.get_json()
        username = request.form.get('username')
        password = request.form.get('password')
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_exists = User.query.filter_by(username=username).first() is not None
        if user_exists:
            return "Username already exists. Please choose a different one." #, render_template('index.html')
        # Store the username and hashed password in the users dictionary
        # users[username] = hashed_password # Shouldn't this be adding to the db?
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        db.session.rollback()
        
        return redirect(url_for('login')) # Might need to make this index? Registration and login are both in index

    # If GET request, render registration form which is in index.html
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5000)
