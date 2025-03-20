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

# Path for storing AI-generated ideas
IDEAS_FILE = "ideas.json"

def save_ideas(ideas):
    """Save AI-generated ideas to a file for later retrieval."""
    with open(IDEAS_FILE, "w") as f:
        json.dump(ideas, f)

def load_ideas():
    """Load AI-generated ideas from the file."""
    try:
        with open(IDEAS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        niche = data.get("niche", "general")
        platform = data.get("platform", "Instagram")

        if not openai.api_key:
            return jsonify({"status": "error", "message": "OpenAI API key is missing!"})

        prompt = f"Generate 5 viral content ideas for {platform} in the {niche} niche."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert content creator."},
                {"role": "user", "content": prompt}
            ]
        )

        ideas = response["choices"][0]["message"]["content"].strip().split("\n")

        # ✅ Save ideas before payment
        save_ideas(ideas)

        return jsonify({"status": "success", "ideas": ideas})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
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
    ideas = []
    
    # ✅ Load ideas correctly after payment
    try:
        with open(IDEAS_FILE, "r") as f:
            ideas = json.load(f)
    except Exception as e:
        print(f"Error loading ideas: {e}") # Debugging output

    return render_template("success.html", ideas=ideas)

@app.route('/cancel')
def cancel():
    return render_template("cancel.html")

if __name__ == '__main__':
    app.run(debug=True)
