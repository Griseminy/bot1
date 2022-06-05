import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


# users_to_jobs = sqlalchemy.Table(
#     'users_to_jobs',
#     SqlAlchemyBase.metadata,
#     sqlalchemy.Column('users', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('users.id')),
#     sqlalchemy.Column('jobs', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('jobs.id'))
# )

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