#!/bin/bash
# BookMyShow - Startup Script for Linux/Mac

echo ""
echo "================================"
echo "  BookMyShow Application"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1/3] Checking Python installation..."
python3 --version

echo ""
echo "[2/3] Installing/Updating dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[3/3] Starting BookMyShow application..."
echo ""
echo "================================"
echo "  Streamlit is starting..."
echo "  Open your browser to:"
echo "  http://localhost:8501"
echo "================================"
echo ""

streamlit run frontend/app.py
