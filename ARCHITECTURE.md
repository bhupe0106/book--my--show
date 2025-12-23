# 🏗️ Technical Architecture & LLD - BookMyShow

## System Design Overview

This document details the Low-Level Design (LLD) of the BookMyShow application.

## 1. Architecture Pattern

### 3-Tier Architecture
```
┌──────────────────────────────────────┐
│     PRESENTATION LAYER               │
│  (Streamlit - Frontend Pages)        │
├──────────────────────────────────────┤
│     BUSINESS LOGIC LAYER             │
│  (Service Classes)                   │
├──────────────────────────────────────┤
│     DATA ACCESS LAYER                │
│  (Database Models & In-Memory DB)    │
└──────────────────────────────────────┘
```

## 2. Core Components

### 2.1 Data Models (models/database.py)

#### User
```python
@dataclass
class User:
    user_id: str              # Unique identifier
    name: str                 # User's full name
    email: str                # Email address
    phone: str                # Phone number
    password: str             # Password (hashed in production)
    created_at: datetime      # Account creation time
    bookings: List[Booking]   # User's bookings
    wallet_balance: float     # Wallet balance for quick payments
```

**Operations**: Create, Read, Authenticate

#### Movie
```python
@dataclass
class Movie:
    movie_id: str             # Unique identifier
    title: str                # Movie title
    genre: str                # Genre
    duration: int             # Duration in minutes
    rating: float             # IMDb-like rating
    language: str             # Language
    release_date: datetime    # Release date
    poster_url: str           # Poster URL
    description: str          # Description
    director: str             # Director name
    cast: List[str]           # Cast list
```

**Operations**: List, Search, Get Details

#### Theater
```python
@dataclass
class Theater:
    theater_id: str           # Unique identifier
    name: str                 # Theater name
    city: str                 # City
    location: str             # Street address
    total_screens: int        # Number of screens
    screens: dict             # Screen details
```

**Operations**: List, Get Details, Filter by City

#### Show
```python
@dataclass
class Show:
    show_id: str              # Unique identifier
    movie_id: str             # Foreign key to Movie
    theater_id: str           # Foreign key to Theater
    start_time: datetime      # Show start time
    end_time: datetime        # Show end time
    seats: List[Seat]         # Available seats
    language: str             # Show language
    format: str               # Format (2D, 3D, IMAX)
```

**Operations**: List, Get Details, Update Seats

#### Seat
```python
@dataclass
class Seat:
    seat_id: str              # Format: "{Row}{Number}" (e.g., "A1")
    row: str                  # Row letter (A-J)
    number: int               # Seat number (1-10)
    price: float              # Price
    status: SeatStatus        # Status (AVAILABLE, BOOKED, RESERVED)
```

**Statuses**: 
- `AVAILABLE`: Open for booking
- `BOOKED`: Seat is booked
- `RESERVED`: Temporarily reserved

#### Booking
```python
@dataclass
class Booking:
    booking_id: str           # Unique identifier
    user_id: str              # Foreign key to User
    show_id: str              # Foreign key to Show
    booking_date: datetime    # When booking was made
    booking_details: List[BookingDetail]  # Seats booked
    total_price: float        # Total amount
    status: BookingStatus     # Status
    payment_method: str       # Payment method
```

**Statuses**:
- `PENDING`: Payment pending
- `CONFIRMED`: Payment successful
- `CANCELLED`: Booking cancelled

#### BookingDetail
```python
@dataclass
class BookingDetail:
    booking_detail_id: str    # Unique identifier
    booking_id: str           # Foreign key to Booking
    show_id: str              # Foreign key to Show
    seat_id: str              # Foreign key to Seat
    price: float              # Price at booking time
```

#### Payment
```python
@dataclass
class Payment:
    payment_id: str           # Unique identifier
    booking_id: str           # Foreign key to Booking
    amount: float             # Payment amount
    payment_method: str       # Method
    status: str               # success, failed, pending
    transaction_id: str       # Transaction ID
    created_at: datetime      # Payment timestamp
```

### 2.2 Service Layer (backend/services.py)

#### MovieService
```
Operations:
├── get_all_movies()
├── get_movie_details(movie_id)
└── search_movies(query)

Dependencies:
└── MovieDatabase
```

#### TheaterService
```
Operations:
├── get_all_theaters()
├── get_theater_details(theater_id)
└── get_theaters_by_city(city)

Dependencies:
└── MovieDatabase
```

#### ShowService
```
Operations:
├── get_shows_by_movie_and_theater(movie_id, theater_id)
├── get_show_details(show_id)
└── get_available_seats(show_id)

Dependencies:
└── MovieDatabase
```

#### UserService
```
Operations:
├── create_user(name, email, phone, password)
├── get_user(user_id)
└── authenticate_user(email, password)

Dependencies:
└── MovieDatabase
```

#### BookingService
```
Operations:
├── create_booking(user_id, show_id, seat_ids)
├── get_booking(booking_id)
├── get_user_bookings(user_id)
└── cancel_booking(booking_id)

Dependencies:
├── MovieDatabase
└── ShowService
```

#### PaymentService
```
Operations:
├── process_payment(booking_id, amount, payment_method)
└── get_payment(payment_id)

Dependencies:
└── MovieDatabase
```

### 2.3 Presentation Layer (frontend/)

#### Main App (app.py)
```
Responsibilities:
├── Initialize services
├── Manage session state
├── Handle navigation
└── Render sidebar
```

#### Pages
- **00_home.py**: Movie browsing and search
- **01_book_tickets.py**: 5-step booking wizard
- **02_my_bookings.py**: Booking management
- **03_login.py**: User authentication

## 3. Data Flow Diagrams

### 3.1 Booking Flow
```
User Login
    ↓
Browse Movies (MovieService)
    ↓
Search/Filter (MovieService.search_movies)
    ↓
Select Movie
    ↓
Find Theaters (TheaterService)
    ↓
Select Theater
    ↓
Get Shows (ShowService)
    ↓
Select Show Time
    ↓
View Seats (ShowService.get_available_seats)
    ↓
Select Seats
    ↓
Create Booking (BookingService.create_booking)
    ↓
Process Payment (PaymentService.process_payment)
    ↓
Confirm Booking → Update Show (Seats marked as BOOKED)
    ↓
Display Confirmation
```

### 3.2 Class Relationships
```
User
├── bookings[] → Booking
                ├── show_id → Show
                │             ├── movie_id → Movie
                │             └── theater_id → Theater
                └── booking_details[] → BookingDetail
                                        └── seat_id → Seat

Payment
└── booking_id → Booking
```

## 4. Design Patterns Used

### 4.1 Service Locator Pattern
```python
services = {
    'movie_service': MovieService(db),
    'theater_service': TheaterService(db),
    'show_service': ShowService(db),
    'booking_service': BookingService(db, show_service),
    'payment_service': PaymentService(db),
    'user_service': UserService(db)
}
```

### 4.2 Repository Pattern
```python
class MovieDatabase:
    def get_all_movies(self) -> List[Movie]
    def get_movie(self, movie_id) -> Optional[Movie]
    # Centralized data access
```

### 4.3 Session Management
```python
# Streamlit session state for user context
st.session_state.current_user
st.session_state.selected_seats
st.session_state.selected_show
```

### 4.4 Multi-Page Architecture
```
app.py (Main)
├── pages/
│   ├── 00_home.py
│   ├── 01_book_tickets.py
│   ├── 02_my_bookings.py
│   └── 03_login.py
```

## 5. State Management

### Session State Variables
```python
st.session_state.services              # All service instances
st.session_state.current_user          # Logged-in user
st.session_state.selected_movie        # Currently selected movie
st.session_state.selected_theater      # Selected theater
st.session_state.selected_show         # Selected show
st.session_state.selected_seats        # Selected seat IDs
```

## 6. Algorithm Details

### 6.1 Seat Selection Algorithm
```
1. Get all seats for show
2. Filter by AVAILABLE status
3. Display in grid layout
4. Track selected seat IDs
5. Calculate total price
6. Validate availability before booking
7. Update seat status to BOOKED
```

### 6.2 Booking Creation Algorithm
```
1. Validate user exists
2. Validate show exists
3. For each selected seat:
   a. Check if AVAILABLE
   b. If not available, reject
4. Create Booking object
5. Create BookingDetail for each seat
6. Update seat status to BOOKED
7. Update user's bookings
8. Return booking
```

### 6.3 Payment Processing Algorithm
```
1. Validate booking exists
2. Validate amount matches total
3. Create Payment object
4. Simulate gateway processing
5. Generate transaction ID
6. Update booking status based on payment
7. Return payment confirmation
```

## 7. Error Handling

### Validation Errors
```python
if not show or not user:
    return None  # Handle gracefully in UI

if seat.status != SeatStatus.AVAILABLE:
    st.error("Seat not available")
```

### Transaction Safety
```python
# Validate all seats before creating booking
for seat_id in seat_ids:
    if not is_available(seat_id):
        return None  # Rollback

# Update all seats atomically
for seat in seats:
    seat.status = BOOKED
```

## 8. Performance Considerations

### Caching
```python
@st.cache_resource
def initialize_services():
    # Services initialized once per session
    return services
```

### In-Memory Storage
- Current implementation uses Python dictionaries
- Scales for ~10,000 records
- For larger scale, use SQL database

### Query Optimization
```python
# Efficient filtering
shows = [s for s in db.shows.values() 
         if s.movie_id == movie_id 
         and s.theater_id == theater_id]
```

## 9. Scalability Roadmap

### Phase 1: Current
- In-memory database
- Single user session
- 3 movies, 2 theaters

### Phase 2: SQL Database
- PostgreSQL integration
- Connection pooling
- Query optimization

### Phase 3: Microservices
- User Service
- Booking Service
- Payment Service
- Notification Service

### Phase 4: Distributed
- Load balancing
- Caching layer (Redis)
- Message queue (RabbitMQ)

## 10. Security Considerations

### Current Implementation
```python
# Simple text storage (for demo)
user.password = password
```

### Production Implementation
```python
# Hash passwords
from werkzeug.security import generate_password_hash
hashed = generate_password_hash(password)

# Use JWT tokens
import jwt
token = jwt.encode({'user_id': user.user_id})
```

### Other Security Measures
- Input validation
- SQL injection prevention
- CSRF tokens
- Rate limiting
- HTTPS enforcement

## 11. Testing Strategy

### Unit Tests
```python
def test_user_creation():
    user = user_service.create_user(...)
    assert user.user_id is not None

def test_booking_creation():
    booking = booking_service.create_booking(...)
    assert booking.total_price > 0
```

### Integration Tests
```python
def test_full_booking_flow():
    # Create user
    # Select movie
    # Create booking
    # Process payment
    # Verify confirmation
```

### UI Tests
```python
# Streamlit testing with pytest
# Verify page rendering
# Check button functionality
```

## 12. Deployment Architecture

### Streamlit Cloud
```
GitHub → Streamlit Cloud → Public URL
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "frontend/app.py"]
```

### AWS Deployment
```
EC2 Instance
├── Python Environment
├── Streamlit Server
└── Database (RDS)
```

---

## Summary

The BookMyShow application demonstrates solid LLD principles:

✅ **Separation of Concerns**: Models, Services, UI
✅ **DRY Principle**: Reusable service methods
✅ **SOLID Principles**: Single responsibility, Dependency injection
✅ **Scalability**: Ready for database migration
✅ **Security**: Foundation for auth/encryption
✅ **Maintainability**: Clear structure and documentation

---

**Document Version**: 1.0  
**Last Updated**: December 2025
