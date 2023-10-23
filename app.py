from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)


def connect_db():
    return sqlite3.connect('my_database.db')

conn = connect_db()
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        email VARCHAR(20) NOT NULL,
        password VARCHAR(20) NOT NULL,
        chats VARCHAR(1000),
        joined TIMESTAMP
    )
''')
conn.commit()

@app.route('/')
def home():
    return "It's Working"

@app.route('/signin', methods=['POST'])
def signin():
    conn = connect_db()
    cursor = conn.cursor()
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor.execute('SELECT * FROM users WHERE email=?', (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        user_data = {
            'id': user[0],
            'name': user[1],
            'email': user[2]
        }
        return jsonify(user_data)
    else:
        return 'Error logging in', 400

@app.route('/register', methods=['POST'])
def register():
    conn = connect_db()
    cursor = conn.cursor()
    
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    cursor.execute('SELECT * FROM users WHERE email=?', (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return 'The email has already been used'

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_id = str(uuid.uuid4())

    cursor.execute('''
        INSERT INTO users (id, name, email, password, chats, joined)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, name, email, hashed_password.decode('utf-8'), '', datetime.now()))
    conn.commit()

    cursor.execute('SELECT * FROM users WHERE email=?', (email,))
    user = cursor.fetchone()

    user_data = {
        'id': user[0],
        'name': user[1],
        'email': user[2]
    }

    return jsonify(user_data)

@app.route('/chatbot', methods=['PUT'])
def chatbot():
    conn = connect_db()
    cursor = conn.cursor()
    
    data = request.get_json()
    user_id = data.get('id')
    chat = data.get('chat')

    cursor.execute('UPDATE users SET chats = ? WHERE id = ?', (chat, user_id))
    conn.commit()

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        user_data = {
            'id': user[0],
            'name': user[1],
            'email': user[2]
        }
        return jsonify(user_data)
    else:
        return 'User not found', 400

@app.route('/profile/<string:user_id>', methods=['GET'])
def profile(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        user_data = {
            'id': user[0],
            'name': user[1],
            'email': user[2]
        }
        return jsonify(user_data)
    else:
        return 'User not found', 400

if __name__ == '__main__':
    app.run(debug=True)
