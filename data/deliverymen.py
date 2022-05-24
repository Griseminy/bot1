import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Deliverymen(SqlAlchemyBase):
    __tablename__ = 'deliverymen'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    delivery_good = orm.relation("Delivery_goods", back_populates='deliveryman')