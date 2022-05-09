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
    brend = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    goods = orm.relation("Goods", back_populates='brend')