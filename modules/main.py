# Fuel quote history endpoint
from flask import Flask, jsonify

app = Flask(__name__)

# Mock fuel quote history data
fuel_quote_history = [
    {"Name": "John Doe", "Gallons Requested": 100, "Delivery Address": "123 Lane", "Delivery Date": "3/1/24", "Suggested Price/Gallon": 4.00, "Total Amount Due": 400},
    {"Name": "Jane Doe", "Gallons Requested": 200, "Delivery Address": "123 Main St", "Delivery Date": "3/23/24", "Suggested Price/Gallon": 4.00, "Total Amount Due": 200},
]

@app.route('/fuel_quote_history', methods=['GET'])
def get_fuel_quote_history():
    # Return fuel quote history data
    return jsonify(fuel_quote_history)

# add fuel quote form?

if __name__ == '__main__':
    app.run(debug=True)