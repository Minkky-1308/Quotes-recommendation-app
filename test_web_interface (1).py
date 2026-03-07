from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

# Configuration
WEB_URL = "http://localhost:8000"
WAIT_TIME = 10
TEST_MESSAGES = [
    "hello",
    "give me a motivational quote",
    "tell me a joke",
    "goodbye",
    "what's up"
]

class WebInterfaceTester:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.results = []
        
    def setup_driver(self):
        """Initialize Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in background
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(WAIT_TIME)
        
    def teardown_driver(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            
    def test_connectivity(self):
        """Test 1: Verify frontend-backend connectivity."""
        print("🔍 Testing Connectivity...")
        try:
            self.driver.get(self.url)
            time.sleep(2)
            
            # Check if page loads
            if "Chatbot" in self.driver.title:
                print("✅ PASS: Page loaded successfully")
                return True
            else:
                print("❌ FAIL: Page title incorrect")
                return False
        except Exception as e:
            print(f"❌ FAIL: {str(e)}")
            return False
            
    def test_message_delivery(self):
        """Test 2: Verify real-time response delivery."""
        print("🔍 Testing Message Delivery...")
        passed = 0
        failed = 0
        
        for message in TEST_MESSAGES:
            try:
                # Find input field
                input_field = WebDriverWait(self.driver, WAIT_TIME).until(
                    EC.presence_of_element_located((By.ID, "user-input"))
                )
                
                # Send message
                input_field.clear()
                input_field.send_keys(message)
                input_field.send_keys(Keys.ENTER)
                
                # Wait for response
                time.sleep(3)
                
                # Check if response appeared
                messages = self.driver.find_elements(By.CLASS_NAME, "message")
                if len(messages) >= 2:  # At least user + bot message
                    print(f"✅ PASS: '{message}' - Response received")
                    passed += 1
                else:
                    print(f"❌ FAIL: '{message}' - No response")
                    failed += 1
                    
            except Exception as e:
                print(f"❌ FAIL: '{message}' - {str(e)}")
                failed += 1
                
        return passed, failed
        
    def test_message_rendering(self):
        """Test 3: Verify correct rendering of chatbot messages."""
        print("🔍 Testing Message Rendering...")
        
        try:
            # Check for user message styling
            user_messages = self.driver.find_elements(By.CLASS_NAME, "user-message")
            bot_messages = self.driver.find_elements(By.CLASS_NAME, "bot-message")
            
            if len(user_messages) > 0 and len(bot_messages) > 0:
                print("✅ PASS: Messages rendered correctly")
                return True
            else:
                print("❌ FAIL: Messages not rendered properly")
                return False
        except Exception as e:
            print(f"❌ FAIL: {str(e)}")
            return False
            
    def test_stability(self):
        """Test 4: Verify stable performance during continuous interaction."""
        print("🔍 Testing Stability (5 consecutive messages)...")
        
        try:
            for i in range(5):
                input_field = self.driver.find_element(By.ID, "user-input")
                input_field.send_keys(f"test message {i}")
                input_field.send_keys(Keys.ENTER)
                time.sleep(2)
                
            print("✅ PASS: Stable performance maintained")
            return True
        except Exception as e:
            print(f"❌ FAIL: {str(e)}")
            return False
            
    def run_all_tests(self):
        """Run all test cases."""
        print("=" * 50)
        print("🚀 Starting Web Interface Testing")
        print("=" * 50)
        
        self.setup_driver()
        
        results = {
            "connectivity": self.test_connectivity(),
            "message_delivery": self.test_message_delivery(),
            "message_rendering": self.test_message_rendering(),
            "stability": self.test_stability()
        }
        
        self.teardown_driver()
        
        # Print Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        for test, result in results.items():
            if isinstance(result, tuple):
                passed, failed = result
                print(f"{test}: {passed} passed, {failed} failed")
            else:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"{test}: {status}")
        print("=" * 50)
        
        return results

if __name__ == "__main__":
    tester = WebInterfaceTester(WEB_URL)
    tester.run_all_tests()