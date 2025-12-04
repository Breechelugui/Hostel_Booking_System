from dataclasses import dataclass
from typing import Optional
import hashlib

@dataclass
class User:
    id: int
    name: str
    email: str
    phone: str
    password_hash: str
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'password_hash': self.password_hash
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password_hash=data['password_hash']
        )
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        return self.password_hash == self.hash_password(password)