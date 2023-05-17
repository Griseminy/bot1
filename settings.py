from data import db_session
from data.deliverymen import Deliverymen

deliverymen = {"Антон_Жижа_Центр": 640287782, 'Жижкин_Жижа_Снюс_Заозерный': 2071177185, 'Склад': 1}
admin = 1904018585
admin_2 = 754288169
admin_3 = 5929705793
delyverymen_id = {"Антон_Жижа_Центр": '@slutmee', 'Жижкин_Жижа_Снюс_Заозерный': '@stariy_xer_2009', 'Склад': '@sklad'}
text_chat = '''Доставка осуществляется в нижеперечисленные районы города:

Антон @slutmee: Звёздный-Стадион-Каравай-Ксм

Жижкин @Stariy_xer_2009: Заозёрный

Оплата производится только при получении товара!

Возможна доставка и дальше по предварительному уведомлению об этом нашим курьерам.
Тех. поддержка @q738383838'''
text_start = 'Привет! Этот бот предназначен для того, чтобы вы всегда могли узнать наличие товара у доставщика.' \
             'Нажмите на кнопку наличия, дальше выберите доставщика, а затем линейку.\n' \
             'Наш канал t.me/MoonVapeKgn \n' \
             'Купить жидкость t.me/MoonVapeKgn/34\n' \
             'Прошу, если есть вопросы, то переходите в закреп канала'
sberbank = 5469320011598922
alfabank = 4584432922570461

cities = {'Курган': -100000000000000}
groups = {-1000000000000000: '@fgsdfgsfd'}
chat_ids = {-1000000000000000}# [-1001605650569]
text_start_2 = ""
text_success = ""

def add_deliverymen(deliverymen):
    db_sess = db_session.create_session()
    spis = db_sess.query(Deliverymen.user_id).all()
    for name, user_id in deliverymen.items():
        if (user_id,) not in spis:
            deliveryman = Deliverymen(name=name, user_id=user_id, tg_id=delyverymen_id[name])
            db_sess.add(deliveryman)
            db_sess.commit()