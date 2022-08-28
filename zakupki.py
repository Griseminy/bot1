from data import db_session
from data.purchase import Purchase


db_session.global_init(f"db/goods.db")
db_sess = db_session.create_session()
zakupleno = db_session.create_session().query(
                    Purchase).filter(Purchase.amount > 0).all()
deneg = 0
for elem in zakupleno:
    deneg += elem.amount * elem.price
print(deneg)