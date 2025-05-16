import os
import json
from datetime import datetime
from services.file_service import load_json, save_json
from hashlib import sha256

def hash_password(password: str) -> str:
    return sha256(password.encode('utf-8')).hexdigest()

def register_user(username, password, firstname='', lastname='', email='', phone='', birthdate='', users_file='static/resources/users.json'):
    users = load_json(users_file) or []

    if any(u['username'].lower() == username.lower() for u in users):
        return "Username already exists"

    if not username or not password:
        return "Username and password are required"

    user = {
        'username': username,
        'password': hash_password(password),
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'phone': phone,
        'birthdate': birthdate,
        'registered_at': str(datetime.now())
    }

    users.append(user)
    save_json(users_file, users)
    return None

def authenticate_user(username, password, users_file='static/resources/users.json'):
    users = load_json(users_file) or []
    hashed = hash_password(password)

    for user in users:
        if user['username'].lower() == username.lower() and user['password'] == hashed:
            return True
    return False