from models.room import Room, RoomType
from utils.database import Database

class RoomService:
    def __init__(self):
        self.db = Database()
    
    def create_room(self, number, room_type, capacity, price_per_night):
        """Create a new room"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Check if room number already exists
        cursor.execute("SELECT id FROM rooms WHERE number = ?", (number,))
        if cursor.fetchone():
            conn.close()
            raise ValueError("Room number already exists")
        
        cursor.execute(
            "INSERT INTO rooms (number, room_type, capacity, price_per_night) VALUES (?, ?, ?, ?)",
            (number, room_type, capacity, price_per_night)
        )
        room_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return Room(room_id, number, RoomType(room_type), capacity, price_per_night)
    
    def get_room_by_id(self, room_id):
        """Get room by ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Room(row[0], row[1], RoomType(row[2]), row[3], row[4], bool(row[5]))
        return None
    
    def list_available_rooms(self):
        """List all available rooms"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE is_available = 1")
        rows = cursor.fetchall()
        conn.close()
        
        return [Room(row[0], row[1], RoomType(row[2]), row[3], row[4], bool(row[5])) for row in rows]
    
    def list_all_rooms(self):
        """List all rooms"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms")
        rows = cursor.fetchall()
        conn.close()
        
        return [Room(row[0], row[1], RoomType(row[2]), row[3], row[4], bool(row[5])) for row in rows]
    
    def update_room_availability(self, room_id, is_available):
        """Update room availability"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE rooms SET is_available = ? WHERE id = ?", (is_available, room_id))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0