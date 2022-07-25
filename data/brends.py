import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Brends(SqlAlchemyBase):
    __tablename__ = 'brends'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    brend = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    goods = orm.relation("Goods", back_populates='brend')
    discount_1 = sqlalchemy.Column(sqlalchemy.Integer)
    discount_2 = sqlalchemy.Column(sqlalchemy.Integer)
    salary = sqlalchemy.Column(sqlalchemy.Integer)
    purchase = orm.relation("Purchase", back_populates='brend')
    txt_file = sqlalchemy.Column(sqlalchemy.String)
    photo_link = sqlalchemy.Column(sqlalchemy.String)