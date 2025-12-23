# 📦 MongoDB Setup - BookMyShow

## ✅ Setup Complete!

### What Has Been Done

1. **Created Virtual Environment**
   - Location: `c:\Users\Asus\Desktop\book-my-show\venv`

2. **Updated Dependencies**
   - Added `pymongo>=4.6.0` (MongoDB driver)
   - Added `python-dotenv>=1.0.0` (Environment variables)
   - All packages installed successfully

3. **Created MongoDB Configuration**
   - ✅ `.env` file with MongoDB connection string
   - ✅ `mongodb_connection.py` - Connection management
   - ✅ `mongodb_repository.py` - Data access layer

4. **MongoDB Connection Details**
   ```
   URI: mongodb://localhost:27017/
   Database: bookshow
   Status: ✅ CONNECTED
   ```

---

## 📁 New Files Created

### Configuration Files
- **`.env`** - Environment variables for MongoDB
  ```
  MONGODB_URI=mongodb://localhost:27017/
  MONGODB_DATABASE=bookshow
  DEBUG=True
  SECRET_KEY=your-secret-key-here-change-in-production
  ```

### Backend Files
- **`backend/mongodb_connection.py`** - MongoDB connection singleton
  - Handles database connections
  - Provides connection pooling
  - Includes connection status checks
  
- **`backend/mongodb_repository.py`** - Repository pattern implementation
  - `UserRepository` - User operations
  - `MovieRepository` - Movie operations
  - `TheaterRepository` - Theater operations
  - `BookingRepository` - Booking operations
  - `PaymentRepository` - Payment operations

### Setup Script
- **`setup_mongodb.py`** - Database initialization script
  - Creates sample data
  - Sets up indexes for performance
  - Initializes all collections

---

## 🗂️ MongoDB Collections

The application uses the following collections:

```javascript
// Collections in bookshow database
{
  "users": [],           // User accounts
  "movies": [],          // Movie information
  "theaters": [],        // Theater/Cinema details
  "shows": [],           // Movie screenings
  "seats": [],           // Theater seats
  "bookings": [],        // Ticket bookings
  "booking_details": [], // Booking seat details
  "payments": []         // Payment records
}
```

---

## 🚀 How to Use MongoDB

### 1. Verify MongoDB is Running
```bash
# MongoDB should be running on localhost:27017
# You should see it in the Services or running process
```

### 2. Initialize Database with Sample Data
```bash
cd c:\Users\Asus\Desktop\book-my-show
python setup_mongodb.py
```

### 3. Run the Application
```bash
python -m streamlit run frontend/app.py
```

---

## 📊 Sample Data

The setup script creates:
- **3 Sample Users**
  - Rahul Kumar (rahul@gmail.com)
  - Demo User (demo@gmail.com) - Password: demo123
  - Priya Singh (priya@gmail.com)

- **3 Sample Movies**
  - Avatar: The Way of Water
  - The Marvels
  - Oppenheimer

- **3 Sample Theaters**
  - PVR Cinemas (Mumbai)
  - INOX Entertainment (Bangalore)
  - Cinepolis (Delhi)

---

## 🔧 Configuration Files

### `.env` File
```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=bookshow

# Application Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
```

### Requirements Updated
```
streamlit>=1.28.1
pandas>=2.0.0
numpy>=1.24.0
python-dateutil>=2.8.2
pymongo>=4.6.0          ← NEW
python-dotenv>=1.0.0    ← NEW
```

---

## 📋 Implementation Details

### MongoDB Connection (mongodb_connection.py)
```python
# Singleton pattern for connection management
connection = MongoDBConnection()
db = connection.get_db()

# Create indexes for performance
db[Collections.USERS].create_index("email", unique=True)
db[Collections.BOOKINGS].create_index("user_id")
```

### Repository Pattern (mongodb_repository.py)
```python
# Clean data access layer
user_repo = UserRepository()
user = user_repo.get_user_by_email("demo@gmail.com")

movie_repo = MovieRepository()
movies = movie_repo.get_all_movies()

booking_repo = BookingRepository()
bookings = booking_repo.get_user_bookings(user_id)
```

---

## ✨ Features

✅ **Connection Pooling**
- Automatic connection management
- Singleton pattern for efficiency
- Connection status verification

✅ **Repository Pattern**
- Clean separation of concerns
- Easy to test
- Easy to switch databases

✅ **Error Handling**
- Connection error messages
- Detailed logging
- Graceful fallback

✅ **Data Integrity**
- Unique indexes on key fields
- Foreign key relationships
- Transaction support ready

---

## 🔄 Migration from In-Memory to MongoDB

The codebase is now set up to use MongoDB. To fully migrate:

1. **Update Services** - Modify `backend/services.py` to use repositories
2. **Update Frontend** - Update pages to use new data layer
3. **Data Migration** - Run `setup_mongodb.py` to populate data

---

## 📞 Troubleshooting

### Issue: "Cannot connect to MongoDB"
**Solution**: Make sure MongoDB is running
```bash
# Check if MongoDB service is running
Get-Service MongoDB

# Or verify on port 27017
netstat -ano | findstr :27017
```

### Issue: "Collection 'users' not found"
**Solution**: Initialize database with sample data
```bash
python setup_mongodb.py
```

### Issue: "pymongo module not found"
**Solution**: Install dependencies
```bash
python -m pip install -r requirements.txt
```

---

## 🎯 Next Steps

1. **Test MongoDB Setup**
   ```bash
   python setup_mongodb.py
   ```

2. **Verify Collections**
   - Use MongoDB Compass or mongo shell
   - Should see 8 collections in "bookshow" database

3. **Run Application**
   ```bash
   python -m streamlit run frontend/app.py
   ```

4. **Test Functionality**
   - Register new user
   - Book tickets
   - View bookings

---

## 📚 Documentation

For more information:
- [MongoDB Official Docs](https://docs.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

---

## ✅ Status

- ✅ Virtual Environment Created
- ✅ MongoDB Dependencies Installed
- ✅ MongoDB Connected
- ✅ Connection Module Created
- ✅ Repository Layer Implemented
- ✅ Setup Script Ready
- ✅ Environment Variables Configured

---

**Ready to use MongoDB with BookMyShow! 🎬📊**

Run `python setup_mongodb.py` to initialize the database with sample data.
