from models.user import User
from utils.helpers import load_json_data, save_json_data, get_next_id, validate_email

class UserService:
    def __init__(self, data_file='data/users.json'):
        self.data_file = data_file
    
    def create_user(self, name, email, phone, password):
        """Create a new user"""
        if not validate_email(email):
            raise ValueError("Invalid email format")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        users_data = load_json_data(self.data_file)
        
        # Check if email already exists
        if any(user['email'] == email for user in users_data):
            raise ValueError("Email already exists")
        
        user_id = get_next_id(users_data)
        password_hash = User.hash_password(password)
        user = User(user_id, name, email, phone, password_hash)
        
        users_data.append(user.to_dict())
        save_json_data(self.data_file, users_data)
        
        return user
    
    def authenticate_user(self, email, password):
        """Authenticate user with email and password"""
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        users_data = load_json_data(self.data_file)
        user_data = next((user for user in users_data if user['id'] == user_id), None)
        return User.from_dict(user_data) if user_data else None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        users_data = load_json_data(self.data_file)
        user_data = next((user for user in users_data if user['email'] == email), None)
        return User.from_dict(user_data) if user_data else None
    
    def list_users(self):
        """List all users"""
        users_data = load_json_data(self.data_file)
        return [User.from_dict(user) for user in users_data]