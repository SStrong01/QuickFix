from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import stripe
import openai
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Set API keys
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-key-here")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "your-stripe-secret-key-here")

# Route for Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Route to Generate AI Ideas
@app.route("/generate", methods=["POST"])
def generate_ideas():
    data = request.json
    niche = data.get("niche", "")
    platform = data.get("platform", "")

    if not niche or not platform:
        return jsonify({"error": "Niche and Platform are required!"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Generate viral content ideas for {platform} in the {niche} niche."}]
        )
        ideas = response["choices"][0]["message"]["content"].split("\n")

        session["ideas"] = ideas # Store ideas in session
        return jsonify({"ideas": ideas})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for Checkout
@app.route("/checkout", methods=["POST"])
def checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "AI Generated Ideas"},
                    "unit_amount": 1000, # $10
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for("success", _external=True),
            cancel_url=url_for("index", _external=True),
        )
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for Success Page
@app.route("/success")
def success():
    ideas = session.get("ideas", [])
    return render_template("success.html", ideas=ideas)

if __name__ == "__main__":
    app.run(debug=True)
