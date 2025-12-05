#!/usr/bin/env python3

import click
import sys
from datetime import datetime
from tabulate import tabulate
from services.user_service import UserService
from services.room_service import RoomService
from services.booking_service import BookingService
from models.room import RoomType
from utils.helpers import parse_date

# Initialize services
user_service = UserService()
room_service = RoomService()
booking_service = BookingService()

# Global variable to store current user
current_user = None

def show_main_menu():
    """Show the main interactive menu"""
    while True:
        click.echo("\n=== HOSTEL BOOKING SYSTEM ===")
        click.echo("1. Register")
        click.echo("2. Login")
        click.echo("3. Exit")
        
        choice = click.prompt("Choose", type=int)
        
        if choice == 1:
            register_user()
        elif choice == 2:
            if login_user():
                show_user_menu()
        elif choice == 3:
            click.echo("Goodbye!")
            sys.exit(0)
        else:
            click.echo("Invalid choice. Please try again.")

def register_user():
    """Register a new user"""
    try:
        name = click.prompt('Name')
        email = click.prompt('Email')
        phone = click.prompt('Phone')
        password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
        
        user = user_service.create_user(name, email, phone, password)
        click.echo(f"✅ User registered successfully! ID: {user.id}")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")

def login_user():
    """Login user"""
    global current_user
    email = click.prompt('Email')
    password = click.prompt('Password', hide_input=True)
    
    user = user_service.authenticate_user(email, password)
    if user:
        current_user = user
        click.echo(f"✅ Login successful! Welcome, {user.name}")
        return True
    else:
        click.echo("❌ Invalid email or password")
        return False

def show_user_menu():
    """Show user menu after login"""
    while True:
        click.echo(f"\n=== WELCOME {current_user.name.upper()} ===")
        click.echo("1. View Available Rooms")
        click.echo("2. Make Booking")
        click.echo("3. View My Bookings")
        click.echo("4. Cancel Booking")
        click.echo("5. Logout")
        
        choice = click.prompt("Choose", type=int)
        
        if choice == 1:
            view_available_rooms()
        elif choice == 2:
            make_booking()
        elif choice == 3:
            view_my_bookings()
        elif choice == 4:
            cancel_my_booking()
        elif choice == 5:
            click.echo("Logged out successfully!")
            break
        else:
            click.echo("Invalid choice. Please try again.")

def view_available_rooms():
    """View available rooms"""
    rooms = room_service.list_available_rooms()
    if not rooms:
        click.echo("No available rooms.")
        return
    
    table_data = [[r.id, r.number, r.room_type.value, r.capacity, f"KSh {r.price_per_night:.0f}"] for r in rooms]
    click.echo(tabulate(table_data, headers=['ID', 'Number', 'Type', 'Capacity', 'Price/Night'], tablefmt='grid'))

def make_booking():
    """Make a booking"""
    try:
        view_available_rooms()
        room_id = click.prompt('Room ID', type=int)
        check_in = click.prompt('Check-in date (YYYY-MM-DD)')
        check_out = click.prompt('Check-out date (YYYY-MM-DD)')
        
        check_in_date = parse_date(check_in)
        check_out_date = parse_date(check_out)
        
        booking = booking_service.create_booking(current_user.id, room_id, check_in_date, check_out_date)
        click.echo(f"✅ Booking created successfully!")
        click.echo(f"   Booking ID: {booking.id}")
        click.echo(f"   Total Price: KSh {booking.total_price:.2f}")
        click.echo(f"   Nights: {(check_out_date - check_in_date).days}")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")

def view_my_bookings():
    """View user's bookings"""
    bookings = booking_service.get_user_bookings(current_user.id)
    if not bookings:
        click.echo("No bookings found.")
        return
    
    table_data = []
    for b in bookings:
        room = room_service.get_room_by_id(b.room_id)
        table_data.append([
            b.id,
            room.number if room else 'Unknown',
            b.check_in.strftime('%Y-%m-%d'),
            b.check_out.strftime('%Y-%m-%d'),
            f"KSh {b.total_price:.2f}",
            b.status.value
        ])
    
    click.echo(tabulate(table_data, headers=['ID', 'Room', 'Check-in', 'Check-out', 'Total', 'Status'], tablefmt='grid'))

def cancel_my_booking():
    """Cancel user's booking"""
    view_my_bookings()
    try:
        booking_id = click.prompt('Booking ID to cancel', type=int)
        booking = booking_service.get_booking_by_id(booking_id)
        
        if not booking or booking.user_id != current_user.id:
            click.echo("❌ Booking not found or not yours.")
            return
        
        if booking_service.cancel_booking(booking_id):
            click.echo(f"✅ Booking {booking_id} cancelled successfully!")
        else:
            click.echo(f"❌ Failed to cancel booking.")
    except ValueError:
        click.echo("❌ Invalid booking ID.")

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Hostel Booking System CLI"""
    if ctx.invoked_subcommand is None:
        show_main_menu()

# User commands
@cli.group()
def user():
    """User management commands"""
    pass

@user.command()
@click.option('--name', prompt='Name', help='User name')
@click.option('--email', prompt='Email', help='User email')
@click.option('--phone', prompt='Phone', help='User phone number')
@click.option('--password', prompt='Password', hide_input=True, confirmation_prompt=True, help='User password')
def create(name, email, phone, password):
    """Create a new user"""
    try:
        user = user_service.create_user(name, email, phone, password)
        click.echo(f"✅ User created successfully! ID: {user.id}")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")

@user.command()
@click.option('--email', prompt='Email', help='User email')
@click.option('--password', prompt='Password', hide_input=True, help='User password')
def login(email, password):
    """Login user"""
    user = user_service.authenticate_user(email, password)
    if user:
        click.echo(f"✅ Login successful! Welcome, {user.name}")
        return user
    else:
        click.echo("❌ Invalid email or password")
        return None

@user.command()
def list():
    """List all users"""
    users = user_service.list_users()
    if not users:
        click.echo("No users found.")
        return
    
    table_data = [[u.id, u.name, u.email, u.phone] for u in users]
    click.echo(tabulate(table_data, headers=['ID', 'Name', 'Email', 'Phone'], tablefmt='grid'))

# Room commands
@cli.group()
def room():
    """Room management commands"""
    pass

@room.command()
@click.option('--number', prompt='Room number', help='Room number')
@click.option('--type', prompt='Room type', type=click.Choice(['single', 'double', 'dormitory']), help='Room type')
@click.option('--capacity', prompt='Capacity', type=int, help='Room capacity')
@click.option('--price', prompt='Price per night', type=float, help='Price per night')
def create(number, type, capacity, price):
    """Create a new room"""
    try:
        room = room_service.create_room(number, type, capacity, price)
        click.echo(f"✅ Room created successfully! ID: {room.id}")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")

@room.command()
@click.option('--available-only', is_flag=True, help='Show only available rooms')
def list(available_only):
    """List rooms"""
    rooms = room_service.list_available_rooms() if available_only else room_service.list_all_rooms()
    if not rooms:
        click.echo("No rooms found.")
        return
    
    table_data = [[r.id, r.number, r.room_type.value, r.capacity, f"KSh {r.price_per_night:.2f}", 
                   "✅" if r.is_available else "❌"] for r in rooms]
    click.echo(tabulate(table_data, headers=['ID', 'Number', 'Type', 'Capacity', 'Price/Night', 'Available'], tablefmt='grid'))

# Booking commands
@cli.group()
def booking():
    """Booking management commands"""
    pass

@booking.command()
@click.option('--user-id', prompt='User ID', type=int, help='User ID')
@click.option('--room-id', prompt='Room ID', type=int, help='Room ID')
@click.option('--check-in', prompt='Check-in date (YYYY-MM-DD)', help='Check-in date')
@click.option('--check-out', prompt='Check-out date (YYYY-MM-DD)', help='Check-out date')
def create(user_id, room_id, check_in, check_out):
    """Create a new booking"""
    try:
        check_in_date = parse_date(check_in)
        check_out_date = parse_date(check_out)
        
        booking = booking_service.create_booking(user_id, room_id, check_in_date, check_out_date)
        click.echo(f"✅ Booking created successfully!")
        click.echo(f"   Booking ID: {booking.id}")
        click.echo(f"   Total Price: KSh {booking.total_price:.2f}")
        click.echo(f"   Nights: {(check_out_date - check_in_date).days}")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")

@booking.command()
@click.option('--booking-id', prompt='Booking ID', type=int, help='Booking ID to cancel')
def cancel(booking_id):
    """Cancel a booking"""
    if booking_service.cancel_booking(booking_id):
        click.echo(f"✅ Booking {booking_id} cancelled successfully!")
    else:
        click.echo(f"❌ Booking {booking_id} not found.")

@booking.command()
@click.option('--user-id', type=int, help='Filter by user ID')
def list(user_id):
    """List bookings"""
    if user_id:
        bookings = booking_service.get_user_bookings(user_id)
    else:
        bookings = booking_service.list_all_bookings()
    
    if not bookings:
        click.echo("No bookings found.")
        return
    
    table_data = []
    for b in bookings:
        user = user_service.get_user_by_id(b.user_id)
        room = room_service.get_room_by_id(b.room_id)
        table_data.append([
            b.id, 
            user.name if user else 'Unknown',
            room.number if room else 'Unknown',
            b.check_in.strftime('%Y-%m-%d'),
            b.check_out.strftime('%Y-%m-%d'),
            f"KSh {b.total_price:.2f}",
            b.status.value
        ])
    
    click.echo(tabulate(table_data, headers=['ID', 'User', 'Room', 'Check-in', 'Check-out', 'Total', 'Status'], tablefmt='grid'))

@booking.command()
@click.option('--booking-id', prompt='Booking ID', type=int, help='Booking ID')
def details(booking_id):
    """Show booking details"""
    booking = booking_service.get_booking_by_id(booking_id)
    if not booking:
        click.echo(f"❌ Booking {booking_id} not found.")
        return
    
    user = user_service.get_user_by_id(booking.user_id)
    room = room_service.get_room_by_id(booking.room_id)
    
    click.echo(f"\n📋 Booking Details (ID: {booking.id})")
    click.echo(f"   User: {user.name if user else 'Unknown'} ({user.email if user else 'N/A'})")
    click.echo(f"   Room: {room.number if room else 'Unknown'} ({room.room_type.value if room else 'N/A'})")
    click.echo(f"   Check-in: {booking.check_in.strftime('%Y-%m-%d')}")
    click.echo(f"   Check-out: {booking.check_out.strftime('%Y-%m-%d')}")
    click.echo(f"   Nights: {(booking.check_out - booking.check_in).days}")
    click.echo(f"   Total Price: KSh {booking.total_price:.2f}")
    click.echo(f"   Status: {booking.status.value}")

# Quick setup command for demo
@cli.command()
def setup():
    """Setup demo data"""
    try:
        # Create sample users
        user1 = user_service.create_user("Brendah Chelugui", "brendachelugui@gmail.com", "+254712345678", "Chelugui")
        user2 = user_service.create_user("Erasmus Pkoskei", "pkosgei@gmail.com", "+254723456789", "Chelugui")
        
        # Create multiple rooms of each type
        rooms = [
            room_service.create_room("101", "single", 1, 2500.0),
            room_service.create_room("102", "single", 1, 2500.0),
            room_service.create_room("103", "single", 1, 2500.0),
            room_service.create_room("104", "single", 1, 2500.0),
            room_service.create_room("201", "double", 2, 4000.0),
            room_service.create_room("202", "double", 2, 4000.0),
            room_service.create_room("203", "double", 2, 4000.0),
            room_service.create_room("301", "dormitory", 4, 1500.0),
            room_service.create_room("302", "dormitory", 4, 1500.0),
            room_service.create_room("303", "dormitory", 4, 1500.0)
        ]
        
        click.echo("✅ Demo data created successfully!")
        click.echo(f"   Users: {user1.name} (ID: {user1.id}), {user2.name} (ID: {user2.id})")
        click.echo(f"   Rooms: {len(rooms)} rooms created (4 single, 3 double, 3 dormitory)")
        click.echo("\n   Demo login credentials:")
        click.echo("   - brendachelugui@gmail.com / Chelugui")
        click.echo("   - pkosgei@gmail.com / Chelugui")
        
    except ValueError as e:
        click.echo(f"❌ Error: {e}")

if __name__ == '__main__':
    cli()