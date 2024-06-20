from config import ma
from marshmallow import fields, validate
from models.purchase import Purchase

class PurchaseSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Purchase
        load_instance = True
        exclude = ("user_id",)

    user = fields.Nested(
        "UserSchema",
        only=("id",),
    )

    user_id = fields.Integer(required=True, validate=validate.Range(min=1, error="Invalid user ID"))
    merchandise_id = fields.Integer(required=True, validate=validate.Range(min=1, error="Invalid merchandise ID"))
    price = fields.Float(required=True, validate=validate.Range(min=0, error="Price must be a positive number"))
    status = fields.String(required=True, validate=validate.OneOf(["Pending", "Completed", "Canceled"], error="Invalid status"))
    purchase_date = fields.DateTime(required=True)

purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)
