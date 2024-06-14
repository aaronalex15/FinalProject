from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import flask_bcrypt, db
from sqlalchemy import event

class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    brands = db.relationship('Merchandise', back_populates='category')

    serialize_rules = ("-brands.category",)

    @classmethod
    def create_category(cls, name, parent_id=None):
        category = cls(name=name, parent_id=parent_id)
        db.session.add(category)
        db.session.commit()
        return category
    
    @validates("name")
    def validate_type(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Name must be of type string.")
        elif name not in ["Shirts", "Hoodies", "Letterman Jackets", "Shoes", "Sweats", "Hats", "Helmets"]:
            raise ValueError("Category name must be any of: Shirts, Hoodies, Letterman Jackets, Shoes, Sweats, Hats, or Helmets.")
        else:
            return name

