"""
Book Tickets Page - Select movie, theater, show, and seats
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.database import MovieDatabase, SeatStatus
from backend.services import MovieService, TheaterService, ShowService, BookingService, PaymentService, UserService

st.set_page_config(page_title="Book Tickets - BookMyShow", layout="wide")

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

st.title("🎟️ Book Tickets")

if not st.session_state.current_user:
    st.warning("⚠️ Please login to book tickets")
    if st.button("Go to Login"):
        st.switch_page("pages/03_login.py")
    st.stop()

# Step 1: Select Movie
st.subheader("Step 1: Select Movie")
movies = services['movie_service'].get_all_movies()
movie_options = {m.title: m for m in movies}
selected_movie_title = st.selectbox("Choose a movie:", list(movie_options.keys()), key="movie_select")
selected_movie = movie_options[selected_movie_title]

with st.expander("Movie Details"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(selected_movie.poster_url, use_container_width=True)
    with col2:
        st.markdown(f"### {selected_movie.title}")
        st.markdown(f"**Rating:** ⭐ {selected_movie.rating}/10")
        st.markdown(f"**Genre:** {selected_movie.genre}")
        st.markdown(f"**Duration:** {selected_movie.duration} mins")
        st.markdown(f"**Language:** {selected_movie.language}")
        st.markdown(f"**Director:** {selected_movie.director}")
        st.markdown(f"**Cast:** {', '.join(selected_movie.cast)}")
        st.markdown(f"**Description:** {selected_movie.description}")

st.divider()

# Step 2: Select Theater
st.subheader("Step 2: Select Theater")
theaters = services['theater_service'].get_all_theaters()
theater_options = {f"{t.name} - {t.city}" : t for t in theaters}
selected_theater_name = st.selectbox("Choose a theater:", list(theater_options.keys()), key="theater_select")
selected_theater = theater_options[selected_theater_name]

st.info(f"📍 {selected_theater.location}")

st.divider()

# Step 3: Select Show
st.subheader("Step 3: Select Show Time")
shows = services['show_service'].get_shows_by_movie_and_theater(selected_movie.movie_id, selected_theater.theater_id)

if shows:
    show_options = {}
    for show in shows:
        show_time_str = show.start_time.strftime("%a, %b %d - %I:%M %p")
        available = show.available_seats()
        show_options[f"{show_time_str} | {available} seats available"] = show
    
    selected_show_str = st.selectbox("Choose a show time:", list(show_options.keys()), key="show_select")
    selected_show = show_options[selected_show_str]
    
    st.success(f"✅ {selected_show.available_seats()} seats available")
else:
    st.warning("No shows available for this combination")
    st.stop()

st.divider()

# Step 4: Select Seats
st.subheader("Step 4: Select Seats")

# Create seat layout
available_seats = services['show_service'].get_available_seats(selected_show.show_id)

# Display seat layout in grid
st.markdown("#### Theater Layout")
st.info("🟢 Available | 🔴 Booked")

# Group seats by row
seat_rows = {}
for seat in selected_show.seats:
    if seat.row not in seat_rows:
        seat_rows[seat.row] = []
    seat_rows[seat.row].append(seat)

# Display seats
cols = st.columns(10)
selected_seat_ids = st.session_state.get('selected_seats', [])

for row_label, row_seats in sorted(seat_rows.items()):
    st.write(f"**{row_label}**")
    cols = st.columns(10)
    
    for idx, seat in enumerate(row_seats):
        with cols[idx % 10]:
            if seat.status == SeatStatus.AVAILABLE:
                if st.button(
                    f"{seat.seat_id}",
                    key=f"seat_{seat.seat_id}",
                    help=f"₹{seat.price}",
                    use_container_width=True,
                    type="secondary" if seat.seat_id not in selected_seat_ids else "primary"
                ):
                    if seat.seat_id in selected_seat_ids:
                        selected_seat_ids.remove(seat.seat_id)
                    else:
                        selected_seat_ids.append(seat.seat_id)
                    st.session_state.selected_seats = selected_seat_ids
            else:
                st.button(f"{seat.seat_id}", disabled=True, use_container_width=True)

st.divider()

# Step 5: Review and Payment
if selected_seat_ids:
    st.subheader("Step 5: Review & Payment")
    
    selected_seats_obj = [s for s in selected_show.seats if s.seat_id in selected_seat_ids]
    total_price = sum(s.price for s in selected_seats_obj)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Booking Summary")
        st.markdown(f"**Movie:** {selected_movie.title}")
        st.markdown(f"**Theater:** {selected_theater.name}")
        st.markdown(f"**Show Time:** {selected_show.start_time.strftime('%a, %b %d - %I:%M %p')}")
        st.markdown(f"**Selected Seats:** {', '.join(selected_seat_ids)}")
        st.markdown(f"**Number of Seats:** {len(selected_seat_ids)}")
    
    with col2:
        st.markdown("#### Price Breakdown")
        for seat in selected_seats_obj:
            st.markdown(f"**{seat.seat_id}:** ₹{seat.price}")
        st.divider()
        st.markdown(f"### **Total Amount: ₹{total_price}**")
    
    st.divider()
    
    # Payment method selection
    st.markdown("#### Select Payment Method")
    payment_method = st.radio("Choose payment method:", ["Credit/Debit Card", "UPI", "Wallet", "Net Banking"])
    
    # Confirm booking
    if st.button("Confirm & Pay", use_container_width=True, type="primary"):
        with st.spinner("Processing your booking..."):
            # Create booking
            booking = services['booking_service'].create_booking(
                st.session_state.current_user.user_id,
                selected_show.show_id,
                selected_seat_ids
            )
            
            if booking:
                # Process payment
                payment = services['payment_service'].process_payment(
                    booking.booking_id,
                    total_price,
                    payment_method
                )
                
                if payment and payment.status == "success":
                    st.success("✅ Booking confirmed! Redirecting to my bookings...")
                    st.balloons()
                    st.session_state.selected_seats = []
                    st.switch_page("pages/02_my_bookings.py")
                else:
                    st.error("❌ Payment failed. Please try again.")
            else:
                st.error("❌ Booking failed. Please try again.")
else:
    st.info("👆 Please select seats to proceed")
