from data import db_session
from data.deliverymen import Deliverymen

deliverymen = {'Антон': 123, 'Aртём': 456, 'Глеб': 789}

def add_deliverymen(deliverymen):
    db_sess = db_session.create_session()
    for name, user_id in deliverymen.items():
        deliveryman = Deliverymen(name=name, user_id=user_id)
        db_sess.add(deliveryman)
        db_sess.commit()
