from flask import Flask, send_from_directory
from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__, static_folder="../dist", template_folder='templates')

# This will enable CORS for all routes
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory('../dist', 'index.html')

# calling the app configuration
if os.environ.get("APP_ENV") == "development":
    config =  Config().dev_config
else:
    config = Config().production_config

# load the secret key defined in the .env file
app.secret_key = os.environ.get("SECRET_KEY")
bcrypt = Bcrypt(app)

# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("MYSQL_DB_URL")

# To specify to track modifications of objects and emit signals
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
 
db = SQLAlchemy(app)

# import api blueprint to register it with app
from src.routes import api
app.register_blueprint(api, url_prefix="/api/v1")