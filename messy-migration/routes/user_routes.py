from flask import Blueprint, request, jsonify
from passlib.hash import pbkdf2_sha256
from db import get_db
import sqlite3

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def home():
    return "User Management System"

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    db = get_db()
    users = db.execute("SELECT id, name, email FROM users").fetchall()
    return jsonify([dict(u) for u in users]), 200

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    user = db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    if user:
        return jsonify(dict(user)), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not all([name, email, password]):
        return jsonify({'error': 'Missing fields'}), 400
    db = get_db()
    try:
        db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                   (name, email, pbkdf2_sha256.hash(password)))
        db.commit()
        return jsonify({'message': 'User created'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User already exists'}), 409

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(force=True)
    name = data.get('name')
    email = data.get('email')
    if not all([name, email]):
        return jsonify({'error': 'Missing fields'}), 400
    db = get_db()
    result = db.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    db.commit()
    if result.rowcount:
        return jsonify({'message': 'User updated'}), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    result = db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    if result.rowcount:
        return jsonify({'message': f'User {user_id} deleted'}), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Please provide a name to search'}), 400
    db = get_db()
    users = db.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f'%{name}%',)).fetchall()
    return jsonify([dict(u) for u in users]), 200

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    email = data.get('email')
    password = data.get('password')
    if not all([email, password]):
        return jsonify({'status': 'failed', 'error': 'Missing credentials'}), 400
    db = get_db()
    user = db.execute("SELECT id, password FROM users WHERE email = ?", (email,)).fetchone()
    if user and pbkdf2_sha256.verify(password, user['password']):
        return jsonify({'status': 'success', 'user_id': user['id']}), 200
    return jsonify({'status': 'failed'}), 401 