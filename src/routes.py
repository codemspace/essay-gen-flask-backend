from flask import Blueprint
from src.controllers.auth_controller import auth
from src.controllers.essay_controller import essays
from src.controllers.subscription_controller import subscriptions
from src.controllers.document_controller import documents

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(essays, url_prefix="/essays")
api.register_blueprint(subscriptions, url_prefix="/subscriptions")
api.register_blueprint(documents, url_prefix="/documents")