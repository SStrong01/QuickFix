from flask import Flask, request, jsonify, render_template, session
import openai
import stripe
from flask_cors import CORS
import os
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app) # Allow frontend requests

# Set a secret key for sessions (optional)
app.secret_key = "supersecretkey"

# Load API keys
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
    ideas = load_ideas()
    return render_template("index.html", ideas=ideas)

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

        # Save ideas to a file before payment
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
    # Retrieve stored AI-generated ideas
    ideas = load_ideas()

    return f"""
    <html>
    <head>
        <title>Payment Successful</title>
        <style>
            body {{
                text-align: center;
                background: linear-gradient(to right, #28a745, #ff69b4);
                font-family: Arial, sans-serif;
                color: white;
                padding: 50px;
            }}
            h1 {{
                font-size: 28px;
                margin-bottom: 20px;
            }}
            .btn {{
                background-color: #fff;
                color: #28a745;
                padding: 12px 20px;
                border-radius: 5px;
                font-size: 18px;
                text-decoration: none;
                font-weight: bold;
            }}
            .btn:hover {{
                background-color: #ddd;
            }}
            .ideas-box {{
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>✅ Payment Successful! Thank you for your purchase.</h1>
        <p>Here are your AI-generated ideas:</p>
        <div class="ideas-box">
            <ul>
                {''.join(f'<li>{idea}</li>' for idea in ideas)}
            </ul>
        </div>
        <p>Click below to generate more ideas!</p>
        <a href="/" class="btn">🔙 Go Back to AI Generator</a>
    </body>
    </html>
    """

@app.route('/cancel')
def cancel():
    return '''
    <html>
    <head>
        <title>Payment Canceled</title>
        <style>
            body {
                text-align: center;
                background: linear-gradient(to right, #ff0000, #ff69b4);
                font-family: Arial, sans-serif;
                color: white;
                padding: 50px;
            }
            h1 {
                font-size: 28px;
                margin-bottom: 20px;
            }
            .btn {
                background-color: #fff;
                color: #ff0000;
                padding: 12px 20px;
                border-radius: 5px;
                font-size: 18px;
                text-decoration: none;
                font-weight: bold;
            }
            .btn:hover {
                background-color: #ddd;
            }
        </style>
    </head>
    <body>
        <h1>❌ Payment Canceled</h1>
        <p>Your payment was canceled. Click below to try again.</p>
        <a href="/" class="btn">🔙 Go Back</a>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
