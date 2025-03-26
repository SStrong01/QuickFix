from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import openai
import stripe
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here" # Replace with a secure key

# Set OpenAI + Stripe API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_ideas():
    data = request.get_json()
    niche = data.get('niche')
    platform = data.get('platform')

    if not niche or not platform:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Call OpenAI Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are an AI content idea generator."},
                {"role": "user", "content": f"Generate 7 viral content ideas for {platform} in the {niche} niche."}
            ],
            temperature=0.7
        )

        # Extract and split ideas
        ideas = response.choices[0].message['content'].strip().split('\n')
        ideas = [idea.strip('-•0123456789. ') for idea in ideas if idea.strip()]

        # Save to session
        session['generated_ideas'] = ideas
        session.modified = True

        return jsonify({"ideas": ideas})

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
                    'product_data': {
                        'name': 'AI-Generated Content Ideas',
                    },
                    'unit_amount': 1000, # $10 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('index', _external=True),
        )
        return jsonify({'checkout_url': session_data.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/success')
def success():
    ideas = session.get('generated_ideas', [])
    return render_template('success.html', ideas=ideas)

if __name__ == '__main__':
    app.run(debug=True)
