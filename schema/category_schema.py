from config import ma
from marshmallow import fields, validate
from marshmallow_sqlalchemy import auto_field
from models.category import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    merchandise = fields.Nested("MerchandiseSchema", many=True, exclude=("category",))

    class Meta:
        model = Category
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field(
        required=True,
        validate=validate.OneOf(
            [
                "Shirts",
                "Hoodies",
                "Jackets",
                "Shoes",
                "Sweats",
                "Hats",
                "Helmets",
            ],
            error="Category name must be any of: Shirts, Hoodies, Letterman Jackets, Shoes, Sweats, Hats, Helmets.",
        ),
        description=auto_field(),
    )


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
