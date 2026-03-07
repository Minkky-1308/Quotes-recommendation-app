import requests
import time
import statistics

# Configuration
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
TEST_MESSAGES = [
    "hello",
    "give me a motivational quote",
    "tell me a joke",
    "goodbye"
]
NUM_REQUESTS = 10

def test_response_time():
    """Test response time for multiple requests."""
    print("📊 Performance Testing...")
    response_times = []
    
    for i in range(NUM_REQUESTS):
        start_time = time.time()
        
        try:
            payload = {
                "message": TEST_MESSAGES[i % len(TEST_MESSAGES)],
                "sender": "test_user"
            }
            
            response = requests.post(RASA_API_URL, json=payload, timeout=10)
            
            if response.status_code == 200:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to ms
                response_times.append(response_time)
                print(f"✅ Request {i+1}: {response_time:.2f}ms")
            else:
                print(f"❌ Request {i+1}: Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request {i+1}: Error - {str(e)}")
    
    if response_times:
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print("\n📈 Performance Summary:")
        print(f"Average Response Time: {avg_time:.2f}ms")
        print(f"Minimum Response Time: {min_time:.2f}ms")
        print(f"Maximum Response Time: {max_time:.2f}ms")
        
        if avg_time < 2000:  # 2 seconds threshold
            print("✅ PASS: Performance is acceptable")
            return True
        else:
            print("❌ FAIL: Performance is too slow")
            return False
    else:
        print("❌ FAIL: No successful responses")
        return False

if __name__ == "__main__":
    test_response_time()