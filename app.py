from flask import Flask, jsonify, request, render_template, session
from modules.login.login import login_bp
from modules.profile.profile_page import profile_bp 

app = Flask(__name__)
app.config['TESTING'] = True

@app.route('/')
def home():
    return 'Fuel Quote Server is up and running!'

def index():
    if 'logged_in' in session:
        return f"Hello, {session['username']}! You are logged in. <a href='/login/logout'>Logout</a>"
    else:
        return "Welcome! You are not logged in. <a href='/login'>Login</a>"

app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

app.register_blueprint(profile_bp, url_prefix='/profile')