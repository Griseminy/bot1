from data import db_session
from data.deliverymen import Deliverymen

deliverymen = {'Антон': 123, 'Aртём': 456, 'Глеб': 789}
admin = 1904018585

def add_deliverymen(deliverymen):
    db_sess = db_session.create_session()
    spis = db_sess.query(Deliverymen.user_id).all()
    for name, user_id in deliverymen.items():
        if (user_id,) not in spis:
            deliveryman = Deliverymen(name=name, user_id=user_id)
            db_sess.add(deliveryman)
            db_sess.commit()

