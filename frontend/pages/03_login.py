"""
Login/Register Page
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.database import MovieDatabase
from backend.services import UserService

st.set_page_config(page_title="Login - BookMyShow", layout="centered")

# Initialize services
if 'services' not in st.session_state:
    db = MovieDatabase()
    st.session_state.services = {
        'db': db,
        'user_service': UserService(db),
    }

services = st.session_state.services

st.title("🎬 BookMyShow")
st.markdown("---")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.subheader("Login to Your Account")
    
    email = st.text_input("Email Address", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login", use_container_width=True, type="primary"):
        if email and password:
            user = services['user_service'].authenticate_user(email, password)
            if user:
                st.session_state.current_user = user
                st.success(f"✅ Welcome back, {user.name}!")
                st.switch_page("pages/my_bookings.py")
            else:
                st.error("❌ Invalid email or password")
        else:
            st.warning("⚠️ Please enter email and password")
    
    st.divider()
    st.markdown("**Demo Credentials:**")
    st.code("Email: demo@gmail.com\nPassword: demo123", language="text")

with tab2:
    st.subheader("Create New Account")
    
    name = st.text_input("Full Name", placeholder="Enter your full name")
    email = st.text_input("Email Address", placeholder="Enter your email", key="reg_email")
    phone = st.text_input("Phone Number", placeholder="Enter your phone number")
    password = st.text_input("Password", type="password", placeholder="Create a password", key="reg_password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    
    agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
    
    if st.button("Register", use_container_width=True, type="primary"):
        if name and email and phone and password and confirm_password:
            if password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters long")
            elif not agree_terms:
                st.error("❌ Please agree to the Terms of Service")
            else:
                user = services['user_service'].create_user(name, email, phone, password)
                st.session_state.current_user = user
                st.success(f"✅ Account created successfully!")
                st.info(f"Welcome {user.name}! Redirecting to bookings page...")
                st.switch_page("pages/my_bookings.py")
        else:
            st.warning("⚠️ Please fill in all fields")

st.divider()
st.markdown("### New User? Create an account above! →")
