import os
import sqlite3
import uuid
import datetime
import jwt
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set configuration options for the app
app.config['UPLOAD_FOLDER'] = 'uploads' # Directory for uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Maximum file size allowed
app.config['JWT_SECRET_KEY'] = 'YOUR_KEY' # Secret key for JWT tokens
app.config['JWT_ALGORITHM'] = 'HS256' # Algorithm used for JWT tokens
app.config['DATABSE'] = 'database.db' # Database filename
app.config['BASE_URL'] = 'YOUR_SITE' # Site URL 

# Connect to the database
conn = sqlite3.connect(app.config['DATABSE'])

# Create a cursor
cursor = conn.cursor()

# Create a table if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        auth_token TEXT
    )
""")
conn.commit()

# Verify a JWT token
def verify_jwt(jwt_token):
    try:
        decoded_payload = jwt.decode(jwt_token, app.config['JWT_SECRET_KEY'], algorithms=[app.config['JWT_ALGORITHM']])
        return decoded_payload
    except jwt.exceptions.InvalidSignatureError:
        # Signature verification failed
        return None
    except jwt.exceptions.ExpiredSignatureError:
        # Token has expired
        return None

# Handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if request has a valid JWT token
    auth_token = request.headers.get('Authorization')
    token = str.replace(str(auth_token), 'Bearer ', '')
    if token is None:
        return jsonify({'error': 'Missing authorization token'}), 401

    decoded_payload = verify_jwt(token)
    if decoded_payload is None:
        return jsonify({'error': 'Invalid or expired authorization token'}), 401

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    # Check if the file extension is allowed
    allowed_extensions = {'mp4', 'mov', 'avi'}
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        # Generate a unique filename and save the file
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1]
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = app.config['BASE_URL'] +'/'+ app.config['UPLOAD_FOLDER']+'/' + filename
        # Return the filename to the client
        return jsonify({'file_url': file_url}), 200
    else:
        return jsonify({'error': 'Invalid file extension'}), 400

if __name__ == '__main__':
    app.run(debug=True)
