from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from os import environ
import os
import stripe
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate Flask app
app = Flask(
    __name__,
    static_url_path="",
    static_folder="./client/build",
    template_folder="./client/build",
)

# Configure SQLAlchemy database URI
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set secret key for sessions
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Configure Flask-Session to use SQLAlchemy for session management
db = SQLAlchemy(app)

# Bind SQLAlchemy session to Flask-Session
# Session(app)
# app.config["SESSION_SQLALCHEMY"] = db.session
# app.session_interface = SQLAlchemySessionInterface(db.session)

# Configure Stripe keys
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
}
stripe.api_key = stripe_keys["secret_key"]

# Initialize Flask extensions
migrate = Migrate(app, db)
api = Api(app)
ma = Marshmallow(app)
flask_bcrypt = Bcrypt(app)
