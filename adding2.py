from data import db_session
from data.brends import Brends
from data.goods import Goods
from data.deliverymen import Deliverymen
from data.delivery_goods import Delivery_goods


db_session.global_init(f"db/goods.db")

with open('vkusy.txt', mode='r', encoding="utf8") as f:
    for elem in f.read().split('\n\n\n'):
        characteristics_1 = elem.split('\n\n')[0]
        characteristics_2 = elem.split('\n\n')[1]

        brend = characteristics_1.split('\n')[0]
        price = int(characteristics_1.split('\n')[1])
        salary = int(characteristics_1.split('\n')[2])
        discount_1, discount_2 = int(characteristics_1.split('\n')[3].split('/')[0]), int(characteristics_1.split('\n')[3].split('/')[1])

        flavors = characteristics_2.split('\n')
        print(brend, price, salary, discount_1, discount_2)
        print(flavors)
        db_sess = db_session.create_session()
        db_sess.add(Brends(brend=characteristics_1.split('\n')[0],
                            price=int(characteristics_1.split('\n')[1]),
                                       discount_1=int(characteristics_1.split('\n')[3].split('/')[0]),
                                       discount_2=int(characteristics_1.split('\n')[3].split('/')[1]),
                                       salary=int(characteristics_1.split('\n')[2])))
        db_sess.commit()
        db_sess = db_session.create_session()
        brend = db_sess.query(Brends).filter(Brends.brend == brend).first()
        for elem in flavors:
            db_sess.add(Goods(title=elem, brend=brend))
            db_sess.commit()
            good = db_sess.query(Goods).filter(Goods.brend == brend, Goods.title == elem).first()
            for el in db_sess.query(Deliverymen).all():
                delivery_good = Delivery_goods(amount=0, good=good, deliveryman=el)
                db_sess.add(delivery_good)
                db_sess.commit()