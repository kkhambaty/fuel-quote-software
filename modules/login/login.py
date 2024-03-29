from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock user data (replace this with a database later)
users = {
    'user1': {'username': 'user1', 'password': 'password1'},
    'user2': {'username': 'user2', 'password': 'password2'}
}

# Login route with validations
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Validate required fields
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Validate field lengths
    if len(username) > 50 or len(password) > 50:
        return jsonify({'error': 'Username and password must be less than 50 characters long'}), 400
    
    # Validate field types (assuming strings for username and password)
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({'error': 'Username and password must be strings'}), 400
    
    # Perform authentication
    if username in users and users[username]['password'] == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)