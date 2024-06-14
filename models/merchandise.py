from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import flask_bcrypt, db
from sqlalchemy import event, LargeBinary
import stripe
import os

class Merchandise(db.Model, SerializerMixin):
    __tablename__ = "merchandise"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    merchandise_file = db.Column(db.String(255))
    price = db.Column(db.Float)
    brand = db.Column(db.String)
    type = db.Column(db.String)
    image = db.Column(db.String)
    stripe_product_id = db.Column(db.String)
    stripe_price_id = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return f"""<Merchandise {self.id}: 
                        Title: {self.title}, 
                        Type: {self.type},
                        Description: {self.description}, 
                        Brand: {self.brand}, 
                        Price: {self.price} 
                        />
                        """

    # Relationships
    purchases = db.relationship('Purchase', back_populates='merchandise')
    category = db.relationship('Category', back_populates='merchandise')
    favorites = db.relationship('Favorite', back_populates='merchandise')

    # Association Proxy
    users = association_proxy("purchases", "user")

    # Validations
    @validates("title")
    def validate_title(self, _, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        elif len(title) < 2 or len(title) > 50:
            raise ValueError("Title must be between 2 and 50 characters long.")
        else:
            return title

    @validates("price")
    def validate_price(self, key, price):
        if price is None or not isinstance(price, float):
            raise ValueError("Price must be provided and must be a float.")
        elif price > 5000:
            raise ValueError("Price cannot be more than 5000 dollars.")
        else:
            return price

    @validates("brand")
    def validate_brand(self, _, brand):
        if not isinstance(brand, str):
            raise TypeError("Brand must be of type string.")
        elif brand not in ["New Era", "Live Mechanics", "Puma", "Nike", "NFL", "G-West"]:
            raise ValueError("Brand must be either New Era, Live Mechanics, Puma, Nike, NFL, or G-West.")
        else:
            return brand

    @validates("type")
    def validate_type(self, _, type):
        if not isinstance(type, str):
            raise TypeError("Type must be of type string.")
        elif type not in ["Shoes", "Clothing"]:
            raise ValueError("Type must be either Shoes or Clothing.")
        else:
            return type

    def __init__(self, *args, **kwargs):
        super(Merchandise, self).__init__(*args, **kwargs)
        self.create_stripe_product_and_price()

    def create_stripe_product_and_price(self):
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

        if not self.stripe_product_id or not self.stripe_price_id:
            stripe_product = stripe.Product.create(
                name=self.title,
                description=self.description,
                type="good",
            )

            stripe_price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=int(self.price * 100),
                currency="usd",
            )

            self.stripe_product_id = stripe_product.id
            self.stripe_price_id = stripe_price.id

            db.session.commit()

@event.listens_for(Merchandise.__table__, 'after_create')
def create_initial_categories(*args, **kwargs):
    shoes = Merchandise(type='Shoes', description='Shoes related merchandise', brand='Nike')
    clothing = Merchandise(type='Clothing', description='Clothing related merchandise', brand='Puma')
    db.session.add_all([shoes, clothing])
    db.session.commit()
