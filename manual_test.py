#!/usr/bin/env python3
"""
Manual test script to verify specific functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_login_and_pages():
    """Test login and page access manually"""
    session = requests.Session()
    
    print("🔍 Testing Admin Login and Pages...")
    
    # Test login
    login_data = {
        'login_id': 'ODJODO20240001',
        'password': 'admin123'
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data)
    print(f"Login response: {response.status_code}")
    
    if response.status_code == 200:
        # Test dashboard
        dashboard = session.get(f"{BASE_URL}/dashboard")
        print(f"Dashboard: {dashboard.status_code}")
        
        # Test time-off page
        try:
            time_off = session.get(f"{BASE_URL}/time_off")
            print(f"Time-off page: {time_off.status_code}")
            if time_off.status_code != 200:
                print(f"Time-off error: {time_off.text[:200]}")
        except Exception as e:
            print(f"Time-off error: {e}")
        
        # Test check-in
        try:
            checkin = session.post(f"{BASE_URL}/check_in")
            print(f"Check-in: {checkin.status_code}")
            if checkin.status_code == 200:
                result = checkin.json()
                print(f"Check-in result: {result}")
        except Exception as e:
            print(f"Check-in error: {e}")

if __name__ == "__main__":
    test_login_and_pages()