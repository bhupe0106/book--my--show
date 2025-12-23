"""
MongoDB Setup Script for BookMyShow
Initializes database with sample data
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.mongodb_connection import get_database, Collections, MongoDBConnection
from backend.mongodb_repository import (
    UserRepository, MovieRepository, TheaterRepository, BookingRepository, PaymentRepository
)
from models.database import User, Movie, Theater, Show, Seat, SeatStatus


def initialize_database():
    """Initialize MongoDB with sample data"""
    
    print("🚀 Initializing MongoDB for BookMyShow...")
    print("=" * 60)
    
    try:
        # Connect to MongoDB
        connection = MongoDBConnection()
        db = get_database()
        
        # Clear existing data
        print("🧹 Clearing existing collections...")
        for collection in [Collections.USERS, Collections.MOVIES, Collections.THEATERS, 
                          Collections.SHOWS, Collections.SEATS, Collections.BOOKINGS, 
                          Collections.BOOKING_DETAILS, Collections.PAYMENTS]:
            db[collection].delete_many({})
        print("✅ Collections cleared")
        
        # Initialize repositories
        user_repo = UserRepository()
        movie_repo = MovieRepository()
        theater_repo = TheaterRepository()
        
        # Create sample users
        print("\n📝 Creating sample users...")
        sample_users = [
            User(
                user_id="U001",
                name="Rahul Kumar",
                email="rahul@gmail.com",
                phone="9876543210",
                password="password123"
            ),
            User(
                user_id="U002",
                name="Demo User",
                email="demo@gmail.com",
                phone="9876543211",
                password="demo123"
            ),
            User(
                user_id="U003",
                name="Priya Singh",
                email="priya@gmail.com",
                phone="9876543212",
                password="priya123"
            )
        ]
        
        for user in sample_users:
            if user_repo.create_user(user):
                print(f"  ✅ Created user: {user.name} ({user.email})")
        
        # Create sample movies
        print("\n🎬 Creating sample movies...")
        sample_movies = [
            Movie(
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
            Movie(
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
            Movie(
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
            )
        ]
        
        for movie in sample_movies:
            if movie_repo.create_movie(movie):
                print(f"  ✅ Created movie: {movie.title}")
        
        # Create sample theaters
        print("\n🏢 Creating sample theaters...")
        sample_theaters = [
            Theater(
                theater_id="T001",
                name="PVR Cinemas",
                city="Mumbai",
                location="Andheri West",
                total_screens=4
            ),
            Theater(
                theater_id="T002",
                name="INOX Entertainment",
                city="Bangalore",
                location="Koramangala",
                total_screens=3
            ),
            Theater(
                theater_id="T003",
                name="Cinepolis",
                city="Delhi",
                location="Connaught Place",
                total_screens=5
            )
        ]
        
        for theater in sample_theaters:
            if theater_repo.create_theater(theater):
                print(f"  ✅ Created theater: {theater.name} ({theater.city})")
        
        # Create indexes for better performance
        print("\n📊 Creating database indexes...")
        db[Collections.USERS].create_index("email", unique=True)
        db[Collections.USERS].create_index("user_id", unique=True)
        db[Collections.MOVIES].create_index("movie_id", unique=True)
        db[Collections.THEATERS].create_index("theater_id", unique=True)
        db[Collections.BOOKINGS].create_index("booking_id", unique=True)
        db[Collections.BOOKINGS].create_index("user_id")
        db[Collections.PAYMENTS].create_index("payment_id", unique=True)
        db[Collections.PAYMENTS].create_index("booking_id")
        print("  ✅ Indexes created")
        
        print("\n" + "=" * 60)
        print("✅ MongoDB initialization completed successfully!")
        print("\n📊 Sample Data Summary:")
        print(f"  • Users: {len(sample_users)}")
        print(f"  • Movies: {len(sample_movies)}")
        print(f"  • Theaters: {len(sample_theaters)}")
        print("\n🎯 Demo Account:")
        print("  • Email: demo@gmail.com")
        print("  • Password: demo123")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        print("\n⚠️  Make sure MongoDB is running at mongodb://localhost:27017/")
        sys.exit(1)


if __name__ == "__main__":
    initialize_database()
