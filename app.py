from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Fuel Quote Server is up and running!'

if __name__ == '__main__':
    app.run(debug=True)
