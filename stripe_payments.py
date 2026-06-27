import stripe

stripe.api_key = "YOUR_SECRET_KEY"

# Create checkout session
def create_checkout_session(plan, success_url, cancel_url):
    prices = {
        "silver": 500,  # £5.00
        "gold": 1500    # £15.00
    }

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "gbp",
                "product_data": {
                    "name": f"FIFA AI {plan.upper()} Plan",
                },
                "unit_amount": prices[plan],
            },
            quantity=1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return session.url