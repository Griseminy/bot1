from data import db_session
from data.deliverymen import Deliverymen

deliverymen = {'Антон': 640287782, 'Aртём': 636503360}
admin = 1904018585
admin_2 = 754288169
delyverymen_id = {'Антон': '@slutmee', 'Aртём': '@soberaf'}
text_chat = '''Наш канал t.me/GhostVapeKgn
Переходите в закреп, там удобное меню

Доставка осуществляется в нижеперечисленные районы города:

Рынок-Звёздный-Стадион-Ксм-Швейная фирма-Каравай:
@soberaf

Рынок-Звёздный-Стадион-Ксм-Каравай: 
@slutmee

Оплата производится только при получении товара!

Возможна доставка и дальше по предварительному уведомлению об этом нашим курьерам.

Наш чат t.me/+8Hm_C9FN7IljOGYy
Отзывы: t.me/GhostVapeOtz
Тех. поддержка @q738383838'''
text_start = 'Привет! Этот бот предназначен для того, чтобы вы всегда могли узнать наличие товара у доставщика.\n' \
             'Нажмите на кнопку наличия, дальше выберите доставщика, а затем линейку.\n' \
             'Наш канал t.me/GhostVapeKgn \n' \
             'Прошу, если есть вопросы, то переходите в закреп канала'
sberbank = 5469320011598922
alfabank = 4584432922570461


def add_deliverymen(deliverymen):
    db_sess = db_session.create_session()
    spis = db_sess.query(Deliverymen.user_id).all()
    for name, user_id in deliverymen.items():
        if (user_id,) not in spis:
            deliveryman = Deliverymen(name=name, user_id=user_id, tg_id=delyverymen_id[name])
            db_sess.add(deliveryman)
            db_sess.commit()