# Hostel Booking System CLI

A command-line interface for managing hostel bookings with user authentication, room management, and booking operations.

## Features

- **User Management**: Create users with secure password authentication
- **Room Management**: Add and manage different room types (single, double, dormitory)
- **Booking System**: Create, view, and cancel bookings with conflict checking
- **Data Persistence**: JSON file storage for all data
- **Security**: Password hashing and authentication

## Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Quick Start

1. **Setup demo data:**
```bash
python3 main.py setup
```

2. **Create a user:**
```bash
python3 main.py user create
```

3. **Login:**
```bash
python3 main.py user login
```

## Commands

### User Commands
```bash
python3 main.py user create          # Create new user
python3 main.py user login           # Login user
python3 main.py user list            # List all users
```

### Room Commands
```bash
python3 main.py room create          # Create new room
python3 main.py room list            # List all rooms
python3 main.py room list --available-only  # List available rooms only
```

### Booking Commands
```bash
python3 main.py booking create       # Create new booking
python3 main.py booking list         # List all bookings
python3 main.py booking list --user-id 1    # List bookings for specific user
python3 main.py booking details --booking-id 1  # Show booking details
python3 main.py booking cancel --booking-id 1   # Cancel booking
```

## Demo Data

After running `python3 main.py setup`, you can login with:
- **John Doe**: john@example.com / password123
- **Jane Smith**: jane@example.com / password456

## Project Structure

```
Hostel_Booking_System/
├── data/                 # JSON data files
├── models/              # Data models
├── services/            # Business logic
├── utils/               # Helper functions
├── main.py             # CLI application
└── requirements.txt    # Dependencies
```

## Room Types

- **Single**: 1 person capacity
- **Double**: 2 person capacity  
- **Dormitory**: 4+ person capacity

## Security

- Passwords are hashed using SHA-256
- Minimum 6 character password requirement
- Hidden password input during registration/login