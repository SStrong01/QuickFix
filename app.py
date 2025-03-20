from flask import Flask, request, jsonify, render_template
import openai
import stripe
from flask_cors import CORS
import os
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set a secret key for Flask sessions
app.secret_key = "supersecretkey"

# Load API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY") # Your Stripe Secret Key

# File to store AI-generated ideas
IDEAS_FILE = "ideas.json"

def ensure_ideas_file():
    """Ensure that the ideas.json file exists, creating it if necessary."""
    if not os.path.exists(IDEAS_FILE):
        with open(IDEAS_FILE, "w") as f:
            json.dump([], f) # Create an empty JSON file

def save_ideas(ideas):
    """Save AI-generated ideas to a file for later retrieval."""
    ensure_ideas_file()
    with open(IDEAS_FILE, "w") as f:
        json.dump(ideas, f)

def load_ideas():
    """Load AI-generated ideas from the file, ensuring it exists."""
    ensure_ideas_file()
    try:
        with open(IDEAS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading ideas: {e}")
        return []

def generate_ai_ideas(niche, platform):
    """Generate new AI ideas using OpenAI API."""
    try:
        if not openai.api_key:
            return ["❌ ERROR: OpenAI API key is missing!"]

        prompt = f"Generate 5 viral content ideas for {platform} in the {niche} niche."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert content creator."},
                {"role": "user", "content": prompt}
            ]
        )

        ideas = response["choices"][0]["message"]["content"].strip().split("\n")
        return ideas

    except Exception as e:
        return [f"❌ ERROR: {str(e)}"]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_content():
    """Generate new ideas using OpenAI and save them."""
    try:
        data = request.json
        niche = data.get("niche", "general")
        platform = data.get("platform", "Instagram")

        ideas = generate_ai_ideas(niche, platform)

        # ✅ Save NEWLY generated ideas
        save_ideas(ideas)

        return jsonify({"status": "success", "ideas": ideas})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create a Stripe checkout session."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'AI Content Ideas'},
                    'unit_amount': 500, # $5.00
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="https://quickfix-xidb.onrender.com/success",
            cancel_url="https://quickfix-xidb.onrender.com/cancel",
        )
        return jsonify({"url": session.url})

    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/success')
def success():
    """Retrieve AI-generated ideas after payment."""
    ideas = load_ideas()
    print(f"✅ Loaded AI ideas successfully: {ideas}") # Debugging output
    return render_template("success.html", ideas=ideas)

@app.route('/cancel')
def cancel():
    return render_template("cancel.html")

if __name__ == '__main__':
    app.run(debug=True)
