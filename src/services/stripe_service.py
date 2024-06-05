import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

def create_session(user_id, price_id):
    url = os.environ.get("STRIPE_SUCCESS_REDIRECT_URL")
    client_url = os.environ.get("CLIENT_URL")
    session = stripe.checkout.Session.create(
            success_url=f"{url}?user_id={user_id}&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{client_url}/checkout/cancel",
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            mode="subscription",
        )
    
    return session

def get_session(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    return session

def get_subscription(subscription_id):
    subscription = stripe.Subscription.retrieve(subscription_id)
    return subscription