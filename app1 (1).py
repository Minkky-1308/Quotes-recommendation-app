from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Rasa Server Configuration
RASA_SERVER_URL = "http://localhost:5005"
RASA_WEBHOOK_URL = f"{RASA_SERVER_URL}/webhooks/rest/webhook"

@app.route('/')
def index():
    """Serve the main chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and send to Rasa API."""
    try:
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'response': 'Please enter a message.'}), 400
        
        # Send message to Rasa REST API
        payload = {
            "message": user_message,
            "sender": "user"
        }
        
        response = requests.post(RASA_WEBHOOK_URL, json=payload)
        
        if response.status_code == 200:
            rasa_response = response.json()
            # Extract the first response message
            if rasa_response:
                bot_message = rasa_response[0].get('text', 'No response received.')
                return jsonify({'response': bot_message})
            else:
                return jsonify({'response': 'No response received.'})
        else:
            return jsonify({'response': 'Server error. Please try again.'}), 500
            
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)