import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Sales(SqlAlchemyBase):
    __tablename__ = 'sales'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date)
    deliveryman_id = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey("deliverymen.id"))
    deliveryman = orm.relation('Deliverymen')
    deliverygood_ids = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sales_salary = sqlalchemy.Column(sqlalchemy.Float)
    total = sqlalchemy.Column(sqlalchemy.Float)
    on_check = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_send = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    income = sqlalchemy.Column(sqlalchemy.Float)
