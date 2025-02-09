from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Health check endpoint for AWS ALB
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Temporary in-memory user store for POC purposes
users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    if email in users:
        return jsonify({'message': 'User already exists'}), 400
    
    users[email] = {
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'password': data.get('password')
    }
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = users.get(email)
    if user and user['password'] == password:
        return jsonify({'message': 'Login successful', 'user': email}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
