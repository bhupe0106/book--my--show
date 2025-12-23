"""
BookMyShow Frontend Application using Streamlit
Multi-page application for movie booking system
"""
import streamlit as st
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import MovieDatabase
from backend.services import (
    MovieService, TheaterService, ShowService, 
    UserService, BookingService, PaymentService
)


# Initialize session state and services
@st.cache_resource
def initialize_services():
    db = MovieDatabase()
    movie_service = MovieService(db)
    theater_service = TheaterService(db)
    show_service = ShowService(db)
    user_service = UserService(db)
    booking_service = BookingService(db, show_service)
    payment_service = PaymentService(db)
    
    return {
        'db': db,
        'movie_service': movie_service,
        'theater_service': theater_service,
        'show_service': show_service,
        'user_service': user_service,
        'booking_service': booking_service,
        'payment_service': payment_service
    }


def init_session_state():
    """Initialize session state variables"""
    if 'services' not in st.session_state:
        st.session_state.services = initialize_services()
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'selected_movie' not in st.session_state:
        st.session_state.selected_movie = None
    if 'selected_theater' not in st.session_state:
        st.session_state.selected_theater = None
    if 'selected_show' not in st.session_state:
        st.session_state.selected_show = None
    if 'selected_seats' not in st.session_state:
        st.session_state.selected_seats = []


def home_page():
    """Home page with browse movies"""
    st.title("🎬 BookMyShow")
    st.markdown("Your Ultimate Movie Ticket Booking Platform")
    
    services = st.session_state.services
    
    # Display featured movies
    st.subheader("Featured Movies")
    
    movies = services['movie_service'].get_all_movies()
    
    if movies:
        cols = st.columns(3)
        for idx, movie in enumerate(movies):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.image(movie.poster_url, use_container_width=True)
                    st.markdown(f"### {movie.title}")
                    st.markdown(f"⭐ {movie.rating}/10")
                    st.markdown(f"**Genre:** {movie.genre}")
                    st.markdown(f"**Duration:** {movie.duration} mins")
                    st.markdown(f"**Director:** {movie.director}")
                    
                    if st.button("Book Tickets", key=f"btn_{movie.movie_id}"):
                        st.session_state.selected_movie = movie
                        st.switch_page("pages/book_tickets.py")
    else:
        st.info("No movies available at the moment")


def login_page():
    """Login/Registration page"""
    st.title("🔐 Login / Register")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    services = st.session_state.services
    user_service = services['user_service']
    
    with tab1:
        st.subheader("Login to Your Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            if email and password:
                user = user_service.authenticate_user(email, password)
                if user:
                    st.session_state.current_user = user
                    st.success(f"Welcome back, {user.name}!")
                    st.switch_page("pages/my_bookings.py")
                else:
                    st.error("Invalid email or password")
            else:
                st.warning("Please enter email and password")
    
    with tab2:
        st.subheader("Create New Account")
        name = st.text_input("Full Name", key="register_name")
        email = st.text_input("Email", key="register_email")
        phone = st.text_input("Phone Number", key="register_phone")
        password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Register", key="register_btn"):
            if name and email and phone and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    user = user_service.create_user(name, email, phone, password)
                    st.session_state.current_user = user
                    st.success(f"Account created successfully! Welcome, {user.name}!")
                    st.info("Redirecting to bookings page...")
                    st.switch_page("pages/my_bookings.py")
            else:
                st.warning("Please fill in all fields")


def main():
    """Main application"""
    # Page configuration
    st.set_page_config(
        page_title="BookMyShow",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🎬 BookMyShow")
        st.divider()
        
        if st.session_state.current_user:
            st.success(f"Logged in as: {st.session_state.current_user.name}")
            st.divider()
            
            page = st.radio(
                "Navigation",
                ["Home", "Book Tickets", "My Bookings", "Logout"],
                key="nav_radio"
            )
            
            if page == "Home":
                st.switch_page("pages/home.py")
            elif page == "Book Tickets":
                st.switch_page("pages/book_tickets.py")
            elif page == "My Bookings":
                st.switch_page("pages/my_bookings.py")
            elif page == "Logout":
                st.session_state.current_user = None
                st.success("Logged out successfully!")
                st.switch_page("pages/home.py")
        else:
            page = st.radio(
                "Navigation",
                ["Home", "Login/Register"],
                key="nav_radio_guest"
            )
            
            if page == "Home":
                st.switch_page("pages/home.py")
            elif page == "Login/Register":
                st.switch_page("pages/login.py")
        
        st.divider()
        st.markdown("### About")
        st.info("BookMyShow - Your ultimate movie booking platform")
    
    # Show appropriate page
    nav = st.query_params.get("page", ["home"])[0]
    
    if nav == "home":
        home_page()
    elif nav == "login":
        login_page()
    else:
        home_page()


if __name__ == "__main__":
    main()
