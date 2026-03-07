import requests
import json

class IntegrationTester:
    def __init__(self, rasa_url, web_url):
        self.rasa_url = rasa_url
        self.web_url = web_url
        
    def test_full_flow(self):
        """Test complete flow: Web → Flask → Rasa → Web."""
        print("🔗 Testing Full Integration Flow...")
        
        # Step 1: Send message to Flask
        flask_url = f"{self.web_url}/chat"
        payload = {"message": "hello"}
        
        try:
            response = requests.post(flask_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "response" in data:
                    print(f"✅ PASS: Full flow successful")
                    print(f"   Input: {payload['message']}")
                    print(f"   Output: {data['response']}")
                    return True
                else:
                    print("❌ FAIL: Invalid response format")
                    return False
            else:
                print(f"❌ FAIL: Flask returned status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ FAIL: {str(e)}")
            return False

if __name__ == "__main__":
    tester = IntegrationTester(
        rasa_url="http://localhost:5005",
        web_url="http://localhost:8000"
    )
    tester.test_full_flow()