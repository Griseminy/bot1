import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Delivery_goods(SqlAlchemyBase):
    __tablename__ = 'delivery_goods'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    good_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("goods.id"))
    good = orm.relation('Goods')
    deliveryman_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("deliverymen.id"))
    deliveryman = orm.relation('Deliverymen')