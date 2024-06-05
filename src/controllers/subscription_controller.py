from flask import request, Response, json, Blueprint, redirect
from src.models.subscription_model import Subscription
from datetime import datetime
from src import db
from src.middlewares import authentication_required
from src.services.stripe_service import create_session, get_session, get_subscription
import os

# essay controller blueprint to be registered with api blueprint
subscriptions = Blueprint("subscriptions", __name__)

# Generate Eassy api/v1/subscriptions/create-checkout-session
@subscriptions.route('/create-checkout-session', methods = ["POST"])
@authentication_required
def create_checkout_session():
    """
    Params
    - priceType (String)
    """
    try:
        data = request.json
        user_id = request.user_id
        if data["priceType"] == "monthly":
            price_id = os.environ.get("STRIPE_MONTHLY_PRICE_ID")
        else:
            price_id = os.environ.get("STRIPE_YEARLY_PRICE_ID")
            
        session = create_session(user_id, price_id)
        
        return Response(
            response=json.dumps({
                "status": True,
                "data": {
                    "sessionId": session["id"],
                }
            }),
            status=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        return Response(
                response=json.dumps({
                    "status": False,
                    "message": "Error Occured",
                    "error": str(e)
                }),
                status=500,
                mimetype="application/json"
            )
        
@subscriptions.route('/success', methods = ["GET"])
def subscription_success():
    try:
        user_id = request.args.get('user_id')
        session_id = request.args.get('session_id')
        session = get_session(session_id)
        
        subscription_id = session["subscription"]
        subscription = get_subscription(subscription_id)
        
        renewal_type = subscription["items"]["data"][0]["plan"]["interval"]
        next_payment_timestamp = subscription["current_period_end"]
        next_payment_date = datetime.utcfromtimestamp(next_payment_timestamp)
        
        subscription = Subscription.query.filter_by(user_id=user_id).first()
        if subscription:
            subscription.type = "UNLIMITED"
            subscription.next_payment_date = next_payment_date
            subscription.renewal_type = renewal_type
            subscription.subscription_id = subscription_id
            db.session.commit()
            
        redirect_url = os.environ.get("CLIENT_URL") + "/generate";
        return redirect(redirect_url, code=302)
    
    except Exception as e:
        return Response(
                response=json.dumps({
                    "status": False,
                    "message": "Error Occured",
                    "error": str(e)
                }),
                status=500,
                mimetype="application/json"
            )
        