from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import openai
import os
import stripe

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/checkout", methods=["POST"])
def checkout():
    niche = request.json.get("niche")
    platform = request.json.get("platform")

    if not niche or not platform:
        return jsonify({"error": "Missing fields"}), 400

    # Save data temporarily in session
    session["niche"] = niche
    session["platform"] = platform

    try:
        session_data = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "AI Content Ideas"},
                    "unit_amount": 1000
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for("success", _external=True),
            cancel_url=url_for("index", _external=True)
        )
        return jsonify({"checkout_url": session_data.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/success")
def success():
    niche = session.get("niche")
    platform = session.get("platform")

    if not niche or not platform:
        return redirect(url_for("index"))

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": f"Generate 5 viral content ideas for {platform} in the {niche} niche."
                }
            ]
        )
        ideas_text = response["choices"][0]["message"]["content"]
        ideas = [idea.strip("-• ") for idea in ideas_text.strip().split("\n") if idea.strip()]
        return render_template("success.html", ideas=ideas)
    except Exception as e:
        return render_template("success.html", ideas=[])

