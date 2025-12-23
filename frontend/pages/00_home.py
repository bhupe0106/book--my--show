"""
Home Page - Browse and search movies
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.database import MovieDatabase
from backend.services import MovieService, TheaterService, ShowService

st.set_page_config(page_title="Home - BookMyShow", layout="wide")

# Initialize services
if 'services' not in st.session_state:
    db = MovieDatabase()
    st.session_state.services = {
        'movie_service': MovieService(db),
        'theater_service': TheaterService(db),
        'show_service': ShowService(db),
        'db': db
    }

services = st.session_state.services

st.title("🏠 Home - BookMyShow")
st.markdown("---")

# Search and filter section
col1, col2 = st.columns([2, 1])

with col1:
    search_query = st.text_input("🔍 Search movies by title or genre...", placeholder="Enter movie name or genre")

with col2:
    sort_by = st.selectbox("Sort by", ["Title", "Rating", "Duration"])

# Get movies
movies = services['movie_service'].get_all_movies()

# Filter by search query
if search_query:
    movies = [m for m in movies if search_query.lower() in m.title.lower() or search_query.lower() in m.genre.lower()]

# Sort
if sort_by == "Rating":
    movies.sort(key=lambda x: x.rating, reverse=True)
elif sort_by == "Duration":
    movies.sort(key=lambda x: x.duration)
else:
    movies.sort(key=lambda x: x.title)

# Display movies
if movies:
    st.subheader(f"Available Movies ({len(movies)})")
    st.markdown("---")
    
    cols = st.columns(3)
    for idx, movie in enumerate(movies):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(movie.poster_url, use_container_width=True)
                st.markdown(f"### {movie.title}")
                
                col_rating, col_lang = st.columns(2)
                with col_rating:
                    st.markdown(f"⭐ **{movie.rating}/10**")
                with col_lang:
                    st.markdown(f"🎙️ {movie.language}")
                
                st.markdown(f"**Genre:** {movie.genre}")
                st.markdown(f"**Duration:** {movie.duration} mins")
                st.markdown(f"**Director:** {movie.director}")
                st.markdown(f"**Cast:** {', '.join(movie.cast[:2])}")
                st.markdown(f"*{movie.description[:100]}...*")
                
                if st.button("Book Now", key=f"book_{movie.movie_id}", use_container_width=True):
                    st.session_state.selected_movie = movie
                    st.switch_page("pages/book_tickets.py")
else:
    st.info("No movies found matching your search")

st.markdown("---")
st.markdown("### 📊 Quick Stats")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Movies", len(services['movie_service'].get_all_movies()))
with col2:
    st.metric("Theaters", len(services['theater_service'].get_all_theaters()))
with col3:
    st.metric("Total Shows", len(services['show_service'].db.shows))
