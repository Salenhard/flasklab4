from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.json.ensure_ascii = False

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'student':
        return 'dvfu'
    return None

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

if __name__ == '__main__':
    app.run(debug=True)

import structures.views


