from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    # Correct relationship name
    merchandise = db.relationship("Merchandise", back_populates="category")

    @classmethod
    def create_category(cls, name, description=None):
        category = cls(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        return category
