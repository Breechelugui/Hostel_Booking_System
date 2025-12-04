from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class BookingStatus(Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

@dataclass
class Booking:
    id: int
    user_id: int
    room_id: int
    check_in: datetime
    check_out: datetime
    total_price: float
    status: BookingStatus = BookingStatus.CONFIRMED
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'room_id': self.room_id,
            'check_in': self.check_in.isoformat(),
            'check_out': self.check_out.isoformat(),
            'total_price': self.total_price,
            'status': self.status.value
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            room_id=data['room_id'],
            check_in=datetime.fromisoformat(data['check_in']),
            check_out=datetime.fromisoformat(data['check_out']),
            total_price=data['total_price'],
            status=BookingStatus(data['status'])
        )