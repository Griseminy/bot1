from data import db_session
from data.brends import Brends
from data.delivery_goods import Delivery_goods
from data.deliverymen import Deliverymen
from data.goods import Goods
from data.purchase import Purchase
from data.sales import Sales
import operator

db_session.global_init(f"db/goods.db")
db_sess = db_session.create_session()

sales = db_sess.query(Sales).filter(Sales.id > 450).all()
tovary = {}
for elem in sales:
    for el in elem.deliverygood_ids.split('&'):
        tovar_id = db_sess.query(Delivery_goods).filter(Delivery_goods.id == el[:-2]).first().good_id
        if tovar_id not in tovary.keys():
            tovary[tovar_id] = 1
        else:
            tovary[tovar_id] += 1
brendsspis = db_sess.query(Brends).all()
brend_data_goods = {}
for elem in brendsspis:
    brend_data_goods[elem.brend] = {}
    goods_spis = db_sess.query(Goods).filter(Goods.brend == elem).all()
    for el in goods_spis:
        brend_data_goods[elem.brend][el.title] = 0
for elem in tovary.keys():
    tovarcall = db_sess.query(Goods).get(elem)
    brendcall = db_sess.query(Brends).get(tovarcall.brend_id)
    brend_data_goods[brendcall.brend][tovarcall.title] = tovary[elem]
new_dict = {}
for elem in brend_data_goods.keys():
    kolvo = 0
    for el in brend_data_goods[elem].keys():
        kolvo += brend_data_goods[elem][el]
    # brend_data_goods[elem]['кол-во'] = kolvo
    new_dict[elem] = kolvo
    # print(f"{elem} {kolvo}")
    # for el in brend_data_goods[elem].keys():
    #     print(f"\t\t{el}   {brend_data_goods[elem][el]}")

sorted_tuples = sorted(new_dict.items(), key=operator.itemgetter(1))
sorted_dict = {k: v for k, v in sorted_tuples}
for elem in sorted_dict:
    print(f"{elem} {sorted_dict[elem]}")
    for el in brend_data_goods[elem].keys():
        print(f"\t\t{el}   {brend_data_goods[elem][el]}")