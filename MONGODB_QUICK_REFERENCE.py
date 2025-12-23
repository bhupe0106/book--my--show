#!/usr/bin/env python
"""
MongoDB Setup Quick Reference for BookMyShow
"""

# ============================================
# QUICK START GUIDE
# ============================================

"""
1. VERIFY MONGODB IS RUNNING
   - MongoDB should be running on localhost:27017
   - Check: mongosh or MongoDB Compass

2. INITIALIZE DATABASE
   Run: python setup_mongodb.py
   
   This will:
   ✅ Connect to MongoDB
   ✅ Clear existing data
   ✅ Create 3 sample users
   ✅ Create 3 sample movies
   ✅ Create 3 sample theaters
   ✅ Create database indexes

3. RUN APPLICATION
   Run: python -m streamlit run frontend/app.py
   
4. LOGIN WITH DEMO ACCOUNT
   Email: demo@gmail.com
   Password: demo123
"""

# ============================================
# ENVIRONMENT VARIABLES
# ============================================

"""
.env file contains:
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=bookshow
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
"""

# ============================================
# MONGODB STRUCTURE
# ============================================

"""
Database: bookshow

Collections:
├── users
│   ├── user_id (unique)
│   ├── email (unique)
│   ├── name
│   ├── phone
│   ├── password
│   └── wallet_balance
│
├── movies
│   ├── movie_id (unique)
│   ├── title
│   ├── genre
│   ├── duration
│   ├── rating
│   ├── director
│   └── cast[]
│
├── theaters
│   ├── theater_id (unique)
│   ├── name
│   ├── city
│   ├── location
│   └── total_screens
│
├── shows
│   ├── show_id (unique)
│   ├── movie_id
│   ├── theater_id
│   ├── start_time
│   └── end_time
│
├── seats
│   ├── seat_id (unique)
│   ├── show_id
│   ├── row
│   ├── number
│   └── status
│
├── bookings
│   ├── booking_id (unique)
│   ├── user_id
│   ├── show_id
│   ├── total_price
│   └── status
│
├── booking_details
│   ├── booking_detail_id
│   ├── booking_id
│   ├── seat_id
│   └── price
│
└── payments
    ├── payment_id (unique)
    ├── booking_id
    ├── amount
    └── status
"""

# ============================================
# CODE EXAMPLES
# ============================================

# Import MongoDB connection
from backend.mongodb_connection import get_database, Collections, MongoDBConnection

# Get database
db = get_database()

# Query users
users = db[Collections.USERS].find({})
for user in users:
    print(f"User: {user['email']}")

# Query movies
movies = db[Collections.MOVIES].find({})
for movie in movies:
    print(f"Movie: {movie['title']}")

# Create index
db[Collections.USERS].create_index("email", unique=True)

# ============================================
# REPOSITORY USAGE
# ============================================

from backend.mongodb_repository import (
    UserRepository, MovieRepository, TheaterRepository,
    BookingRepository, PaymentRepository
)

# User operations
user_repo = UserRepository()
user = user_repo.get_user_by_email("demo@gmail.com")
all_users = db[Collections.USERS].find({})

# Movie operations
movie_repo = MovieRepository()
movies = movie_repo.get_all_movies()
movie = movie_repo.get_movie("M001")

# Theater operations
theater_repo = TheaterRepository()
theaters = theater_repo.get_all_theaters()
theater = theater_repo.get_theater("T001")

# Booking operations
booking_repo = BookingRepository()
bookings = booking_repo.get_user_bookings("U001")
booking = booking_repo.get_booking("B001")

# ============================================
# USEFUL COMMANDS
# ============================================

"""
# Initialize database
python setup_mongodb.py

# Run application
python -m streamlit run frontend/app.py

# Test MongoDB connection
python -c "from backend.mongodb_connection import MongoDBConnection; \
print('Connected!' if MongoDBConnection().is_connected() else 'Not connected')"

# Check installed packages
pip list | findstr mongo

# View MongoDB data (using MongoDB Compass)
1. Download MongoDB Compass
2. Connect to mongodb://localhost:27017/
3. Navigate to bookshow database
4. Browse collections
"""

# ============================================
# TROUBLESHOOTING
# ============================================

"""
Problem: "Cannot connect to MongoDB"
Solution: 
  1. Start MongoDB service
  2. Verify it's running on localhost:27017
  3. Check firewall settings

Problem: "pymongo not installed"
Solution:
  python -m pip install pymongo>=4.6.0

Problem: "Database bookshow not found"
Solution:
  python setup_mongodb.py

Problem: "Collection not found"
Solution:
  python setup_mongodb.py
  (Creates all collections with sample data)
"""

# ============================================
# FEATURES
# ============================================

"""
✅ Connection Pooling
   - Automatic connection management
   - Singleton pattern for efficiency

✅ Repository Pattern
   - Clean data access layer
   - Easy to test
   - Easy to modify

✅ Error Handling
   - Comprehensive error messages
   - Connection status checking

✅ Data Integrity
   - Unique indexes on key fields
   - Proper data validation

✅ Sample Data
   - 3 users
   - 3 movies
   - 3 theaters
   - Ready to use
"""

# ============================================
# SAMPLE DATA
# ============================================

"""
Users:
1. Rahul Kumar (rahul@gmail.com)
2. Demo User (demo@gmail.com) - Password: demo123 ✅
3. Priya Singh (priya@gmail.com)

Movies:
1. Avatar: The Way of Water (Rating: 7.8)
2. The Marvels (Rating: 6.1)
3. Oppenheimer (Rating: 8.5)

Theaters:
1. PVR Cinemas (Mumbai)
2. INOX Entertainment (Bangalore)
3. Cinepolis (Delhi)
"""

# ============================================
# NOTES
# ============================================

"""
1. Virtual environment created at: venv/
2. All dependencies installed globally
3. MongoDB connection tested and working
4. Ready to initialize database

Next Steps:
1. python setup_mongodb.py
2. python -m streamlit run frontend/app.py
3. Login with demo@gmail.com / demo123
"""
