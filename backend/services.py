"""
Backend Services for BookMyShow Application
Business Logic Layer
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from models.database import (
    Movie, Theater, Show, User, Booking, BookingDetail, Seat, Payment,
    SeatStatus, BookingStatus, MovieDatabase
)


class MovieService:
    """Service for movie operations"""
    
    def __init__(self, db: MovieDatabase):
        self.db = db
    
    def get_all_movies(self) -> List[Movie]:
        """Fetch all available movies"""
        return self.db.get_all_movies()
    
    def get_movie_details(self, movie_id: str) -> Optional[Movie]:
        """Get detailed information about a specific movie"""
        return self.db.get_movie(movie_id)
    
    def search_movies(self, query: str) -> List[Movie]:
        """Search movies by title or genre"""
        query = query.lower()
        return [
            movie for movie in self.db.get_all_movies()
            if query in movie.title.lower() or query in movie.genre.lower()
        ]


class TheaterService:
    """Service for theater operations"""
    
    def __init__(self, db: MovieDatabase):
        self.db = db
    
    def get_all_theaters(self) -> List[Theater]:
        """Fetch all available theaters"""
        return self.db.get_all_theaters()
    
    def get_theater_details(self, theater_id: str) -> Optional[Theater]:
        """Get theater information"""
        return self.db.get_theater(theater_id)
    
    def get_theaters_by_city(self, city: str) -> List[Theater]:
        """Get all theaters in a specific city"""
        return [
            theater for theater in self.db.get_all_theaters()
            if theater.city.lower() == city.lower()
        ]


class ShowService:
    """Service for show/screening operations"""
    
    def __init__(self, db: MovieDatabase):
        self.db = db
        self._initialize_shows()
    
    def _initialize_shows(self):
        """Initialize sample shows"""
        if not self.db.shows:
            # Create sample shows
            for movie_id in list(self.db.movies.keys())[:3]:
                for theater_id in list(self.db.theaters.keys()):
                    for i in range(2):  # 2 shows per movie per theater
                        show_id = f"S{uuid.uuid4().hex[:8]}"
                        start_time = datetime.now() + timedelta(days=i, hours=10 + i*3)
                        end_time = start_time + timedelta(minutes=180)
                        
                        # Create seats (10x10 theater)
                        seats = []
                        for row in range(ord('A'), ord('J') + 1):
                            for seat_num in range(1, 11):
                                seat_id = f"{chr(row)}{seat_num}"
                                price = 250 if seat_num > 7 else 200  # Premium seats
                                seats.append(Seat(
                                    seat_id=seat_id,
                                    row=chr(row),
                                    number=seat_num,
                                    price=price
                                ))
                        
                        show = Show(
                            show_id=show_id,
                            movie_id=movie_id,
                            theater_id=theater_id,
                            start_time=start_time,
                            end_time=end_time,
                            seats=seats
                        )
                        self.db.shows[show_id] = show
    
    def get_shows_by_movie_and_theater(self, movie_id: str, theater_id: str) -> List[Show]:
        """Get all shows for a specific movie in a theater"""
        return [
            show for show in self.db.shows.values()
            if show.movie_id == movie_id and show.theater_id == theater_id
        ]
    
    def get_show_details(self, show_id: str) -> Optional[Show]:
        """Get show details"""
        return self.db.shows.get(show_id)
    
    def get_available_seats(self, show_id: str) -> List[Seat]:
        """Get all available seats for a show"""
        show = self.get_show_details(show_id)
        if not show:
            return []
        return [seat for seat in show.seats if seat.status == SeatStatus.AVAILABLE]


class UserService:
    """Service for user operations"""
    
    def __init__(self, db: MovieDatabase):
        self.db = db
    
    def create_user(self, name: str, email: str, phone: str, password: str) -> User:
        """Create a new user"""
        user_id = f"U{uuid.uuid4().hex[:8]}"
        user = User(
            user_id=user_id,
            name=name,
            email=email,
            phone=phone,
            password=password
        )
        self.db.add_user(user)
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user information"""
        return self.db.get_user(user_id)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        for user in self.db.users.values():
            if user.email == email and user.password == password:
                return user
        return None


class BookingService:
    """Service for booking operations"""
    
    def __init__(self, db: MovieDatabase, show_service: ShowService):
        self.db = db
        self.show_service = show_service
    
    def create_booking(self, user_id: str, show_id: str, seat_ids: List[str]) -> Optional[Booking]:
        """Create a new booking"""
        show = self.show_service.get_show_details(show_id)
        user = self.db.get_user(user_id)
        
        if not show or not user:
            return None
        
        # Validate all seats are available
        for seat_id in seat_ids:
            seat = next((s for s in show.seats if s.seat_id == seat_id), None)
            if not seat or seat.status != SeatStatus.AVAILABLE:
                return None
        
        # Create booking
        booking_id = f"B{uuid.uuid4().hex[:8]}"
        booking = Booking(
            booking_id=booking_id,
            user_id=user_id,
            show_id=show_id,
            booking_date=datetime.now()
        )
        
        # Add seats to booking
        for seat_id in seat_ids:
            seat = next(s for s in show.seats if s.seat_id == seat_id)
            booking_detail = BookingDetail(
                booking_detail_id=f"BD{uuid.uuid4().hex[:8]}",
                booking_id=booking_id,
                show_id=show_id,
                seat_id=seat_id,
                price=seat.price
            )
            booking.add_seat(booking_detail)
            # Mark seat as booked
            seat.status = SeatStatus.BOOKED
        
        self.db.add_booking(booking)
        user.add_booking(booking)
        
        return booking
    
    def get_booking(self, booking_id: str) -> Optional[Booking]:
        """Get booking details"""
        return self.db.get_booking(booking_id)
    
    def get_user_bookings(self, user_id: str) -> List[Booking]:
        """Get all bookings of a user"""
        return self.db.get_user_bookings(user_id)
    
    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking"""
        booking = self.get_booking(booking_id)
        if not booking or booking.status == BookingStatus.CANCELLED:
            return False
        
        show = self.show_service.get_show_details(booking.show_id)
        if not show:
            return False
        
        # Free up seats
        for detail in booking.booking_details:
            seat = next((s for s in show.seats if s.seat_id == detail.seat_id), None)
            if seat:
                seat.status = SeatStatus.AVAILABLE
        
        booking.status = BookingStatus.CANCELLED
        return True


class PaymentService:
    """Service for payment operations"""
    
    def __init__(self, db: MovieDatabase):
        self.db = db
    
    def process_payment(self, booking_id: str, amount: float, payment_method: str) -> Optional[Payment]:
        """Process payment for a booking"""
        booking = self.db.get_booking(booking_id)
        if not booking:
            return None
        
        # Simulate payment processing
        payment_id = f"P{uuid.uuid4().hex[:8]}"
        transaction_id = f"TXN{uuid.uuid4().hex[:12]}"
        
        # In real scenario: integrate with payment gateway
        payment = Payment(
            payment_id=payment_id,
            booking_id=booking_id,
            amount=amount,
            payment_method=payment_method,
            status="success",  # Simulate successful payment
            transaction_id=transaction_id
        )
        
        self.db.payments[payment_id] = payment
        
        # Update booking status
        if payment.status == "success":
            booking.status = BookingStatus.CONFIRMED
        
        return payment
    
    def get_payment(self, payment_id: str) -> Optional[Payment]:
        """Get payment details"""
        return self.db.payments.get(payment_id)
