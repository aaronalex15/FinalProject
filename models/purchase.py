from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import flask_bcrypt, db
from .user import User
from .merchandise import Merchandise  
import stripe
import os

class Purchase(db.Model, SerializerMixin):
    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    merchandise_id = db.Column(db.Integer, db.ForeignKey("merchandise.id"), nullable=False)  
    price = db.Column(db.Float)
    status = db.Column(db.String, nullable=False)
    purchase_date = db.Column(db.DateTime, default=db.func.now())

    # Relationships
    user = db.relationship("User", back_populates="purchases")
    merchandise = db.relationship("Merchandise", back_populates="purchases") 

    # Serializer Rules
    serialize_rules = ("-user.purchases", "-merchandise.purchases",)

    # Validations
    @validates("user_id")
    def validate_user_id(self, _, user_id):
        if not isinstance(user_id, int):
            raise TypeError("User id must be an integer")
        elif user_id < 1:
            raise ValueError(f"{user_id} has to be a positive integer")
        elif not db.session.get(User, user_id):
            raise ValueError(f"{user_id} has to correspond to an existing user")
        else:
            return user_id

    @validates("merchandise_id")
    def validate_merchandise_id(self, _, merchandise_id):
        if not isinstance(merchandise_id, int):
            raise TypeError("Merchandise id must be an integer")
        elif merchandise_id < 1:
            raise ValueError(f"{merchandise_id} must be a positive integer")
        elif not db.session.get(Merchandise, merchandise_id):
            raise ValueError(f"{merchandise_id} has to correspond to an existing merchandise")
        else:
            return merchandise_id
