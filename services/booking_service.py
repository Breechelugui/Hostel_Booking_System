from datetime import datetime
from models.booking import Booking, BookingStatus
from services.room_service import RoomService
from services.user_service import UserService
from utils.helpers import load_json_data, save_json_data, get_next_id

class BookingService:
    def __init__(self, data_file='data/bookings.json'):
        self.data_file = data_file
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
        
        bookings_data = load_json_data(self.data_file)
        booking_id = get_next_id(bookings_data)
        
        booking = Booking(booking_id, user_id, room_id, check_in, check_out, total_price)
        
        bookings_data.append(booking.to_dict())
        save_json_data(self.data_file, bookings_data)
        
        return booking
    
    def _has_conflicting_booking(self, room_id, check_in, check_out):
        """Check if there are conflicting bookings"""
        bookings_data = load_json_data(self.data_file)
        
        for booking_data in bookings_data:
            if (booking_data['room_id'] == room_id and 
                booking_data['status'] == BookingStatus.CONFIRMED.value):
                
                existing_checkin = datetime.fromisoformat(booking_data['check_in'])
                existing_checkout = datetime.fromisoformat(booking_data['check_out'])
                
                # Check for overlap
                if not (check_out <= existing_checkin or check_in >= existing_checkout):
                    return True
        return False
    
    def cancel_booking(self, booking_id):
        """Cancel a booking"""
        bookings_data = load_json_data(self.data_file)
        
        for booking in bookings_data:
            if booking['id'] == booking_id:
                booking['status'] = BookingStatus.CANCELLED.value
                save_json_data(self.data_file, bookings_data)
                return True
        return False
    
    def get_booking_by_id(self, booking_id):
        """Get booking by ID"""
        bookings_data = load_json_data(self.data_file)
        booking_data = next((booking for booking in bookings_data if booking['id'] == booking_id), None)
        return Booking.from_dict(booking_data) if booking_data else None
    
    def get_user_bookings(self, user_id):
        """Get all bookings for a user"""
        bookings_data = load_json_data(self.data_file)
        user_bookings = [booking for booking in bookings_data if booking['user_id'] == user_id]
        return [Booking.from_dict(booking) for booking in user_bookings]
    
    def list_all_bookings(self):
        """List all bookings"""
        bookings_data = load_json_data(self.data_file)
        return [Booking.from_dict(booking) for booking in bookings_data]