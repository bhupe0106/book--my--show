# 🚀 Quick Start Guide - BookMyShow

## Option 1: Quick Launch (Windows)

Simply double-click `run.bat` file in the project folder.

```
run.bat
```

The application will automatically:
1. Check Python installation
2. Install required dependencies
3. Start the Streamlit server
4. Open in your default browser

## Option 2: Manual Launch (All Platforms)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run frontend/app.py
```

### Step 3: Access the Application
Open your browser and navigate to:
```
http://localhost:8501
```

## 🎯 First Steps in the Application

### 1. Create an Account
- Click "Login/Register" in the sidebar
- Switch to "Register" tab
- Fill in your details
- Create your account

### 2. Browse Movies
- You'll be taken to "My Bookings" page
- Click "Browse Movies" button
- View all available movies
- Search by title or genre

### 3. Book Your First Ticket
- Click "Book Now" on any movie
- Select your preferred theater
- Choose a show time
- Click on available seats to select them
- Review your booking
- Choose payment method
- Confirm booking

### 4. View Your Bookings
- Go to "My Bookings" page
- See all your reservations
- View booking details
- Cancel if needed

## 🔑 Demo Account (Optional)

If you don't want to create an account, use demo credentials:
- **Email**: demo@gmail.com
- **Password**: demo123

Or create a new account with your own details.

## 🎨 Application Features

### Home Page
- Browse all available movies
- Search movies by title
- Sort by rating, duration, or title
- View movie details (cast, director, duration, etc.)

### Book Tickets
- 5-step booking process
- Visual theater seat layout
- Real-time seat availability
- Price calculation
- Multiple payment methods

### My Bookings
- View all your bookings
- Filter by status (Confirmed, Pending, Cancelled)
- See booking details
- Cancel bookings
- View user profile

## 🌟 Key Features

✅ **User Authentication**
- Register new account
- Login with email/password
- Profile management

✅ **Movie Discovery**
- Browse all movies
- Advanced search and filtering
- Movie details with cast and director

✅ **Booking System**
- Multi-step booking wizard
- Visual seat selection
- Real-time availability tracking

✅ **Payment Integration**
- Support for multiple payment methods
- Order confirmation
- Transaction tracking

✅ **Booking Management**
- View all bookings
- Cancel bookings
- Track booking status

## 🛠️ Troubleshooting

### Issue: Python not found
**Solution**: Install Python 3.8+ from https://www.python.org/

### Issue: Port 8501 already in use
**Solution**: Run with a different port:
```bash
streamlit run frontend/app.py --server.port=8502
```

### Issue: Dependencies installation fails
**Solution**: Try updating pip first:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Application not loading
**Solution**: Clear Streamlit cache:
```bash
streamlit cache clear
streamlit run frontend/app.py
```

## 📱 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Any modern browser with JavaScript enabled

## 🔒 Test Data

### Sample Movies
1. **Avatar: The Way of Water**
   - Genre: Sci-Fi
   - Rating: 7.8/10
   - Duration: 192 minutes

2. **The Marvels**
   - Genre: Action
   - Rating: 6.1/10
   - Duration: 105 minutes

3. **Oppenheimer**
   - Genre: Drama
   - Rating: 8.5/10
   - Duration: 180 minutes

### Sample Theaters
1. **PVR Cinemas** - Mumbai, Andheri West
2. **INOX Entertainment** - Bangalore, Koramangala

### Sample Seats
- Row A-J with seats 1-10
- Regular seats: ₹200
- Premium seats (rows G-J): ₹250

## 💡 Pro Tips

1. **Batch Booking**: Select multiple seats at once for group bookings
2. **Price Comparison**: Different seats have different prices
3. **Show Timing**: Shows are available 2 days in advance
4. **Payment Methods**: Choose your preferred payment method at checkout
5. **Booking Cancellation**: Cancel up to show time for refunds

## 🎓 Architecture Overview

The application follows a 3-tier architecture:

```
┌─────────────────────────┐
│   Streamlit Frontend    │
│  (User Interface)       │
├─────────────────────────┤
│  Backend Services       │
│  (Business Logic)       │
├─────────────────────────┤
│  Database Layer         │
│  (Data Models)          │
└─────────────────────────┘
```

## 📚 Project Structure

```
book-my-show/
├── frontend/          # Streamlit UI
├── backend/          # Business logic
├── models/           # Data models
├── requirements.txt  # Dependencies
├── README.md         # Full documentation
├── QUICKSTART.md     # This file
├── run.bat          # Windows launcher
└── run.sh           # Linux/Mac launcher
```

## 🚀 Next Steps

1. **Explore the Code**: Check out the implementation details
2. **Customize**: Modify colors, add movies, change prices
3. **Extend**: Add features like reviews, wishlists, etc.
4. **Deploy**: Host on Streamlit Cloud, Heroku, or AWS
5. **Database**: Replace in-memory DB with PostgreSQL/MySQL

## 📞 Support

For detailed information, see the main [README.md](README.md)

---

**Enjoy BookMyShow! 🎬🎟️**

Happy booking and have fun exploring the application!
