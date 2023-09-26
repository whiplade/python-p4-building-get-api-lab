from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, MetaData, Integer
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Integer

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Bakery(db.Model, SerializerMixin):
    __tablename__ = "bakeries"

    serialize_rules = "+baked_goods,"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # the relationship to BakedGood
    baked_goods = db.relationship("BakedGood", back_populates="bakery")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "baked_goods": [good.to_dict() for good in self.baked_goods],
        }


class BakedGood(db.Model, SerializerMixin):
    __tablename__ = "baked_goods"

    serialize_rules = "-bakery,"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    bakery_id = db.Column(Integer(), ForeignKey("bakeries.id"))

    # the relationship to Bakery
    bakery = db.relationship("Bakery", back_populates="baked_goods")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "bakery_id": self.bakery_id,
        }