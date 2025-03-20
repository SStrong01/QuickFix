from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import openai
import stripe
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_secret_key")

# Load API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_content():
    """Generate AI content dynamically based on user input."""
    try:
        # Ensure Content-Type is JSON
        if request.content_type != "application/json":
            return jsonify({"status": "error", "message": "Content-Type must be 'application/json'"}), 415

        # Parse JSON request data
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON data"}), 400

        niche = data.get("niche", "general")
        platform = data.get("platform", "Instagram")

        # Generate AI content using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Give me 5 viral {platform} ideas for {niche}"}]
        )

        ideas = response["choices"][0]["message"]["content"].strip().split("\n")

        # Save generated ideas in session to retrieve after payment
        session["ai_ideas"] = ideas  

        return jsonify({"status": "success", "ideas": ideas})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create a Stripe checkout session for payment."""
    try:
        # Parse request JSON
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid request"}), 400

        # Set Stripe session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Premium AI Content Ideas'
                    },
                    'unit_amount': 5000, # $50.00 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('home', _external=True),
        )

        return jsonify({"url": checkout_session.url})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/success')
def success():
    """Display success page with AI-generated content."""
    ideas = session.get("ai_ideas", []) # Retrieve stored ideas
    return render_template("success.html", ideas=ideas)

if __name__ == '__main__':
    app.run(debug=True)
