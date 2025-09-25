import requests
import json

API_BASE = 'http://127.0.0.1:5000'

# Test register
reg_data = {
    'username': 'testuser',
    'email': 'test@test.com',
    'password': 'password123'
}

print("Testing /register...")
response = requests.post(f"{API_BASE}/register", json=reg_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test verify-otp (use a fixed OTP for test, but since session is not shared, this won't work in script; for demo, assume OTP from console)
# For now, skip verify and test login after manual register

# Test login (will fail if not registered)
login_data = {
    'username': 'testuser',
    'password': 'password123'
}

print("\nTesting /login...")
response = requests.post(f"{API_BASE}/login", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
