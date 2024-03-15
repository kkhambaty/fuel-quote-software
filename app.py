from flask import Flask, jsonify, request, render_template
from login.login import login_bp

app = Flask(__name__)

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
    app.run(debug=True)
