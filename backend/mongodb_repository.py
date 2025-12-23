"""
MongoDB Repository Layer for BookMyShow
Provides database operations using MongoDB
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from backend.mongodb_connection import get_database, Collections
from models.database import (
    User, Movie, Theater, Show, Seat, Booking, BookingDetail, Payment,
    SeatStatus, BookingStatus
)


class MongoRepository:
    """Base repository for MongoDB operations"""
    
    def __init__(self):
        self.db = get_database()
    
    def dict_to_object(self, data: Dict) -> Dict:
        """Convert MongoDB _id to string"""
        if data and '_id' in data:
            data['id'] = str(data['_id'])
            del data['_id']
        return data


class UserRepository(MongoRepository):
    """User repository for MongoDB"""
    
    def create_user(self, user: User) -> bool:
        """Create a new user"""
        try:
            user_data = {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'password': user.password,
                'created_at': user.created_at,
                'wallet_balance': user.wallet_balance
            }
            self.db[Collections.USERS].insert_one(user_data)
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            user_data = self.db[Collections.USERS].find_one({'user_id': user_id})
            if user_data:
                return User(
                    user_id=user_data['user_id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    password=user_data['password'],
                    created_at=user_data.get('created_at', datetime.now()),
                    wallet_balance=user_data.get('wallet_balance', 0.0)
                )
        except Exception as e:
            print(f"Error getting user: {e}")
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            user_data = self.db[Collections.USERS].find_one({'email': email})
            if user_data:
                return User(
                    user_id=user_data['user_id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    password=user_data['password'],
                    created_at=user_data.get('created_at', datetime.now()),
                    wallet_balance=user_data.get('wallet_balance', 0.0)
                )
        except Exception as e:
            print(f"Error getting user by email: {e}")
        return None
    
    def user_exists(self, email: str) -> bool:
        """Check if user exists by email"""
        try:
            return self.db[Collections.USERS].find_one({'email': email}) is not None
        except:
            return False


class MovieRepository(MongoRepository):
    """Movie repository for MongoDB"""
    
    def create_movie(self, movie: Movie) -> bool:
        """Create a new movie"""
        try:
            movie_data = {
                'movie_id': movie.movie_id,
                'title': movie.title,
                'genre': movie.genre,
                'duration': movie.duration,
                'rating': movie.rating,
                'language': movie.language,
                'release_date': movie.release_date,
                'poster_url': movie.poster_url,
                'description': movie.description,
                'director': movie.director,
                'cast': movie.cast
            }
            self.db[Collections.MOVIES].insert_one(movie_data)
            return True
        except Exception as e:
            print(f"Error creating movie: {e}")
            return False
    
    def get_all_movies(self) -> List[Movie]:
        """Get all movies"""
        try:
            movies = []
            for movie_data in self.db[Collections.MOVIES].find():
                movies.append(Movie(
                    movie_id=movie_data['movie_id'],
                    title=movie_data['title'],
                    genre=movie_data['genre'],
                    duration=movie_data['duration'],
                    rating=movie_data['rating'],
                    language=movie_data['language'],
                    release_date=movie_data.get('release_date', datetime.now()),
                    poster_url=movie_data['poster_url'],
                    description=movie_data['description'],
                    director=movie_data['director'],
                    cast=movie_data.get('cast', [])
                ))
            return movies
        except Exception as e:
            print(f"Error getting all movies: {e}")
            return []
    
    def get_movie(self, movie_id: str) -> Optional[Movie]:
        """Get movie by ID"""
        try:
            movie_data = self.db[Collections.MOVIES].find_one({'movie_id': movie_id})
            if movie_data:
                return Movie(
                    movie_id=movie_data['movie_id'],
                    title=movie_data['title'],
                    genre=movie_data['genre'],
                    duration=movie_data['duration'],
                    rating=movie_data['rating'],
                    language=movie_data['language'],
                    release_date=movie_data.get('release_date', datetime.now()),
                    poster_url=movie_data['poster_url'],
                    description=movie_data['description'],
                    director=movie_data['director'],
                    cast=movie_data.get('cast', [])
                )
        except Exception as e:
            print(f"Error getting movie: {e}")
        return None


class TheaterRepository(MongoRepository):
    """Theater repository for MongoDB"""
    
    def create_theater(self, theater: Theater) -> bool:
        """Create a new theater"""
        try:
            theater_data = {
                'theater_id': theater.theater_id,
                'name': theater.name,
                'city': theater.city,
                'location': theater.location,
                'total_screens': theater.total_screens
            }
            self.db[Collections.THEATERS].insert_one(theater_data)
            return True
        except Exception as e:
            print(f"Error creating theater: {e}")
            return False
    
    def get_all_theaters(self) -> List[Theater]:
        """Get all theaters"""
        try:
            theaters = []
            for theater_data in self.db[Collections.THEATERS].find():
                theaters.append(Theater(
                    theater_id=theater_data['theater_id'],
                    name=theater_data['name'],
                    city=theater_data['city'],
                    location=theater_data['location'],
                    total_screens=theater_data['total_screens']
                ))
            return theaters
        except Exception as e:
            print(f"Error getting all theaters: {e}")
            return []
    
    def get_theater(self, theater_id: str) -> Optional[Theater]:
        """Get theater by ID"""
        try:
            theater_data = self.db[Collections.THEATERS].find_one({'theater_id': theater_id})
            if theater_data:
                return Theater(
                    theater_id=theater_data['theater_id'],
                    name=theater_data['name'],
                    city=theater_data['city'],
                    location=theater_data['location'],
                    total_screens=theater_data['total_screens']
                )
        except Exception as e:
            print(f"Error getting theater: {e}")
        return None


class BookingRepository(MongoRepository):
    """Booking repository for MongoDB"""
    
    def create_booking(self, booking: Booking) -> bool:
        """Create a new booking"""
        try:
            booking_data = {
                'booking_id': booking.booking_id,
                'user_id': booking.user_id,
                'show_id': booking.show_id,
                'booking_date': booking.booking_date,
                'total_price': booking.total_price,
                'status': booking.status.value,
                'payment_method': booking.payment_method,
                'created_at': datetime.now()
            }
            self.db[Collections.BOOKINGS].insert_one(booking_data)
            
            # Save booking details
            for detail in booking.booking_details:
                detail_data = {
                    'booking_detail_id': detail.booking_detail_id,
                    'booking_id': detail.booking_id,
                    'show_id': detail.show_id,
                    'seat_id': detail.seat_id,
                    'price': detail.price
                }
                self.db[Collections.BOOKING_DETAILS].insert_one(detail_data)
            
            return True
        except Exception as e:
            print(f"Error creating booking: {e}")
            return False
    
    def get_booking(self, booking_id: str) -> Optional[Booking]:
        """Get booking by ID"""
        try:
            booking_data = self.db[Collections.BOOKINGS].find_one({'booking_id': booking_id})
            if booking_data:
                # Get booking details
                details_data = list(self.db[Collections.BOOKING_DETAILS].find({'booking_id': booking_id}))
                booking_details = [
                    BookingDetail(
                        booking_detail_id=d['booking_detail_id'],
                        booking_id=d['booking_id'],
                        show_id=d['show_id'],
                        seat_id=d['seat_id'],
                        price=d['price']
                    )
                    for d in details_data
                ]
                
                return Booking(
                    booking_id=booking_data['booking_id'],
                    user_id=booking_data['user_id'],
                    show_id=booking_data['show_id'],
                    booking_date=booking_data.get('booking_date', datetime.now()),
                    booking_details=booking_details,
                    total_price=booking_data['total_price'],
                    status=BookingStatus(booking_data.get('status', 'pending')),
                    payment_method=booking_data.get('payment_method', 'card')
                )
        except Exception as e:
            print(f"Error getting booking: {e}")
        return None
    
    def get_user_bookings(self, user_id: str) -> List[Booking]:
        """Get all bookings for a user"""
        try:
            bookings = []
            for booking_data in self.db[Collections.BOOKINGS].find({'user_id': user_id}):
                # Get booking details
                details_data = list(self.db[Collections.BOOKING_DETAILS].find({'booking_id': booking_data['booking_id']}))
                booking_details = [
                    BookingDetail(
                        booking_detail_id=d['booking_detail_id'],
                        booking_id=d['booking_id'],
                        show_id=d['show_id'],
                        seat_id=d['seat_id'],
                        price=d['price']
                    )
                    for d in details_data
                ]
                
                booking = Booking(
                    booking_id=booking_data['booking_id'],
                    user_id=booking_data['user_id'],
                    show_id=booking_data['show_id'],
                    booking_date=booking_data.get('booking_date', datetime.now()),
                    booking_details=booking_details,
                    total_price=booking_data['total_price'],
                    status=BookingStatus(booking_data.get('status', 'pending')),
                    payment_method=booking_data.get('payment_method', 'card')
                )
                bookings.append(booking)
            
            return bookings
        except Exception as e:
            print(f"Error getting user bookings: {e}")
            return []
    
    def update_booking_status(self, booking_id: str, status: BookingStatus) -> bool:
        """Update booking status"""
        try:
            self.db[Collections.BOOKINGS].update_one(
                {'booking_id': booking_id},
                {'$set': {'status': status.value}}
            )
            return True
        except Exception as e:
            print(f"Error updating booking status: {e}")
            return False


class PaymentRepository(MongoRepository):
    """Payment repository for MongoDB"""
    
    def create_payment(self, payment: Payment) -> bool:
        """Create a new payment record"""
        try:
            payment_data = {
                'payment_id': payment.payment_id,
                'booking_id': payment.booking_id,
                'amount': payment.amount,
                'payment_method': payment.payment_method,
                'status': payment.status,
                'transaction_id': payment.transaction_id,
                'created_at': payment.created_at
            }
            self.db[Collections.PAYMENTS].insert_one(payment_data)
            return True
        except Exception as e:
            print(f"Error creating payment: {e}")
            return False
    
    def get_payment(self, payment_id: str) -> Optional[Payment]:
        """Get payment by ID"""
        try:
            payment_data = self.db[Collections.PAYMENTS].find_one({'payment_id': payment_id})
            if payment_data:
                return Payment(
                    payment_id=payment_data['payment_id'],
                    booking_id=payment_data['booking_id'],
                    amount=payment_data['amount'],
                    payment_method=payment_data['payment_method'],
                    status=payment_data['status'],
                    transaction_id=payment_data['transaction_id'],
                    created_at=payment_data.get('created_at', datetime.now())
                )
        except Exception as e:
            print(f"Error getting payment: {e}")
        return None
