from dataclasses import dataclass
from enum import Enum

class RoomType(Enum):
    SINGLE = "single"
    DOUBLE = "double"
    DORMITORY = "dormitory"

@dataclass
class Room:
    id: int
    number: str
    room_type: RoomType
    capacity: int
    price_per_night: float
    is_available: bool = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'room_type': self.room_type.value,
            'capacity': self.capacity,
            'price_per_night': self.price_per_night,
            'is_available': self.is_available
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            number=data['number'],
            room_type=RoomType(data['room_type']),
            capacity=data['capacity'],
            price_per_night=data['price_per_night'],
            is_available=data['is_available']
        )