# Hostel Booking System CLI

A command-line interface for managing hostel bookings with user authentication, room management, and booking operations.

## Features

- **Interactive Menu**: User-friendly menu system for easy navigation
- **User Management**: Create users with secure password authentication
- **Room Management**: Add and manage different room types (single, double, dormitory)
- **Booking System**: Create, view, and cancel bookings with conflict checking
- **Database Storage**: SQLite database for reliable data persistence
- **Currency**: Kenyan Shilling (KSh) pricing
- **Security**: Password hashing and authentication

## Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Quick Start

1. **Interactive Mode (Recommended):**
```bash
./main.py
```
This opens the interactive menu where you can:
- Register new users
- Login and manage bookings
- View available rooms

2. **Setup demo data:**
```bash
python3 main.py setup
```

3. **Command Line Mode:**
```bash
python3 main.py user create
python3 main.py room list
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
- **Brendah Chelugui**: brendachelugui@gmail.com / Chelugui
- **Erasmus Pkoskei**: pkosgei@gmail.com / Chelugui

**70 Rooms Available:**
- 24 Single Rooms (101-124) - KSh 2,500/night
- 23 Double Rooms (201-223) - KSh 4,000/night
- 23 Dormitory Rooms (301-323) - KSh 1,500/night
- **Total Capacity**: 162 people

## Project Structure

```
Hostel_Booking_System/
├── data/                 # SQLite database
│   └── hostel.db        # Main database file
├── models/              # Data models
├── services/            # Business logic
├── utils/               # Helper functions & database
├── main.py             # CLI application
└── requirements.txt    # Dependencies
```

## Room Types & Pricing

- **Single**: 1 person capacity - KSh 2,500/night (24 rooms available)
- **Double**: 2 person capacity - KSh 4,000/night (23 rooms available)
- **Dormitory**: 4 person capacity - KSh 1,500/night (23 rooms available)
- **Total Capacity**: 162 people across 70 rooms

## Technical Features

- **Database**: SQLite for reliable data storage
- **Security**: SHA-256 password hashing
- **Validation**: Email format and password length validation
- **Conflict Detection**: Prevents double-booking of rooms
- **Interactive UI**: Menu-driven interface with table formatting
- **CLI Commands**: Full command-line interface support