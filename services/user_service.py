from models.user import User
from utils.database import Database
from utils.helpers import validate_email

class UserService:
    def __init__(self):
        self.db = Database()
    
    def create_user(self, name, email, phone, password):
        """Create a new user"""
        if not validate_email(email):
            raise ValueError("Invalid email format")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            raise ValueError("Email already exists")
        
        password_hash = User.hash_password(password)
        cursor.execute(
            "INSERT INTO users (name, email, phone, password_hash) VALUES (?, ?, ?, ?)",
            (name, email, phone, password_hash)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return User(user_id, name, email, phone, password_hash)
    
    def authenticate_user(self, email, password):
        """Authenticate user with email and password"""
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(row[0], row[1], row[2], row[3], row[4])
        return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(row[0], row[1], row[2], row[3], row[4])
        return None
    
    def list_users(self):
        """List all users"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        
        return [User(row[0], row[1], row[2], row[3], row[4]) for row in rows]