from datetime import datetime
from models.booking import Booking, BookingStatus
from services.room_service import RoomService
from services.user_service import UserService
from utils.database import Database

class BookingService:
    def __init__(self):
        self.db = Database()
        self.room_service = RoomService()
        self.user_service = UserService()
    
    def create_booking(self, user_id, room_id, check_in, check_out):
        """Create a new booking"""
        # Validate user and room exist
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        room = self.room_service.get_room_by_id(room_id)
        if not room:
            raise ValueError("Room not found")
        
        if not room.is_available:
            raise ValueError("Room is not available")
        
        # Validate dates
        if check_in >= check_out:
            raise ValueError("Check-out date must be after check-in date")
        
        if check_in < datetime.now():
            raise ValueError("Check-in date cannot be in the past")
        
        # Check for conflicting bookings
        if self._has_conflicting_booking(room_id, check_in, check_out):
            raise ValueError("Room is already booked for these dates")
        
        # Calculate total price
        nights = (check_out - check_in).days
        total_price = nights * room.price_per_night
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (user_id, room_id, check_in, check_out, total_price) VALUES (?, ?, ?, ?, ?)",
            (user_id, room_id, check_in.isoformat(), check_out.isoformat(), total_price)
        )
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return Booking(booking_id, user_id, room_id, check_in, check_out, total_price)
    
    def _has_conflicting_booking(self, room_id, check_in, check_out):
        """Check if there are conflicting bookings"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT check_in, check_out FROM bookings WHERE room_id = ? AND status = 'confirmed'",
            (room_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            existing_checkin = datetime.fromisoformat(row[0])
            existing_checkout = datetime.fromisoformat(row[1])
            
            # Check for overlap
            if not (check_out <= existing_checkin or check_in >= existing_checkout):
                return True
        return False
    
    def cancel_booking(self, booking_id):
        """Cancel a booking"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET status = 'cancelled' WHERE id = ?", (booking_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0
    
    def get_booking_by_id(self, booking_id):
        """Get booking by ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Booking(
                row[0], row[1], row[2],
                datetime.fromisoformat(row[3]),
                datetime.fromisoformat(row[4]),
                row[5], BookingStatus(row[6])
            )
        return None
    
    def get_user_bookings(self, user_id):
        """Get all bookings for a user"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Booking(
            row[0], row[1], row[2],
            datetime.fromisoformat(row[3]),
            datetime.fromisoformat(row[4]),
            row[5], BookingStatus(row[6])
        ) for row in rows]
    
    def list_all_bookings(self):
        """List all bookings"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        rows = cursor.fetchall()
        conn.close()
        
        return [Booking(
            row[0], row[1], row[2],
            datetime.fromisoformat(row[3]),
            datetime.fromisoformat(row[4]),
            row[5], BookingStatus(row[6])
        ) for row in rows]