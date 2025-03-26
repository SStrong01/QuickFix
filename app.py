from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
import openai
import stripe
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Set API keys from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_ideas():
    data = request.get_json()
    niche = data.get("niche")
    platform = data.get("platform")

    if not niche or not platform:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are an expert social media strategist."},
                {"role": "user", "content": f"Generate viral content ideas for {platform} in the {niche} niche."}
            ]
        )

        ideas_text = response['choices'][0]['message']['content']
        ideas = ideas_text.strip().split("\n")

        # Save ideas in session to show after payment
        session['generated_ideas'] = ideas
        session.modified = True

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        session_data = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'AI-Generated Content Ideas'},
                    'unit_amount': 1000, # $10 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('index', _external=True)
        )
        return jsonify({"checkout_url": session_data.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/success')
def success():
    ideas = session.get('generated_ideas', [])
    return render_template('success.html', ideas=ideas)

if __name__ == '__main__':
    app.run(debug=True)
