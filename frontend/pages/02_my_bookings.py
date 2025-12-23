"""
My Bookings Page - View and manage user bookings
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.database import MovieDatabase, BookingStatus
from backend.services import (
    MovieService, TheaterService, ShowService, 
    BookingService, PaymentService, UserService
)

st.set_page_config(page_title="My Bookings - BookMyShow", layout="wide")

# Initialize services
if 'services' not in st.session_state:
    db = MovieDatabase()
    show_service = ShowService(db)
    st.session_state.services = {
        'db': db,
        'movie_service': MovieService(db),
        'theater_service': TheaterService(db),
        'show_service': show_service,
        'booking_service': BookingService(db, show_service),
        'payment_service': PaymentService(db),
        'user_service': UserService(db),
    }

services = st.session_state.services

st.title("🎫 My Bookings")

if not st.session_state.current_user:
    st.warning("⚠️ Please login to view your bookings")
    if st.button("Go to Login"):
        st.switch_page("pages/03_login.py")
    st.stop()

user = st.session_state.current_user
bookings = services['booking_service'].get_user_bookings(user.user_id)

if bookings:
    st.subheader(f"Your Bookings ({len(bookings)})")
    st.divider()
    
    # Filter bookings
    filter_status = st.selectbox(
        "Filter by status:",
        ["All", "Confirmed", "Pending", "Cancelled"],
        key="booking_filter"
    )
    
    filtered_bookings = bookings
    if filter_status != "All":
        filtered_bookings = [b for b in bookings if b.status.value == filter_status.lower()]
    
    if filtered_bookings:
        for booking in filtered_bookings:
            show = services['show_service'].get_show_details(booking.show_id)
            movie = services['movie_service'].get_movie_details(show.movie_id)
            theater = services['theater_service'].get_theater_details(show.theater_id)
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.image(movie.poster_url, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {movie.title}")
                    st.markdown(f"**Theater:** {theater.name}")
                    st.markdown(f"**Location:** {theater.location}")
                    st.markdown(f"**Show Time:** {show.start_time.strftime('%a, %b %d - %I:%M %p')}")
                    
                    # Seats
                    seats_str = ", ".join([detail.seat_id for detail in booking.booking_details])
                    st.markdown(f"**Seats:** {seats_str}")
                
                with col3:
                    # Status badge
                    if booking.status == BookingStatus.CONFIRMED:
                        st.success(f"✅ {booking.status.value.upper()}")
                    elif booking.status == BookingStatus.PENDING:
                        st.warning(f"⏳ {booking.status.value.upper()}")
                    else:
                        st.error(f"❌ {booking.status.value.upper()}")
                    
                    st.divider()
                    st.markdown(f"**Booking ID:** {booking.booking_id}")
                    st.markdown(f"**Booked On:** {booking.booking_date.strftime('%b %d, %Y')}")
                    st.markdown(f"**Total Amount:** ₹{booking.total_price}")
                
                st.divider()
                
                # Actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("View Details", key=f"view_{booking.booking_id}", use_container_width=True):
                        st.markdown(f"### Booking Details")
                        st.json({
                            "booking_id": booking.booking_id,
                            "movie": movie.title,
                            "theater": theater.name,
                            "show_time": show.start_time.strftime('%a, %b %d - %I:%M %p'),
                            "seats": seats_str,
                            "total_price": booking.total_price,
                            "status": booking.status.value,
                            "payment_method": booking.payment_method
                        })
                
                with col2:
                    if booking.status != BookingStatus.CANCELLED:
                        if st.button("Cancel Booking", key=f"cancel_{booking.booking_id}", use_container_width=True):
                            if services['booking_service'].cancel_booking(booking.booking_id):
                                st.success("✅ Booking cancelled successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to cancel booking")
                
                st.markdown("---")
    else:
        st.info("No bookings found with the selected filter")
else:
    st.info("📭 You haven't booked any tickets yet")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Browse Movies", use_container_width=True):
            st.switch_page("pages/00_home.py")
    with col2:
        if st.button("Book Tickets", use_container_width=True):
            st.switch_page("pages/01_book_tickets.py")

st.divider()

# User profile section
with st.expander("👤 My Profile"):
    st.markdown(f"**Name:** {user.name}")
    st.markdown(f"**Email:** {user.email}")
    st.markdown(f"**Phone:** {user.phone}")
    st.markdown(f"**Member Since:** {user.created_at.strftime('%B %d, %Y')}")
    st.markdown(f"**Total Bookings:** {len(bookings)}")
    
    if len(bookings) > 0:
        total_spent = sum(b.total_price for b in bookings)
        st.markdown(f"**Total Amount Spent:** ₹{total_spent}")
