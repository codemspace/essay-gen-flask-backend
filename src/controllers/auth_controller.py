from flask import request, Response, json, Blueprint
from src.models.user_model import User
from src.models.subscription_model import Subscription
from src.models.social_account_model import Social_account
from src import bcrypt, db
from datetime import datetime, timedelta
from src.middlewares import authentication_required
import jwt
import os
import requests

# user controller blueprint to be registered with api blueprint
auth = Blueprint("auth", __name__)

# login api/v1//auth/signin
@auth.route('/signin', methods = ["POST"])
def handle_login():
    try: 
        # first check user parameters
        data = request.json
        if "email" and "password" in data:
            # check db for user records
            user = User.query.filter_by(email = data["email"]).first()

            # if user records exists we will check user password
            if user:
                # check user password
                if bcrypt.check_password_hash(user.password, data["password"]):
                    # user password matched, we will generate token
                    payload = {
                        'iat': datetime.utcnow(),
                        'exp': datetime.utcnow() + timedelta(days=1),
                        'user_id': user.id
                    }
                    token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
                    return Response(
                            response=json.dumps({"status": True,
                                                "message": "User Sign In Successful",
                                                "token": token}),
                            status=200,
                            mimetype='application/json'
                        )
                
                else:
                    return Response(
                        response=json.dumps({"status": False, "message": "User Password Mistmatched"}),
                        status=401,
                        mimetype='application/json'
                    ) 
            # if there is no user record
            else:
                return Response(
                    response=json.dumps({"status": False, "message": "No user record found. Please register."}),
                    status=404,
                    mimetype='application/json'
                ) 
        else:
            # if request parameters are not correct 
            return Response(
                response=json.dumps({"status": False, "message": "User Parameters Email and Password are required"}),
                status=400,
                mimetype='application/json'
            )
        
    except Exception as e:
        return Response(
                response=json.dumps({"status": False, 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )

# Register api/v1/auth/signup
@auth.route('/signup', methods = ["POST"])
def handle_signup():
    try: 
        # first validate required use parameters
        data = request.json
        if "firstname" in data and "lastname" and data and "email" and "password" in data:
            # validate if the user exist 
            user = User.query.filter_by(email = data["email"]).first()
            # usecase if the user doesn't exists
            if not user:
                # creating the user instance of User Model to be stored in DB
                user_obj = User(
                    firstname = data["firstname"],
                    lastname = data["lastname"],
                    email = data["email"],
                    # hashing the password
                    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                )
                db.session.add(user_obj)
                db.session.commit()
                
                subscription_obj = Subscription(
                    type = "FREE",
                    user = user_obj
                )
                db.session.add(subscription_obj)
                db.session.commit()

                # lets generate jwt token
                payload = {
                    'iat': datetime.utcnow(),
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'user_id': user_obj.id
                }
                token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
                return Response(
                response=json.dumps({"status": True,
                                    "message": "User Sign up Successful",
                                    "token": token}),
                status=200,
                mimetype='application/json'
            )
            else:
                # if user already exists
                return Response(
                response=json.dumps({"status": False, "message": "User already exists kindly use sign in"}),
                status=409,
                mimetype='application/json'
            )
        else:
            # if request parameters are not correct 
            return Response(
                response=json.dumps({"status": False, "message": "User Parameters Firstname, Lastname, Email and Password are required"}),
                status=400,
                mimetype='application/json'
            )
        
    except Exception as e:
        return Response(
                response=json.dumps({"status": False, 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )
        
@auth.route('/current-user', methods = ['GET'])
@authentication_required
def get_authenticated_user():
    try:
        user_id = request.user_id
        user = User.query.get(user_id)
        if user:
            subscription = Subscription.query.filter_by(user_id = user_id).first()
            if subscription:
                payload = {
                    "id": user.id,
                    "email": user.email,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "avatar": user.avatar,
                    "plan": {
                        "type": subscription.type,
                        "renewalType": subscription.renewal_type,
                        "nextPaymentDate": subscription.next_payment_date,
                        "quotaUsage": subscription.quota_usage
                    }
                }
            
                return Response(
                        response=json.dumps({
                            "status": True, 
                            "data": {
                                "user": payload
                            }
                        }),
                        status=200,
                        mimetype='application/json'
                    ) 
            else:
                return Response(
                    response=json.dumps({"status": False, "message": "Plan doesn't exist"}),
                    status=404,
                    mimetype="application/json"
                )
        else:
            return Response(
                    response=json.dumps({"status": False, "message": "User Record doesn't exist"}),
                    status=404,
                    mimetype='application/json'
                ) 
    except Exception as e:
        return Response(
                response=json.dumps({"status": False, 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )
    
@auth.route('/google', methods = ["POST"])
def google_auth():
    try:
        data = request.json
        access_token = data["access_token"]
        headers = { "Authorization": f"Bearer {access_token}" }
        response = requests.get(os.environ.get("GOOGLE_USERINFO_URL"), headers=headers)
        result = response.json()
        
        user = User.query.filter_by(email = result["email"]).first()
        if user:
            social_account = Social_account.query.filter_by(user_id = user.id).first()
            if social_account:
                if social_account.uid == result["sub"]:
                    payload = {
                        'iat': datetime.utcnow(),
                        'exp': datetime.utcnow() + timedelta(days=1),
                        'user_id': user.id
                    }
            
                    token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
                    return Response(
                        response=json.dumps({"status": True,
                                            "message": "User Sign In Successful",
                                            "token": token}),
                        status=200,
                        mimetype='application/json')
                else:
                    return Response(
                        response=json.dumps({"status": False, "message": "User Record doesn't exist, kindly register"}),
                        status=404,
                        mimetype='application/json'
                    )
            else:
                social_account_obj = Social_account(
                    uid = result["sub"],
                    provider = "Google",
                    user = user
                )
                
                db.session.add(social_account_obj)
                db.session.commit()
                
                payload = {
                    'iat': datetime.utcnow(),
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'user_id': user.id
                }
            
                token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
                return Response(
                    response=json.dumps({"status": True,
                                        "message": "User Sign In Successful",
                                        "token": token}),
                    status=200,
                    mimetype='application/json')
        else:
            user_obj = User(
                    firstname = result.get("given_name", ""),
                    lastname = result.get("family_name", ""),
                    email = result["email"],
                    avatar = result.get("picture", "")
                )
            db.session.add(user_obj)
            
            social_account_obj = Social_account(
                uid = result["sub"],
                provider = "Google",
                user = user_obj
            )
            db.session.add(social_account_obj)
            
            subscription_obj = Subscription(
                    type = "FREE",
                    user = user_obj
                )
            db.session.add(subscription_obj)
            db.session.commit()
            
            payload = {
                    'iat': datetime.utcnow(),
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'user_id': user_obj.id
                }
            
            token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
            return Response(
                response=json.dumps({"status": True,
                                    "message": "User Sign Up Successful",
                                    "token": token}),
                status=200,
                mimetype='application/json')
            
    except Exception as e:
        return Response(
                response=json.dumps({"status": False, 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )