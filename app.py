from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load local .env (for development)
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# Gemini API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not set in environment")

@app.route('/validate-idea', methods=['POST'])
def validate_idea():
    data = request.get_json()
    idea_text = data.get('text', '').strip()

    if not idea_text:
        return jsonify({'error': 'No idea text provided'}), 400

    try:
        # Call Gemini API
        response = requests.post(
            "https://gemini-api.example.com/validate",  # Replace with actual endpoint
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GEMINI_API_KEY}"
            },
            json={"text": idea_text}
        )

        response.raise_for_status()
        result = response.json()

        # Return the Gemini response to frontend
        return jsonify(result)

    except requests.exceptions.RequestException as e:
        print("Gemini API error:", e)
        return jsonify({'error': 'Failed to validate idea'}), 500

if __name__ == "__main__":
    app.run(debug=True)
