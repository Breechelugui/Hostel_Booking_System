from models.room import Room, RoomType
from utils.helpers import load_json_data, save_json_data, get_next_id

class RoomService:
    def __init__(self, data_file='data/rooms.json'):
        self.data_file = data_file
    
    def create_room(self, number, room_type, capacity, price_per_night):
        """Create a new room"""
        rooms_data = load_json_data(self.data_file)
        
        # Check if room number already exists
        if any(room['number'] == number for room in rooms_data):
            raise ValueError("Room number already exists")
        
        room_id = get_next_id(rooms_data)
        room = Room(room_id, number, RoomType(room_type), capacity, price_per_night)
        
        rooms_data.append(room.to_dict())
        save_json_data(self.data_file, rooms_data)
        
        return room
    
    def get_room_by_id(self, room_id):
        """Get room by ID"""
        rooms_data = load_json_data(self.data_file)
        room_data = next((room for room in rooms_data if room['id'] == room_id), None)
        return Room.from_dict(room_data) if room_data else None
    
    def list_available_rooms(self):
        """List all available rooms"""
        rooms_data = load_json_data(self.data_file)
        return [Room.from_dict(room) for room in rooms_data if room['is_available']]
    
    def list_all_rooms(self):
        """List all rooms"""
        rooms_data = load_json_data(self.data_file)
        return [Room.from_dict(room) for room in rooms_data]
    
    def update_room_availability(self, room_id, is_available):
        """Update room availability"""
        rooms_data = load_json_data(self.data_file)
        
        for room in rooms_data:
            if room['id'] == room_id:
                room['is_available'] = is_available
                save_json_data(self.data_file, rooms_data)
                return True
        return False