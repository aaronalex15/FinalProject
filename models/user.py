from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import flask_bcrypt, db
from werkzeug.security import check_password_hash
import re

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50))
    avatar = db.Column(db.String)
    bio = db.Column(db.String(250))
    _password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f"<User {self.id}: {self.name} | {self.username} | {self.email} />"

    # Relationships
    purchases = db.relationship("Purchase", back_populates="user")
    favorites = db.relationship('Favorite', back_populates='user')

    # Association Proxy
    merchandise = association_proxy("purchases", "merchandise")

    # Serializer Rules
    serialize_rules = ("-_password_hash", "-purchases.user",)

    # Validations, Password Hashing & Authenticating
    @validates("username")
    def validate_username(self, _, username):
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")
        elif 1 > len(username) > 20:
            raise ValueError("Username must be at least one character and less than 20 characters.")
        else:
            return username

    @validates("email")
    def validate_email(self, _, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address.")
        return email

    @hybrid_property
    def password_hash(self):
        raise AttributeError("You cannot view password!")

    @password_hash.setter
    def password_hash(self, new_password):
        if len(new_password) < 8:
            raise ValueError("Password length does not meet requirements.")
        hashed_password = flask_bcrypt.generate_password_hash(new_password).decode('utf-8')
        self._password_hash = hashed_password

    def authenticate(self, password):
        return flask_bcrypt.check_password_hash(self._password_hash, password)
