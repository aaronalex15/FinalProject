#!/usr/bin/env python3

# Standard library imports
import random
from random import randint

# Remote library imports
from faker import Faker
from werkzeug.security import generate_password_hash

# Local imports
from app import app
from models.user import User
from models.merchandise import Merchandise
from models.purchase import Purchase
from models.category import Category
from config import app, db
from schema.category_schema import CategorySchema


def seed_cat():

    categories = [
        {"name": "Hoodies", "description": "Hoodie merchandise"},
        {"name": "Sweats", "description": "Sweat merchandise"},
        {"name": "Jackets", "description": "Jacket merchandise"},
        {"name": "Shoes", "description": "Shoe merchandise"},
        {"name": "Hats", "description": "Hat merchandise"},
    ]

    category_schema = CategorySchema()
    for cat_data in categories:
        category = Category.query.filter_by(
            name=cat_data["name"], description=cat_data["description"]
        ).first()
        if not category:
            category = category_schema.load(cat_data)
            db.session.add(category)
    db.session.commit()


if __name__ == "__main__":
    fake = Faker()
    with app.app_context():
        Purchase.query.delete()
        User.query.delete()
        Category.query.delete()
        Merchandise.query.delete()

        seed_cat()
        categories = Category.query.all()

        category_hoodies = Category.query.filter_by(
            name="Hoodies", description="Hoodie merchandise"
        ).first()
        if not category_hoodies:
            category_hoodies = Category(
                name="Hoodies", description="Hoodie merchandise"
            )
            db.session.add(category_hoodies)
            db.session.commit()

        category_sweats = Category.query.filter_by(
            name="Sweats", description="Sweat merchandise"
        ).first()
        if not category_sweats:
            category_sweats = Category(name="Sweats", description="Sweat merchandise")
            db.session.add(category_sweats)
            db.session.commit()

        category_jackets = Category.query.filter_by(
            name="Jackets", description="Jacket merchandise"
        ).first()
        if not category_jackets:
            category_jackets = Category(
                name="Jackets", description="Jacket merchandise"
            )
            db.session.add(category_jackets)
            db.session.commit()

        category_shoes = Category.query.filter_by(
            name="Shoes", description="Shoe merchandise"
        ).first()
        if not category_shoes:
            category_shoes = Category(name="Shoes", description="Shoe merchandise")
            db.session.add(category_shoes)
            db.session.commit()

        category_hats = Category.query.filter_by(
            name="Hats", description="Hat merchandise"
        ).first()
        if not category_hats:
            category_hats = Category(name="Hats", description="Hat merchandise")
            db.session.add(category_hats)
            db.session.commit()

        for _ in range(10):
            username = fake.user_name()
            email = fake.email()
            user = User(
                username=username,
                email=email,
                name=fake.name(),
                avatar=fake.image_url(),
                bio=fake.text(max_nb_chars=250),
                _password_hash=generate_password_hash(
                    fake.password()
                ),  # Using generate_password_hash
            )
            print(f"Adding user: {username}, {email}")
            db.session.add(user)

        db.session.commit()

        m1 = Merchandise(
            title="Purple Mask Hoodie",
            description="Beige hoodie with a purple masked character.",
            price=100.00,
            image="/images/merch1.jpeg",
            brand="Live Mechanics",
            type="Clothing",
            category_id=Category.query.filter_by(name="Hoodies").first().id,
        )
        m2 = Merchandise(
            title="Stack Sweats",
            description="Fitted jeans with flared bottoms.",
            price=120.00,
            image="/images/merch2.jpeg",
            brand="Live Mechanics",
            type="Clothing",
            category_id=Category.query.filter_by(name="Sweats").first().id,
        )
        m3 = Merchandise(
            title="Heart Break Letterman",
            description="Letterman jacket with heart break symbols.",
            price=140.00,
            image="/images/merch3.jpeg",
            brand="Live Mechanics",
            type="Clothing",
            category_id=Category.query.filter_by(name="Jackets").first().id,
        )
        m4 = Merchandise(
            title="Gwest Smiley Face Hoodie",
            description="Black/white hoodie with a smiley face character.",
            price=120.00,
            image="/images/merch4.jpeg",
            brand="Live Mechanics",
            type="Clothing",
            category_id=Category.query.filter_by(name="Hoodies").first().id,
        )
        m5 = Merchandise(
            title="Nike Dunks",
            description="Original Nike Dunks.",
            price=150.00,
            image="/images/merch5.jpeg",
            brand="Nike",
            type="Shoes",
            category_id=Category.query.filter_by(name="Shoes").first().id,
        )
        m6 = Merchandise(
            title="Pumas",
            description="Original Pumas.",
            price=100.00,
            image="/images/merch6.jpeg",
            brand="Puma",
            type="Shoes",
            category_id=Category.query.filter_by(name="Shoes").first().id,
        )
        m7 = Merchandise(
            title="Dodger Fitted Cap",
            description="New Era Dodger fitted Cap.",
            price=40.00,
            image="/images/merch7.jpeg",
            brand="New Era",
            type="Clothing",
            category_id=Category.query.filter_by(name="Hats").first().id,
        )
        m8 = Merchandise(
            title="Yankee Fitted Cap",
            description="New Era Yankee fitted Cap.",
            price=40.00,
            image="/images/merch8.jpeg",
            brand="New Era",
            type="Clothing",
            category_id=Category.query.filter_by(name="Hats").first().id,
        )
        m9 = Merchandise(
            title="Raiders Helmet",
            description="Replica Raiders Helmet.",
            price=180.00,
            image="/images/merch9.jpeg",
            brand="New Era",
            type="Clothing",
            category_id=Category.query.filter_by(name="Hats").first().id,
        )
        m10 = Merchandise(
            title="Vikings Helmet",
            description="Replica Vikings Helmet.",
            price=180.00,
            image="/images/merch10.jpeg",
            brand="New Era",
            type="Clothing",
            category_id=Category.query.filter_by(name="Hats").first().id,
        )
        merchandise = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10]
        db.session.add_all(merchandise)
        db.session.commit()

    print("Finished seeding...")
