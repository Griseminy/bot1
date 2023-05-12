from data import db_session
from data.deliverymen import Deliverymen

deliverymen = {'Жижкин': 2071177185, 'Склад': 1}
admin = 1904018585
admin_2 = 754288169
admin_3 = 5929705793
delyverymen_id = {'Жижкин': '@stariy_xer_2009', 'Склад': '@sklad'}
text_chat = '''Доставка осуществляется в нижеперечисленные районы города:



Оплата производится только при получении товара!

Возможна доставка и дальше по предварительному уведомлению об этом нашим курьерам.
Тех. поддержка @q738383838'''
text_start = 'Привет! Этот бот предназначен для того, чтобы вы всегда могли узнать наличие товара у доставщика или предложить объявление.\n' \
             'Нажмите на кнопку наличия, дальше выберите доставщика, а затем линейку.\n' \
             'Наш канал t.me/GhostVapeKgn \n' \
             'Купить жидкость t.me/GhostVapeKgn/34\n' \
             'Барахолка t.me/GhostVapeAd\n' \
             'Прошу, если есть вопросы, то переходите в закреп канала'
sberbank = 5469320011598922
alfabank = 4584432922570461

cities = {'Курган': -1001605650569}
groups = {}#{-1001605650569: '@GhostVapeAd'}
chat_ids = {}# [-1001605650569]
text_start_2 = """В данном боте вы можете предложить своё объявление, но:
 Прикрепите только одно фото или не прикрепляйте
 Прикрепите текст к фотографии или просто пришлите текст
 Один пользователь может публиковать только 1 объявление в день
 Нельзя продавать устройства, которые продаются в @GhostVapeKgn
 Жидкости только в докид к девайсам
 Барахолка @GhostVapeAd"""
text_success = """Спасибо! Если вы корректно предложили объявление, то после модерации ваше объявление будет опубликовано.
 Модерация занимает до 12 часов.
 Список правил:
 Прикрепите только одно фото или не прикрепляйте вовсе
 Прикрепите текст к фотографии или просто пришлите текст
 Один пользователь может публиковать только 1 объявление в день
 Нельзя продавать устройства, которые продаются в @GhostVapeKgn
 Жидкости только в докид к девайсам"""


def add_deliverymen(deliverymen):
    db_sess = db_session.create_session()
    spis = db_sess.query(Deliverymen.user_id).all()
    for name, user_id in deliverymen.items():
        if (user_id,) not in spis:
            deliveryman = Deliverymen(name=name, user_id=user_id, tg_id=delyverymen_id[name])
            db_sess.add(deliveryman)
            db_sess.commit()