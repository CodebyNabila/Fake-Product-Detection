from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('regsister.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Load existing user data from the JSON file if it exists
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

    # Check if the username or email already exists
    for user_data in users.values():
        if user_data['username'] == username:
            return jsonify({"error": "Username already exists. Please choose a different username."})
        if user_data['email'] == email:
            return jsonify({"error": "Email address already exists. Please use a different email address."})

    # Add the new user to the dictionary
    users[username] = {'password': password, 'email': email}

    # Save the updated user data to the JSON file
    with open('users.json', 'w') as file:
        json.dump(users, file)
    
    return jsonify({"success": "Registration successful."})

if __name__ == '__main__':
    app.run(debug=True)
