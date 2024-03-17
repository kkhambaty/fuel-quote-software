from flask import Flask, jsonify, request
from modules.profile import profile_bp 

app = Flask(__name__)

@app.route('/')
def home():
    return 'Fuel Quote Server is up and running!'

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

app.register_blueprint(profile_bp, url_prefix='/profile')