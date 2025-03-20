from flask import Flask, request, jsonify, render_template
import openai
import stripe
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set secret key for Flask sessions
app.secret_key = "supersecretkey"

# Load API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY") # Your Stripe Secret Key

def generate_ai_ideas(niche, platform):
    """Generate AI-generated ideas for a given niche and platform."""
    try:
        if not openai.api_key:
            return ["❌ ERROR: OpenAI API key is missing!"]

        prompt = f"Generate 5 viral content ideas for {platform} in the {niche} niche."

        response = openai.ChatCompletion.create(
            model="gpt-4", # Use "gpt-4" or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are an expert content creator."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract responses correctly
        ideas = response["choices"][0]["message"]["content"].strip().split("\n")
        return ideas

    except Exception as e:
        return [f"❌ ERROR: {str(e)}"]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_content():
    """Generate new ideas using OpenAI and return them instantly."""
    try:
        data = request.json
        niche = data.get("niche", "general")
        platform = data.get("platform", "Instagram")

        ideas = generate_ai_ideas(niche, platform)

        return jsonify({"status": "success", "ideas": ideas})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create a Stripe checkout session."""
    try:
        niche = request.json.get("niche", "general")
        platform = request.json.get("platform", "Instagram")

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
            success_url=f"https://quickfix-xidb.onrender.com/success?niche={niche}&platform={platform}",
            cancel_url="https://quickfix-xidb.onrender.com/cancel",
        )
        return jsonify({"url": session.url})

    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/success')
def success():
    """Generate fresh AI ideas on the success page after payment."""
    niche = request.args.get("niche", "general")
    platform = request.args.get("platform", "Instagram")

    ideas = generate_ai_ideas(niche, platform)
    return render_template("success.html", ideas=ideas)

@app.route('/cancel')
def cancel():
    return render_template("cancel.html")

if __name__ == '__main__':
    app.run(debug=True)
