import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Purchase(SqlAlchemyBase):
    __tablename__ = 'purchase'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date)
    brend_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("brends.id"))
    brend = orm.relation('Brends')
    amount_purchase = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float)
