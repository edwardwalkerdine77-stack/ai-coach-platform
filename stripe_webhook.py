from flask import Flask, request
import stripe
from supabase import create_client

app = Flask(__name__)

# ---------------- STRIPE ----------------
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"
endpoint_secret = "YOUR_STRIPE_WEBHOOK_SECRET"

# ---------------- SUPABASE ----------------
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------- WEBHOOK ----------------
@app.route("/webhook", methods=["POST"])
def webhook():

    payload = request.data
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

    except Exception as e:
        return str(e), 400

    # ---------------- PAYMENT SUCCESS ----------------
    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        # Get plan from metadata
        plan = session.get("metadata", {}).get("plan", "bronze")

        # Get email (or username mapping)
        customer_email = session.get("customer_details", {}).get("email")

        # UPDATE USER IN SUPABASE
        supabase.table("users") \
            .update({"plan": plan}) \
            .eq("email", customer_email) \
            .execute()

        print(f"Upgraded {customer_email} to {plan}")

    return "success", 200


if __name__ == "__main__":
    app.run(port=4242)