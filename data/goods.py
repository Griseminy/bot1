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

class Goods(SqlAlchemyBase):
    __tablename__ = 'goods'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    brend_id = sqlalchemy.Column(sqlalchemy.String,
                                sqlalchemy.ForeignKey("brends.id"))
    brend = orm.relation('Brends')