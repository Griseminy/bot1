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
    date = sqlalchemy.Column(sqlalchemy.Date)
    deliveryman_id = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey("deliverymen.id"))
    deliveryman = orm.relation('Deliverymen')
    deliverygood_ids = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    on_check = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_send = sqlalchemy.Column(sqlalchemy.Boolean, default=False)