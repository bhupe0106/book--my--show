"""
Database Models for BookMyShow Application
Low-Level Design Implementation
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class SeatStatus(Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    RESERVED = "reserved"


class BookingStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Seat:
    """Seat model for theater"""
    seat_id: str
    row: str
    number: int
    price: float
    status: SeatStatus = SeatStatus.AVAILABLE

    def __hash__(self):
        return hash(self.seat_id)


@dataclass
class Show:
    """Show/Screening model"""
    show_id: str
    movie_id: str
    theater_id: str
    start_time: datetime
    end_time: datetime
    seats: List[Seat] = field(default_factory=list)
    language: str = "English"
    format: str = "2D"  # 2D, 3D, IMAX
    
    def available_seats(self) -> int:
        return sum(1 for seat in self.seats if seat.status == SeatStatus.AVAILABLE)


@dataclass
class Movie:
    """Movie model"""
    movie_id: str
    title: str
    genre: str
    duration: int  # in minutes
    rating: float
    language: str
    release_date: datetime
    poster_url: str
    description: str
    director: str
    cast: List[str] = field(default_factory=list)


@dataclass
class Theater:
    """Theater/Cinema model"""
    theater_id: str
    name: str
    city: str
    location: str
    total_screens: int
    screens: dict = field(default_factory=dict)  # screen_id: screen_info


@dataclass
class BookingDetail:
    """Individual booking detail"""
    booking_detail_id: str
    booking_id: str
    show_id: str
    seat_id: str
    price: float


@dataclass
class Booking:
    """Booking/Order model"""
    booking_id: str
    user_id: str
    show_id: str
    booking_date: datetime
    booking_details: List[BookingDetail] = field(default_factory=list)
    total_price: float = 0.0
    status: BookingStatus = BookingStatus.PENDING
    payment_method: str = "card"

    def add_seat(self, booking_detail: BookingDetail):
        self.booking_details.append(booking_detail)
        self.total_price += booking_detail.price


@dataclass
class User:
    """User model"""
    user_id: str
    name: str
    email: str
    phone: str
    password: str  # in production: use hashed passwords
    created_at: datetime = field(default_factory=datetime.now)
    bookings: List[Booking] = field(default_factory=list)
    wallet_balance: float = 0.0

    def add_booking(self, booking: Booking):
        self.bookings.append(booking)


@dataclass
class Payment:
    """Payment model"""
    payment_id: str
    booking_id: str
    amount: float
    payment_method: str
    status: str  # success, failed, pending
    transaction_id: str
    created_at: datetime = field(default_factory=datetime.now)


class MovieDatabase:
    """In-memory database for the application"""
    
    def __init__(self):
        self.users: dict[str, User] = {}
        self.movies: dict[str, Movie] = {}
        self.theaters: dict[str, Theater] = {}
        self.shows: dict[str, Show] = {}
        self.bookings: dict[str, Booking] = {}
        self.payments: dict[str, Payment] = {}
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample data for demonstration"""
        # Sample Movies
        self.movies = {
            "M001": Movie(
                movie_id="M001",
                title="Avatar: The Way of Water",
                genre="Sci-Fi",
                duration=192,
                rating=7.8,
                language="English",
                release_date=datetime(2024, 1, 15),
                poster_url="https://via.placeholder.com/300x450?text=Avatar",
                description="The sequel to Avatar follows Jake Sully and Neytiri.",
                director="James Cameron",
                cast=["Sam Worthington", "Zoe Saldana"]
            ),
            "M002": Movie(
                movie_id="M002",
                title="The Marvels",
                genre="Action",
                duration=105,
                rating=6.1,
                language="English",
                release_date=datetime(2024, 2, 10),
                poster_url="https://via.placeholder.com/300x450?text=Marvels",
                description="Superhero action-adventure film.",
                director="Nia DaCosta",
                cast=["Brie Larson", "Teyonah Parris"]
            ),
            "M003": Movie(
                movie_id="M003",
                title="Oppenheimer",
                genre="Drama",
                duration=180,
                rating=8.5,
                language="English",
                release_date=datetime(2024, 3, 1),
                poster_url="https://via.placeholder.com/300x450?text=Oppenheimer",
                description="The story of J. Robert Oppenheimer.",
                director="Christopher Nolan",
                cast=["Cillian Murphy", "Emily Blunt"]
            ),
        }
        
        # Sample Theaters
        self.theaters = {
            "T001": Theater(
                theater_id="T001",
                name="PVR Cinemas",
                city="Mumbai",
                location="Andheri West",
                total_screens=4
            ),
            "T002": Theater(
                theater_id="T002",
                name="INOX Entertainment",
                city="Bangalore",
                location="Koramangala",
                total_screens=3
            ),
        }
    
    def get_all_movies(self) -> List[Movie]:
        return list(self.movies.values())
    
    def get_movie(self, movie_id: str) -> Optional[Movie]:
        return self.movies.get(movie_id)
    
    def get_all_theaters(self) -> List[Theater]:
        return list(self.theaters.values())
    
    def get_theater(self, theater_id: str) -> Optional[Theater]:
        return self.theaters.get(theater_id)
    
    def add_user(self, user: User):
        self.users[user.user_id] = user
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    def add_booking(self, booking: Booking):
        self.bookings[booking.booking_id] = booking
    
    def get_booking(self, booking_id: str) -> Optional[Booking]:
        return self.bookings.get(booking_id)
    
    def get_user_bookings(self, user_id: str) -> List[Booking]:
        user = self.get_user(user_id)
        return user.bookings if user else []
