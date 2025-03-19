from flask import Flask, request, jsonify, render_template
import openai
import stripe
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app) # Allow frontend requests

# Load API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY") # Your Stripe Secret Key

# Manually set API Key (only for local testing, REMOVE this for deployment)
if not openai.api_key:
    openai.api_key = "your-openai-api-key-here"

if not stripe.api_key:
    stripe.api_key = "your-stripe-secret-key-here"


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


# Route for creating a Stripe Checkout session
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'AI Content Ideas'},
                    'unit_amount': 500, # $5.00 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="https://your-app-name.onrender.com/success",
            cancel_url="https://your-app-name.onrender.com/cancel",
        )
        return jsonify({"url": session.url})

    except Exception as e:
        return jsonify(error=str(e)), 500


# Success and Cancel routes
@app.route('/success')
def success():
    return "Payment Successful! Thank you for your purchase."

@app.route('/cancel')
def cancel():
    return "Payment Cancelled. Please try again."


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
