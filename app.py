from flask import Flask, request, jsonify, send_file, send_from_directory
import sqlite3
import qrcode
import os
from io import BytesIO
from flask_cors import CORS
import random
import string
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='Frontend', static_url_path='')
CORS(app)


# Folder to store uploaded photos & QR codes
UPLOAD_FOLDER = 'uploaded_photos'
QR_FOLDER = 'qr_codes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)


# Function to generate a random access token (6 characters)
def generate_access_token(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Route to serve uploaded photos
@app.route('/uploaded_photos/<filename>')
def uploaded_photos(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Route to serve index.html
@app.route('/')
def index():
    return send_file('Frontend/index.html')

# Route to serve slink.html
@app.route('/slink')
def slink():
    return send_file('Static/slink.html')

# Route to add user details
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        # Get form data
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        website = request.form.get('website', None)
        address = request.form.get('address', None)
        job_title = request.form.get('jobTitle')
        x_handle = request.form.get('xHandle', None)
        instagram_handle = request.form.get('instagramHandle', None)
        facebook_handle = request.form.get('facebookHandle', None)
        photo = request.files.get('photo', None)

        # Validate required fields
        if not username or not phone or not email or not job_title:
            return jsonify({"error": "Missing required fields!"}), 400

        # Save the photo if provided
        photo_path = None
        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(UPLOAD_FOLDER, filename)
            photo.save(photo_path)

        access_token = generate_access_token()

        # Insert user into database
        connection = sqlite3.connect("business_card.db")
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users (name, phone, email, website, address, job_title, x_handle, 
            instagram_handle, facebook_handle, photo, access_token) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, phone, email, website, address, job_title, x_handle,
              instagram_handle, facebook_handle, photo_path, access_token))
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()

        return jsonify({"message": "User added successfully!", "user_id": user_id, "access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to edit user details
@app.route('/edit_user', methods=['POST'])
def edit_user():
    try:
        data = request.form
        user_id = data.get('user_id')
        access_token = data.get('access_token')

        # Validate access token
        connection = sqlite3.connect("business_card.db")
        cursor = connection.cursor()
        cursor.execute("SELECT access_token FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if not result or result[0] != access_token:
            connection.close()
            return jsonify({"error": "Invalid access token!"}), 403

        # Update user details
        cursor.execute("""
            UPDATE users SET name = ?, phone = ?, email = ?, website = ?, address = ?, 
            job_title = ?, x_handle = ?, instagram_handle = ?, facebook_handle = ? WHERE id = ?
        """, (data.get('username'), data.get('phone'), data.get('email'), data.get('website'),
              data.get('address'), data.get('jobTitle'), data.get('xHandle'),
              data.get('instagramHandle'), data.get('facebookHandle'), user_id))
        connection.commit()
        connection.close()

        return jsonify({"message": "User updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Generate QR Code API
@app.route('/generate_qr/<int:user_id>', methods=['GET'])
def generate_qr(user_id):
    try:
        connection = sqlite3.connect("business_card.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        connection.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        qr_url = f"http://127.0.0.1:5000/slink?id={user_id}"
        qr = qrcode.make(qr_url)

        qr_path = os.path.join(QR_FOLDER, f"user_{user_id}.png")
        qr.save(qr_path)

        return send_file(qr_path, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Route to fetch user details
@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        connection = sqlite3.connect("business_card.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        connection.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_data = {
            "username": user[1],
            "phone": user[2],
            "email": user[3],
            "website": user[4],
            "address": user[5],
            "job_title": user[6],
            "x_handle": user[7],
            "instagram_handle": user[8],
            "facebook_handle": user[9],
            "photo_url": f"http://127.0.0.1:5000/{user[10]}" if user[10] else None,
            "access_token": user[11]
        }

        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
    
