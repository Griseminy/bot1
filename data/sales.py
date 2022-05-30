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

class Sales(SqlAlchemyBase):
    __tablename__ = 'sales'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.String)
    deliveryman_id = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey("deliveryman.id"))
    deliveryman = orm.relation('Deliverymen')
    deliverygood_ids = title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_send = orm.relation(sqlalchemy.Boolean, default=False)