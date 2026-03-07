import subprocess
import sys
import re

# Configuration
MIN_ACCURACY_THRESHOLD = 0.80  # Minimum expected accuracy (80%)
MODEL_PATH = "models"
TEST_DATA_FILE = "test_stories.yml"

def run_rasa_test():
    """Executes the rasa test command and captures output."""
    print(f"Running automated tests against {TEST_DATA_FILE}...")
    
    try:
        # Run rasa test command
        result = subprocess.run(
            ["rasa", "test", "--test-data-file", TEST_DATA_FILE, "--model", MODEL_PATH],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Rasa test command failed.")
            print(result.stderr)
            return False
            
        return result.stdout
        
    except FileNotFoundError:
        print("❌ 'rasa' command not found. Ensure Rasa is installed.")
        return False

def parse_accuracy(output):
    """Extracts accuracy from the Rasa test output."""
    # Regex to find accuracy percentage (e.g., "Accuracy: 0.95")
    match = re.search(r"Accuracy:\s*([\d.]+)", output)
    if match:
        return float(match.group(1))
    return 0.0

def main():
    output = run_rasa_test()
    
    if not output:
        sys.exit(1)

    accuracy = parse_accuracy(output)
    print(f"\n📊 Test Results:")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Threshold: {MIN_ACCURACY_THRESHOLD:.2%}")

    if accuracy >= MIN_ACCURACY_THRESHOLD:
        print("✅ PASS: Model meets quality standards.")
        sys.exit(0)
    else:
        print("❌ FAIL: Model accuracy dropped below threshold (Regression detected).")
        sys.exit(1)

if __name__ == "__main__":
    main()