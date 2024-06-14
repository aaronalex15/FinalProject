#!/usr/bin/env python3

from flask import request, g, session, send_file, abort, jsonify, redirect, render_template
from flask_restful import Resource
from functools import wraps
from werkzeug.security import generate_password_hash
from config import app, db, api
import os
import stripe
from datetime import datetime
# Models
from models.user import User
from models.merchandise import Merchandise
from models.purchase import Purchase
from models.category import Category
from models.favorites import Favorite
# Schemas
from schemas.user_schema import user_schema, users_schema
from schemas.merchandise_schema import merchandise_schema, merchandises_schema
from schemas.purchase_schema import purchase_schema, purchases_schema
from schemas.category_schema import category_schema, categories_schema

# Views go here!

# @app.route('/')
# def index(id=0):
#     return render_template('index.html')

@app.before_request
def before_request():
    path_dict = {"userbyid": User, "merchandisebyid": Merchandise, "purchasebyid": Purchase}
    if request.endpoint in path_dict:
        id = request.view_args.get("id")
        record = db.session.get(path_dict.get(request.endpoint), id)
        key_name = "user" if request.endpoint == "userbyid" else "merchandise"
        if request.endpoint == 'purchasebyid':
            key_name = "purchase"
        setattr(g, key_name, record)

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return {"message": "You must be logged in!"}, 422
        return func(*args, **kwargs)
    return decorated_function

# ALL REGISTRATION RELATED ROUTES
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        user = user_schema.load(data, partial=True)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return user_schema.dump(user), 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422
    
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        user = User.query.filter_by(username=data["username"]).first()
        if user and user.authenticate(data.get("password_hash")):
            session["user_id"] = user.id
            return user_schema.dump(user), 200
        else:
            return {"message": "Invalid credentials"}, 422
    except Exception as e:
        return {"error": str(e)}, 422
    
@app.route("/logout", methods=["DELETE"])
def logout():
    try:
        if "user_id" in session:
            del session["user_id"]
        return {}, 204
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422
    
@app.route("/current_user", methods=["GET"])
def current_user():
    try:
        if "user_id" in session:
            user = db.session.get(User, session.get("user_id"))
            return user_schema.dump(user), 200
        else:
            return {"message": "Please log in"}, 400
    except Exception as e:
        return {"error": str(e)}

# ALL MERCHANDISE RELATED ROUTES
class Merchandises(Resource):
    # @login_required
    def get(self):
        try:
            serialized_merchandise = merchandises_schema.dump(Merchandise.query)
            return serialized_merchandise, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    def post(self):
        try:
            data = request.json
            category_id = data.get('category_id') 
            category = Category.query.filter_by(id=category_id).first()
            if not category:
                return {'error': 'Category not found'}, 404
            
            price = data.get('price')
            if not price or price <= 0:
                return {'error': 'Price must be greater than 0 for priced merchandise'}, 422
            
            merchandise = Merchandise(
                title=data['title'],
                description=data['description'],
                price=float(price),
                brands=data['brands'],
                type=data['type'],
                category=category,
                image=data['image']
            )
            db.session.add(merchandise)
            db.session.commit()
            return merchandise_schema.dump(merchandise), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 422
        
class MerchandiseById(Resource):
    # @login_required
    def get(self, id):
        try:
            merchandise = Merchandise.query.get(id)
            if not merchandise:
                abort(404, message="Merchandise not found")
            return merchandise_schema.dump(merchandise), 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    def post(self, id):
        user_id = request.json.get('user_id')
        merchandise = Merchandise.query.get(id)
        if not merchandise:
            abort(404, message="Merchandise not found")
        
        purchase = Purchase.query.filter_by(user_id=user_id, merchandise_id=id).first()
        if purchase:
            return jsonify({"message": "Merchandise downloaded successfully", "merchandise": merchandise_schema.dump(merchandise)}), 200
        else:
            return jsonify({"message": "Purchase required to download the merchandise"}), 402
        
    def patch(self, id):
        if g.merchandise:
            try:
                data = request.json
                updated_merchandise = merchandise_schema.load(data, instance=g.merchandise, partial=True)
                db.session.commit()
                return merchandise_schema.dump(updated_merchandise), 200
            except Exception as e:
                return {"error": str(e)}, 400
        else:
            return {"error": f"Merchandise {id} not found"}, 404
    
@app.route('/images/<path:image_path>')
def get_image(image_path):
    image_folder = 'merchandise_pictures'
    full_path = os.path.join(image_folder, image_path)
    print(full_path)
    return send_file(full_path, mimetype='image/jpeg') 
            
# ALL USER RELATED ROUTES
class Users(Resource):
    @login_required
    def get(self):
        try:
            serialized_user = users_schema.dump(User.query)
            return serialized_user, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    def post(self):
        try:
            data = (request.json)
            user = user_schema.load(data)
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 422

class UserById(Resource):
    @login_required
    # def get(self, id):
    #     try:
    #         if g.user:
    #             return user_schema.dump(g.user), 200
    #     except Exception as e:
    #         return {"error": str(e)}, 400
    
    @login_required
    def patch(self, id):
        try:
            user = db.session.get(User, session["user_id"])
            if user:
                data = request.json
                updated_user = user_schema.load(data, instance=user, partial=True)
                db.session.commit()
                return user_schema.dump(updated_user), 200
            else:
                return {"error": "User not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400
    
    @login_required        
    def delete(self, id):
        try:
            user = db.session.get(User, session["user_id"])
            if user:
                db.session.delete(user)
                db.session.commit()
                return {}, 204
        except Exception as e:
            return {"error": str(e)}, 400
        
# FAVORITES
class Favorites(Resource):
    def get(self, user_id):
        try:
            favorited_merchandises = Favorite.query.filter_by(user_id=user_id).all()
            serialized_merchandises = [merchandise.to_dict() for merchandise in favorited_merchandises]
            return jsonify({"favoritedMerchandises": serialized_merchandises}), 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    def post(self, merchandise_id):
        try:
            user_id = session["user_id"]
            favorite = Favorite(user_id=user_id, merchandise_id=merchandise_id)
            db.session.add(favorite)
            db.session.commit()
            return {"message": "Merchandise added to favorite successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 422
    
    def delete(self, merchandise_id):
        try:
            user_id = session["user_id"]
            favorite = Favorite.query.filter_by(user_id=user_id, merchandise_id=merchandise_id).first()
            if favorite:
                db.session.delete(favorite)
                db.session.commit()
                return {"message": "Merchandise removed from favorites successfully"}, 204
            else:
                return {"message": "Merchandise is not in favorites"}, 404
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 422
        
@app.route("/favorites/<int:user_id>", methods=["GET"])
def get_favorited_merchandises(user_id):
    try:
        favorited_merchandises = Favorite.query.filter_by(user_id=user_id).all()
        serialized_merchandises = [merchandise.to_dict() for merchandise in favorited_merchandises]
        return jsonify({"favoritedMerchandises": serialized_merchandises}), 200
    except Exception as e:
        return {"error": str(e)}, 500
        
# ALL PURCHASE RELATED ROUTES
class Purchases(Resource):
    @login_required
    def get(self):
        try:
            if "user_id" not in session:
                return {"error": "User not logged in"}, 401
            user_id = session["user_id"]
            purchases = Purchase.query.filter_by(user_id=user_id).all()
            serialized_purchases = purchases_schema.dump(purchases)
            return serialized_purchases, 200
        except Exception as e:
            return {"error": str(e)}, 400
    
    def post():
        try:
            data = request.json
            user_id = data.get("user_id")
            merchandise_id = data.get("merchandise_id")
            price = data.get("price")
            status = data.get("status", "pending")  # Default status to "pending" if not provided

            # Create a new Purchase record
            purchase = Purchase(user_id=user_id, merchandise_id=merchandise_id, price=price, status=status)
            db.session.add(purchase)
            db.session.commit()

            return {"message": "Purchase successfully created"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 422

class PurchaseById(Resource):
    def get(self, id):
        try:
            # import ipdb; ipdb.set_trace()
            user = User.query.get(session["user_id"])
            purchase = Purchase.query.filter_by(id=id).first()
            if purchase:
                purchase.status = "Completed"
                purchase.purchase_date = datetime.now()
                # return redirect("http://localhost:3000/success"), 200
                return purchases_schema.dump(user.purchases), 200
            else:
                return {"error": f"Purchase {id} not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400
        
class Categories(Resource):
    def get(self):
        try:
            serialized_category = categories_schema.dump(Category.query)
            return serialized_category, 200
        except Exception as e:
            return {"error": str(e)}, 400

YOUR_DOMAIN = "http://localhost:3000"
stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")
if not stripe_secret_key:
    raise ValueError("STRIPE_SECRET_KEY is not set in the environment variables.")
stripe.api_key = stripe_secret_key

@app.route('/create-checkout-session/<int:id>', methods=['POST'])
def create_checkout_session(id):
    try:
        merchandise_to_purchase = db.session.get(Merchandise, id)
        if merchandise_to_purchase:
            new_purchase_data = {
                "user_id": session.get("user_id"),
                "merchandise_id": merchandise_to_purchase.id,
                "price": merchandise_to_purchase.price,
                "status": "Pending",
            }
            new_purchase = Purchase(**new_purchase_data)

            db.session.add(new_purchase)
            db.session.commit()
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': merchandise_to_purchase.stripe_price_id,
                        'quantity': 1
                    }
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + f"/success/{new_purchase.id}",
                cancel_url=YOUR_DOMAIN + "/cancelled"
            )
            return redirect(checkout_session.url, code=303)
        else:
            return {"message": "Merchandise not found"}, 404
        import ipdb; ipdb.set_trace()
    except Exception as e:
        return {"message": str(e)}

# ROUTES
api.add_resource(Categories, "/categories")
api.add_resource(Merchandises, "/merchandises")
api.add_resource(MerchandiseById, "/merchandises/<int:id>")
api.add_resource(Users, "/users")
api.add_resource(UserById, "/users/<int:id>")
api.add_resource(Purchases, "/purchases")
api.add_resource(PurchaseById, "/success/<int:id>")
api.add_resource(Favorites, "/favorites/<int:merchandise_id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5555)))
# FRONTEND Routes
@app.route("/registration")
@app.route("/user/:<int:id>")
@app.route("/")
@app.route("/cart")
@app.route("/success/:<int:id>")

def index(id=0):
    return render_template("index.html")
