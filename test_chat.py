import requests
import json

# Test 1: Simple message
response = requests.post('http://localhost:5000/chat', json={
    'message': 'who is your boss?',
    'conversation_history': []
})

print("=== TEST 1: who is your boss? ===")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

# Test 2: Developer question
response2 = requests.post('http://localhost:5000/chat', json={
    'message': 'who is your developer?',
    'conversation_history': []
})

print("=== TEST 2: who is your developer? ===")
print(f"Status: {response2.status_code}")
print(f"Response: {response2.json()}")
