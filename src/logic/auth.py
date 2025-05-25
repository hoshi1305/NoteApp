import json
import os
from config import USER_FILE

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def check_login(email, password):
    users = load_users()
    return email in users and users[email] == password

def register_user(email, password):
    users = load_users()
    if email in users:
        return False
    users[email] = password
    save_users(users)
    return True