import requests
import json

# Configuration
RASA_SERVER_URL = "http://localhost:5005"
MODEL_PATH = "models"  # Path to your trained model

# Test Cases based on your description
TEST_CASES = [
    {
        "name": "Greeting - Hello",
        "input": "hello",
        "expected_intent": "greet"
    },
    {
        "name": "Greeting - Hi",
        "input": "hi",
        "expected_intent": "greet"
    },
    {
        "name": "Farewell - Goodbye",
        "input": "goodbye",
        "expected_intent": "goodbye"
    },
    {
        "name": "Quote - Motivational",
        "input": "give me a motivational quote",
        "expected_intent": "request_motivational"
    },
    {
        "name": "Quote - Inspirational",
        "input": "inspire me",
        "expected_intent": "request_inspirational"
    },
    {
        "name": "Quote - Humorous",
        "input": "tell me a joke",
        "expected_intent": "request_humorous"
    },
    {
        "name": "Quote - Love",
        "input": "i need a love quote",
        "expected_intent": "request_love"
    },
    {
        "name": "Quote - Success",
        "input": "success quote",
        "expected_intent": "request_success"
    },
    {
        "name": "Variation - What's up",
        "input": "what's up",
        "expected_intent": "greet"
    }
]

def send_message(message):
    """Sends a message to the Rasa server and returns the response."""
    url = f"{RASA_SERVER_URL}/webhooks/rest/webhook"
    payload = {
        "message": message,
        "sender": "test_user"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None

def run_tests():
    print("Starting Automated Chatbot Testing...\n")
    passed = 0
    failed = 0

    for case in TEST_CASES:
        print(f"Testing: {case['name']}")
        print(f"Input: '{case['input']}'")
        
        response = send_message(case['input'])
        
        if response:
            # Rasa returns a list of messages
            if response:
                intent = response[0].get('entities', [{}])[0].get('intent', {}).get('name', 'unknown')
                # Note: Rasa 3.x returns intents in 'intent' field of the message
                # Adjust based on your Rasa version response structure
                detected_intent = response[0].get('intent', {}).get('name', 'unknown')
                
                if detected_intent == case['expected_intent']:
                    print(f"✅ PASS - Intent: {detected_intent}")
                    passed += 1
                else:
                    print(f"❌ FAIL - Expected: {case['expected_intent']}, Got: {detected_intent}")
                    failed += 1
            else:
                print("❌ FAIL - No response received")
                failed += 1
        else:
            print("❌ FAIL - Server Error")
            failed += 1
        
        print("-" * 30)

    print(f"\nTesting Complete.")
    print(f"Passed: {passed}/{len(TEST_CASES)}")
    print(f"Failed: {failed}/{len(TEST_CASES)}")

if __name__ == "__main__":
    run_tests()