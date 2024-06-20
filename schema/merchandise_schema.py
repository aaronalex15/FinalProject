from config import ma
from marshmallow import validate, fields
from models.merchandise import Merchandise  # Assuming Merchandise model is used
from models.category import Category  # Assuming CategorySchema is used

class MerchandiseSchema(ma.SQLAlchemyAutoSchema):
    category = fields.Nested('CategorySchema', exclude=('merchandise',))
    merchandise_file = fields.String()
    
    class Meta:
        model = Merchandise
        load_instance = True
    
    is_free = fields.Boolean(required=True)
    download_link = fields.String()
    
    title = fields.String(required=True, validate=validate.Length(min=2, max=50, error="Title must be between 2 and 50 characters."))
    description = fields.String(required=True, validate=validate.Length(min=2, max=250, error="Description must be between 2 and 250 characters."))
    price = fields.Float(required=True, validate=validate.Range(min=1, max=5000, error="Price must be between 1 and 5000."))
    
    brands = fields.String(required=True, validate=validate.OneOf(["New Era", "Live Mechanics", "Puma", "Nike", "NFL", "G-West"], error="Brand must be one of: New Era, Live Mechanics, Puma, Nike, NFL, G-West."))
    
    category_id = fields.Integer(required=True)
    image = fields.String()

merchandise_schema = MerchandiseSchema()
merchandises_schema = MerchandiseSchema(many=True)
