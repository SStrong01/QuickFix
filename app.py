from flask import Flask, request, jsonify, render_template, redirect, url_for
import openai
import json
import os
import stripe

app = Flask(__name__)

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Stripe API Keys
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
YOUR_DOMAIN = "https://quickfix-xidb.onrender.com"

# Function to generate AI ideas
def generate_ai_ideas(niche, platform):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Give me viral content ideas for {niche} on {platform}"}]
        )
        return response["choices"][0]["message"]["content"].split("\n")
    except Exception as e:
        return [f"Error generating ideas: {str(e)}"]

# Save AI-generated ideas to JSON
def save_ideas(ideas):
    with open("ideas.json", "w") as f:
        json.dump({"ideas": ideas}, f)

# Load AI-generated ideas
def load_ideas():
    try:
        with open("ideas.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"ideas": []}

# Home Page (AI Generator)
@app.route("/")
def index():
    return render_template("index.html")

# Generate AI Ideas (POST Request)
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    niche = data.get("niche")
    platform = data.get("platform")

    if not niche or not platform:
        return jsonify({"error": "Missing input"}), 400

    ideas = generate_ai_ideas(niche, platform)
    save_ideas(ideas) # Save to JSON

    return jsonify({"ideas": ideas})

# Payment Page (Stripe Checkout)
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Premium AI Content Ideas"
                    },
                    "unit_amount": 5000, # $50 in cents
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success",
            cancel_url=YOUR_DOMAIN + "/",
        )
        return jsonify({"url": checkout_session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Success Page (After Payment)
@app.route("/success")
def success():
    return render_template("success.html")

# Fetch AI Ideas after Payment
@app.route("/get_ideas")
def get_ideas():
    return jsonify(load_ideas())

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
