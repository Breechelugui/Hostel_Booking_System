import json
import os
from datetime import datetime

def load_json_data(file_path):
    """Load data from JSON file"""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_json_data(file_path, data):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def get_next_id(items):
    """Get next available ID"""
    if not items:
        return 1
    return max(item['id'] for item in items) + 1

def parse_date(date_str):
    """Parse date string to datetime object"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

def validate_email(email):
    """Basic email validation"""
    return '@' in email and '.' in email.split('@')[1]