import json
from urllib import response
from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"


@app.route("/bakeries")
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in bakeries]

    return jsonify(bakery_list)


@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery_dict = bakery.to_dict()
        return jsonify(bakery_dict)

    else:
        return jsonify({"message": "Bakery not found"}), 404


@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [good.to_dict() for good in baked_goods]

    return jsonify(baked_goods_list)


@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    luxurious_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if luxurious_good:
        luxurious_good_dict = luxurious_good.to_dict()
        return jsonify(luxurious_good_dict)
    else:
        return jsonify({"message": "No baked goods found"}), 404


if __name__ == "__main__":
    app.run(port=5555, debug=True)