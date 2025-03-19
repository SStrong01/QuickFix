from flask import Flask, request, jsonify, render_template
import openai
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app) # Allow frontend requests

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Manually set API Key (only for local testing, REMOVE this for deployment)
if not openai.api_key:
    openai.api_key = "your-api-key-here" # Replace with your actual API key

@app.route('/')
def home():
    return render_template("index.html") # Serve frontend

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        niche = data.get("niche", "general")
        platform = data.get("platform", "Instagram")

        # Ensure API key is available
        if not openai.api_key:
            return jsonify({"status": "error", "message": "OpenAI API key is missing!"})

        # Generate AI prompt
        prompt = f"Generate 5 viral content ideas for {platform} in the {niche} niche."

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert content creator."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract generated ideas
        ideas = response["choices"][0]["message"]["content"].strip().split("\n")

        return jsonify({"status": "success", "ideas": ideas})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
