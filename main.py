import datetime
import itertools
#import logging
from data import db_session
from data.brends import Brends
from data.delivery_goods import Delivery_goods
from data.deliverymen import Deliverymen
from data.goods import Goods
from data.sales import Sales
from settings import add_deliverymen
from settings import admin
from settings import deliverymen
from settings import delyverymen_id
from settings import text_chat
from sqlalchemy.sql import extract
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

TOKEN = '5301614535:AAGAjCg3CopbFtvzUQVGLAkE9lOpNsbnX-Q'
#logging.basicConfig(
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
#)

#logger = logging.getLogger(__name__)


def start(update, context):
    context.user_data['locality'] = {}
    context.user_data['locality'][1] = 'Старт'
    if update.message.chat.id == admin:
        update.message.reply_text('Нажмите кнопки снизу',
                                  reply_markup=ReplyKeyboardMarkup([['Наличие', 'Изменить количество'],
                                                                    ['Добавить линейку', 'Изменить линейку'],
                                                                    ['Проверка', 'Статистика']], resize_keyboard=True,
                                                                   one_time_keyboard=True))
    elif update.message.chat.id in deliverymen.values():
        context.user_data['user_id_db'] = db_session.create_session().query(
            Deliverymen).filter(Deliverymen.user_id == update.message.chat.id).first().id
        update.message.reply_text('Нажмите кнопки снизу', reply_markup=ReplyKeyboardMarkup([['Продать', 'Наличие'],
                                                                                            ['Статистика за день',
                                                                                             'Статистика за месяц'],
                                                                                            ['Отправить на проверку',
                                                                                             'Нужно перевести']],
                                                                                           resize_keyboard=True,
                                                                                           one_time_keyboard=True))
    else:
        update.message.reply_text('Нажмите кнопки на клавиатуре',
                                  reply_markup=ReplyKeyboardMarkup([['Наличие'], ['Доставка']], resize_keyboard=True,
                                                                   one_time_keyboard=True))


def handler(update, context):
    try:
        if update.message.chat.id == admin:
            # Главное меню
            if context.user_data['locality'][len(context.user_data['locality'])] == 'Старт':
                if update.message.text == 'Добавить линейку':
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Добавить линейку'
                    update.message.reply_text(f'Введите название, цену, зарплату скидки '
                                              f'через слэш каждый с новой строки',
                                              reply_markup=ReplyKeyboardMarkup([['Назад']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Изменить линейку':
                    reply_keyboard = [[elem.brend] for elem in db_session.create_session().query(
                        Brends).all()]
                    reply_keyboard.append(['Назад'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = \
                        'Изменить линейку'
                    update.message.reply_text('Выберите линейку для изменения',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Изменить количество':
                    reply_keyboard = [[elem] for elem in deliverymen]
                    reply_keyboard.append(['Назад'])
                    context.user_data['locality'][
                        len(context.user_data['locality']) + 1] = 'Изменить количество доставщика'
                    update.message.reply_text('Выберите доставщика для изменения',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Наличие':
                    reply_keyboard = [[elem] for elem in deliverymen]
                    reply_keyboard.append(['Общее'])
                    reply_keyboard.append(['Назад'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Наличие'
                    update.message.reply_text('Выберите доставщика',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Проверка':
                    db_sess = db_session.create_session()
                    send_on_check = db_sess.query(Sales).filter(Sales.on_check == True, Sales.is_send == False).all()
                    if send_on_check:
                        context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Проверка 1'
                        reply_keyboard = []
                        for elem in send_on_check:
                            reply_keyboard.append([str(elem.date) + ' ' +
                                                   str(db_sess.query(
                                                       Deliverymen).get(elem.deliveryman_id).name) + ' ' +
                                                   str(elem.total)])
                        reply_keyboard.append(['Отмена'])
                        update.message.reply_text('Выберите дату',
                                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                                   one_time_keyboard=True))
                    else:
                        update.message.reply_text('Ничего не найдено')
                        return start(update, context)
                elif update.message.text == 'Статистика':
                    reply_keyboard = [[elem] for elem in deliverymen]
                    reply_keyboard.append(['Общее'])
                    reply_keyboard.append(['Назад'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Статистика'
                    update.message.reply_text('Выберите доставщика',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
            #
            # Добавление новой линейки
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Добавить линейку':
                if update.message.text == 'Назад':
                    return start(update, context)
                else:
                    context.user_data['new_good'] = {0: update.message.text.split('\n')[0]}
                    db_sess = db_session.create_session()
                    db_sess.add(Brends(brend=context.user_data['new_good'][0],
                                       price=int(update.message.text.split('\n')[1]),
                                       discount_1=int(update.message.text.split('\n')[3].split('/')[0]),
                                       discount_2=int(update.message.text.split('\n')[3].split('/')[1]),
                                       salary=int(update.message.text.split('\n')[2])))
                    db_sess.commit()
                    context.user_data['locality'][
                        len(context.user_data['locality']) + 1] = 'Добавить вкус новой линейки'
                    update.message.reply_text(
                        f'Введите вкусы {context.user_data["new_good"][0]}, каждый с новой строки',
                        reply_markup=ReplyKeyboardMarkup([['Отмена']],
                                                         resize_keyboard=True,
                                                         one_time_keyboard=True))
            elif context.user_data['locality'][len(context.user_data['locality'])] == \
                    'Добавить вкус новой линейки':
                if update.message.text == 'Отмена':
                    return start(update, context)
                else:
                    if add_goods(context.user_data['new_good'][0], update.message.text.split('\n')):
                        update.message.reply_text('Бренд и вкусы успешно добавлены')
                    else:
                        update.message.reply_text('Ошибка')
                    return start(update, context)
            #
            # Изменение линейки
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Изменить линейку':
                if update.message.text == 'Назад':
                    return start(update, context)
                else:
                    brend_id = check_brend(update.message.text)
                    if brend_id:
                        brend = db_session.create_session().query(Brends).get(brend_id)
                        context.user_data['redactor_brend'] = {0: brend_id}
                        context.user_data['locality'][
                            len(context.user_data['locality']) + 1] = 'Выбор изменения в линейке'
                        update.message.reply_text('Что вы хотите изменить?',
                                                  reply_markup=ReplyKeyboardMarkup([[f'Цену {brend.price}'],
                                                                                    [f'Название {brend.brend}'],
                                                                                    [f'Зарплату {brend.salary}'],
                                                                                    [f'Скидку {brend.discount_1}/'
                                                                                     f'{brend.discount_2}'],
                                                                                    ['Изменить вкус'],
                                                                                    ['Добавить вкус'],
                                                                                    ['Отмена']],
                                                                                   resize_keyboard=True,
                                                                                   one_time_keyboard=True))
                    else:
                        update.message.reply_text('Линейка не найдена')
                        return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Выбор изменения в линейке':
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif update.message.text.split(' ')[0] == 'Цену':
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Изменение цены в линейке'
                    update.message.reply_text('Введите новую цену',
                                              reply_markup=ReplyKeyboardMarkup([['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text.split(' ')[0] == 'Название':
                    context.user_data['locality'][
                        len(context.user_data['locality']) + 1] = 'Изменение названия в линейке'
                    update.message.reply_text('Введите новое название',
                                              reply_markup=ReplyKeyboardMarkup([['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text.split(' ')[0] == 'Зарплату':
                    context.user_data['locality'][
                        len(context.user_data['locality']) + 1] = 'Изменение зарплаты в линейке'
                    update.message.reply_text('Введите новую зарплату',
                                              reply_markup=ReplyKeyboardMarkup([['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Изменить вкус':
                    reply_keyboard = [[elem.title] for elem in db_session.create_session().query(
                        Goods.title).filter(
                        Goods.brend_id == context.user_data['redactor_brend'][0]).all()]
                    reply_keyboard.append(['Отмена'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Изменить вкус'
                    update.message.reply_text('Выберите вкус для изменения',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Добавить вкус':
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Добавить вкус'
                    update.message.reply_text('Введите название вкуса',
                                              reply_markup=ReplyKeyboardMarkup([['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text.split(' ')[0] == 'Скидку':
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Изменить скидку'
                    update.message.reply_text('Введите новую скидку через /',
                                              reply_markup=ReplyKeyboardMarkup([['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Нажмите кнопку',
                                              reply_markup=ReplyKeyboardMarkup([['Цену'],
                                                                                ['Название'],
                                                                                ['Изменить вкус'],
                                                                                ['Добавить вкус'],
                                                                                ['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Изменение цены в линейке':
                if update.message.text == 'Отмена':
                    return start(update, context)
                if redact_brend_price(context.user_data['redactor_brend'][0], int(update.message.text)):
                    update.message.reply_text('Цена успешно изменена')
                else:
                    update.message.reply_text('Ошибка')
                return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Изменение названия в линейке':
                if update.message.text == 'Отмена':
                    return start(update, context)
                if redact_brend_title(context.user_data['redactor_brend'][0], update.message.text):
                    update.message.reply_text('Название успешно изменено')
                else:
                    update.message.reply_text('Ошибка')
                return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Изменение зарплаты в линейке':
                if update.message.text == 'Отмена':
                    return start(update, context)
                if redact_brend_salary(context.user_data['redactor_brend'][0], update.message.text):
                    update.message.reply_text('Зарплата успешно изменена')
                else:
                    update.message.reply_text('Ошибка')
                return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Изменить вкус':
                if update.message.text == 'Отмена':
                    return start(update, context)
                else:
                    context.user_data['redactor_brend'][1] = update.message.text
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Новое название вкуса'
                    update.message.reply_text('Введите новое название вкуса',
                                              reply_markup=ReplyKeyboardMarkup([['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Добавить вкус':
                if update.message.text == 'Отмена':
                    return start(update, context)
                else:
                    if add_good(context.user_data['redactor_brend'][0], update.message.text):
                        update.message.reply_text('Вкус успешно добавлен')
                    else:
                        update.message.reply_text('Ошибка')
                return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Новое название вкуса':
                if update.message.text == 'Отмена':
                    return start(update, context)
                if redact_good_title(context.user_data['redactor_brend'][0], context.user_data['redactor_brend'][1],
                                     update.message.text):
                    update.message.reply_text('Название успешно изменено')
                else:
                    update.message.reply_text('Ошибка')
                return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Изменить скидку':
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif '/' in update.message.text:
                    db_sess = db_session.create_session()
                    brend = db_sess.query(Brends).get(context.user_data['redactor_brend'][0])
                    brend.discount_1 = int(update.message.text.split('/')[0])
                    brend.discount_2 = int(update.message.text.split('/')[1])
                    db_sess.add(brend)
                    db_sess.commit()
                    update.message.reply_text('Успешно')
                else:
                    update.message.reply_text('Ошибка')
                return start(update, context)
            #
            # Изменение количества у доставщика
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Изменить количество доставщика':
                context.user_data['add_amount'] = {'delivery_good_id': None, 'brend_id': None,
                                                   'good_id': None, 'deliveryman_id': None, 'amount': None}
                db_sess = db_session.create_session()
                if update.message.text == 'Назад':
                    return start(update, context)
                elif (update.message.text,) in db_sess.query(Deliverymen.name).all():
                    context.user_data['add_amount']['deliveryman_id'] = db_sess.query(
                        Deliverymen).filter(Deliverymen.name == update.message.text).first().id
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Выбор изменения доставщика'
                    update.message.reply_text('Выберите, что хотите сделать',
                                              reply_markup=ReplyKeyboardMarkup([['Убавить товар'],
                                                                                ['Добавить товар'],
                                                                                ['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Выбор изменения доставщика':
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif update.message.text == 'Убавить товар':
                    reply_keyboard = [[elem.brend] for elem in db_session.create_session().query(
                        Brends).all()]
                    reply_keyboard.append(['Отмена'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Убавить товар'
                    update.message.reply_text('Выберите линейку для изменения',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Добавить товар':
                    reply_keyboard = [[elem.brend] for elem in db_session.create_session().query(Brends).all()]
                    reply_keyboard.append(['Отмена'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Добавить товар'
                    update.message.reply_text('Выберите линейку для изменения',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Убавить товар':
                db_sess = db_session.create_session()
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif (update.message.text,) in db_sess.query(Brends.brend).all():
                    brend = db_sess.query(Brends).filter(Brends.brend == update.message.text).first()
                    context.user_data['add_amount']['brend_id'] = brend.id
                    reply_keyboard = [[f"{elem.title} - "
                                       f"{get_amount(db_sess, elem, context)}"]
                                      for elem in db_sess.query(Goods).filter(Goods.brend == brend).all()]
                    reply_keyboard.append(['Отмена'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = \
                        'Выбрать товар доставщика убавления'
                    update.message.reply_text('Выберите товар линейки',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Добавить товар':
                db_sess = db_session.create_session()
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif (update.message.text,) in db_sess.query(Brends.brend).all():
                    brend = db_sess.query(Brends).filter(Brends.brend == update.message.text).first()
                    context.user_data['add_amount']['brend_id'] = brend.id
                    reply_keyboard = [[f"{elem.title} - "
                                       f"{get_amount(db_sess, elem, context)}"]
                                      for elem in db_sess.query(Goods).filter(Goods.brend == brend).all()]
                    reply_keyboard.append(['Отмена'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = \
                        'Выбрать товар доставщика добавления'
                    update.message.reply_text('Выберите товар линейки',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == \
                    'Выбрать товар доставщика убавления':
                db_sess = db_session.create_session()
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif (update.message.text.split(' -')[0],) in db_sess.query(Goods.title).all():
                    good_deliver = db_sess.query(Delivery_goods).filter(
                        Delivery_goods.good_id == db_sess.query(
                            Goods
                        ).filter(
                            Goods.title == update.message.text.split(' -')[0],
                            Goods.brend_id == context.user_data['add_amount']['brend_id']
                        ).first().id,
                        Delivery_goods.deliveryman_id == context.user_data['add_amount']['deliveryman_id']).first()
                    context.user_data['add_amount']['delivery_good_id'] = good_deliver.id
                    context.user_data['add_amount']['amount'] = good_deliver.amount
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Ввод количества убавления'
                    update.message.reply_text(f"Введите количество товара"
                                              f" меньше {context.user_data['add_amount']['amount']}",
                                              reply_markup=ReplyKeyboardMarkup([['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == \
                    'Выбрать товар доставщика добавления':
                db_sess = db_session.create_session()
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif (update.message.text.split(' -')[0],) in db_sess.query(Goods.title).all():
                    good_deliver = db_sess.query(Delivery_goods).filter(
                        Delivery_goods.good_id == db_sess.query(
                            Goods
                        ).filter(
                            Goods.title == update.message.text.split(' -')[0],
                            Goods.brend_id == context.user_data['add_amount']['brend_id']
                        ).first().id,
                        Delivery_goods.deliveryman_id ==
                        context.user_data['add_amount']['deliveryman_id']).first()
                    context.user_data['add_amount']['delivery_good_id'] = good_deliver.id
                    context.user_data['add_amount']['amount'] = good_deliver.amount
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = \
                        'Ввод количества добавления'
                    update.message.reply_text('Введите количество товара',
                                              reply_markup=ReplyKeyboardMarkup([['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == \
                    'Ввод количества убавления':
                try:
                    if update.message.text == 'Отмена':
                        return start(update, context)
                    elif 0 < int(update.message.text) <= context.user_data['add_amount']['amount']:
                        db_sess = db_session.create_session()
                        good_deliver = db_sess.query(Delivery_goods).filter(Delivery_goods.id ==
                                                                            context.user_data['add_amount']
                                                                            ['delivery_good_id']).first()
                        good_deliver.amount -= int(update.message.text)
                        db_sess.add(good_deliver)
                        db_sess.commit()
                        context.user_data['locality'][len(context.user_data['locality']) + 1] = \
                            'Согласие на возврат к вкусам'
                        update.message.reply_text('Хотите ещё изменить количество у других вкусов?',
                                                  reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']],
                                                                                   resize_keyboard=True,
                                                                                   one_time_keyboard=True))
                    else:
                        update.message.reply_text(f'Введённое количество превышает количество товара или'
                                                  f' меньше 0. Введите его снова')
                except:
                    update.message.reply_text(f'Ошибка. Введите еще раз')
            elif context.user_data['locality'][len(context.user_data['locality'])] == \
                    'Ввод количества добавления':
                try:
                    if update.message.text == 'Отмена':
                        return start(update, context)
                    else:
                        db_sess = db_session.create_session()
                        good_deliver = db_sess.query(Delivery_goods).filter(Delivery_goods.id ==
                                                                            context.user_data['add_amount']
                                                                            ['delivery_good_id']).first()
                        good_deliver.amount += int(update.message.text)
                        db_sess.add(good_deliver)
                        db_sess.commit()
                        context.user_data['locality'][len(context.user_data['locality']) + 1] = \
                            'Согласие на возврат к вкусам'
                        update.message.reply_text(f'Успешно. Хотите проделать то'
                                                  f' же действие с другими вкусами?',
                                                  reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']],
                                                                                   resize_keyboard=True,
                                                                                   one_time_keyboard=True))
                except:
                    update.message.reply_text(f"Ошибка. Введите еще раз")
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Согласие на возврат к вкусам':
                if update.message.text == 'Да':
                    context.user_data['locality'] = dict(itertools.islice(context.user_data['locality'].items(),
                                                                          len(context.user_data['locality']) - 2))
                    db_sess = db_session.create_session()
                    reply_keyboard = [[f"{elem.title} - {get_amount(db_sess, elem, context)}"] for elem in
                                      db_sess.query(
                                          Goods
                                      ).filter(
                                          Goods.brend_id == context.user_data['add_amount']['brend_id']).all()]
                    reply_keyboard.append(['Отмена'])
                    update.message.reply_text(f"Выберите товар линейки",
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Нет':
                    return start(update, context)
                else:
                    update.message.reply_text(f'Ошибка. Выберите еще раз',
                                              reply_markup=ReplyKeyboardMarkup([['Да'], ['Нет']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                #
                # Наличие жидкости
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Наличие':
                db_sess = db_session.create_session()
                if update.message.text == 'Назад':
                    return start(update, context)
                elif update.message.text == 'Общее':
                    text_amount = f'Общее наличие:\n'
                    for elem in db_sess.query(Brends).all():
                        text_amount += f'\n{elem.brend}\n'
                        for ele in db_sess.query(Goods).filter(Goods.brend == elem).all():
                            amount_good = 0
                            for el in db_sess.query(Delivery_goods).filter(Delivery_goods.good == ele).all():
                                amount_good += el.amount
                            text_amount += f'{ele.title} {amount_good}\n'
                    update.message.reply_text(text_amount)
                elif (update.message.text,) in db_sess.query(Deliverymen.name).all():
                    deliver = db_sess.query(Deliverymen).filter(Deliverymen.name == update.message.text).first()
                    text_amount = f'Жидкость в наличии у {deliver.name}:\n'
                    for elem in db_sess.query(Brends).all():
                        text_amount += f'\n{elem.brend}\n'
                        for el in db_sess.query(Goods).filter(Goods.brend == elem).all():
                            deliv_good = db_sess.query(Delivery_goods).filter(
                                Delivery_goods.good == el,
                                Delivery_goods.deliveryman == deliver).first()
                            text_amount += f'{el.title} {deliv_good.amount}\n'
                    update.message.reply_text(text_amount)
                    return start(update, context)
                else:
                    update.message.reply_text('Ошибка')
                return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Проверка 1':
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif '-' in update.message.text:
                    db_sess = db_session.create_session()
                    sales_good = db_sess.query(Sales).filter(
                        Sales.date == datetime.date(int(update.message.text.split(' ')[0].split('-')[0]),
                                                    int(update.message.text.split(' ')[0].split('-')[1]),
                                                    int(update.message.text.split(' ')[0].split('-')[2]))).first()
                    if sales_good:
                        sales_good.is_send = True
                        db_sess.add(sales_good)
                        db_sess.commit()
                        update.message.reply_text('Проверено')
                        return start(update, context)
                    else:
                        update.message.reply_text('Ничего не найдено')
                        return start(update, context)
                else:
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Статистика':
                db_sess = db_session.create_session()
                if update.message.text == 'Назад':
                    return start(update, context)
                elif update.message.text == 'Общее':
                    context.user_data['deliveryman'] = None
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Статистика 2'
                    reply_keyboard = [['Число месяца'], ['Месяц'], ['Отмена']]
                    update.message.reply_text('Выберите промежуток',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif (update.message.text,) in db_sess.query(Deliverymen.name).all():
                    context.user_data['deliveryman'] = db_sess.query(Deliverymen).filter(
                        Deliverymen.name == update.message.text).first().id
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Статистика 2'
                    reply_keyboard = [['Число месяца'], ['Месяц'], ['Отмена']]
                    update.message.reply_text('Выберите промежуток',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Статистика 2':
                db_sess = db_session.create_session()
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif update.message.text == 'Месяц':
                    if context.user_data['deliveryman']:
                        salary = 0
                        total = 0
                        amount = 0
                        for elem in db_sess.query(Sales).filter(
                                Sales.deliveryman_id == context.user_data['deliveryman'],
                                extract('month', Sales.date) == datetime.datetime.now().date().month,
                                extract('year', Sales.date) == datetime.datetime.now().date().year,
                                Sales.is_send == True).all():
                            salary += elem.sales_salary
                            total += elem.total
                            amount += len(elem.deliverygood_ids.split('&'))
                        update.message.reply_text(f"Статистика "
                                                  f"{db_sess.query(Deliverymen).get(context.user_data['deliveryman']).name}\n"
                                                  f"Зарплата: {salary}\n"
                                                  f"Скинуто: {total}\n"
                                                  f"Продано штук: {amount}\n"
                                                  f"Средняя цена позиции: {(total + salary) / amount if amount > 0 else 0}\n")
                        return start(update, context)
                    else:
                        salary = 0
                        total = 0
                        amount = 0
                        for elem in db_sess.query(Sales).filter(
                                extract('month', Sales.date) == datetime.datetime.now().date().month,
                                extract('year', Sales.date) == datetime.datetime.now().date().year,
                                Sales.is_send == True).all():
                            salary += elem.sales_salary
                            total += elem.total
                            amount += len(elem.deliverygood_ids.split('&'))
                        update.message.reply_text(f"Статистика общее\n"
                                                  f"Зарплата: {salary}\n"
                                                  f"Скинуто: {total}\n"
                                                  f"Продано штук: {amount}\n"
                                                  f"Средняя цена позиции: {(total + salary) / amount if amount > 0 else 0}\n")
                        return start(update, context)
                elif update.message.text == 'Число месяца':
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Статистика 3'
                    if context.user_data['deliveryman']:
                        reply_keyboard = [[str(elem.date)] for elem in db_sess.query(Sales).filter(
                            Sales.deliveryman_id == context.user_data['deliveryman'],
                            extract('month', Sales.date) == datetime.datetime.now().date().month,
                            extract('year', Sales.date) == datetime.datetime.now().date().year,
                            Sales.is_send == True).all()]
                        reply_keyboard.append(['Отмена'])
                        update.message.reply_text('Выберите день',
                                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                                   resize_keyboard=True,
                                                                                   one_time_keyboard=True))
                    else:
                        reply_keyboard = [[str(elem.date)] for elem in db_sess.query(Sales).filter(
                            extract('month', Sales.date) == datetime.datetime.now().date().month,
                            extract('year', Sales.date) == datetime.datetime.now().date().year,
                            Sales.is_send == True).all()]
                        reply_keyboard.append(['Отмена'])
                        update.message.reply_text('Выберите день',
                                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                                   resize_keyboard=True,
                                                                                   one_time_keyboard=True))
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Статистика 3':
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif '-' in update.message.text:
                    db_sess = db_session.create_session()
                    if context.user_data['deliveryman']:
                        sales_good = db_sess.query(Sales).filter(
                            Sales.deliveryman_id == context.user_data['deliveryman'],
                            Sales.date == datetime.date(int(update.message.text.split('-')[0]),
                                                        int(update.message.text.split('-')[1]),
                                                        int(update.message.text.split('-')[2]))
                        ).first()
                        kolvo = len(sales_good.deliverygood_ids.split('&'))
                        sredn = (sales_good.total + sales_good.sales_salary) / kolvo if kolvo > 0 else 0
                        update.message.reply_text(f"Статитстика"
                                                  f"{db_sess.query(Deliverymen).get(context.user_data['deliveryman']).name}\n"
                                                  f"Зарплата: {sales_good.sales_salary}\n"
                                                  f"Скинуто: {sales_good.total}\n"
                                                  f"Продано штук: {kolvo}\n"
                                                  f"Средняя цена позиции: {sredn}")
                        return start(update, context)
                    else:
                        salary = 0
                        total = 0
                        amount = 0
                        for elem in db_sess.query(Sales).filter(
                                Sales.date == datetime.date(int(update.message.text.split('-')[0]),
                                                            int(update.message.text.split('-')[1]),
                                                            int(update.message.text.split('-')[2]))).all():
                            salary += elem.sales_salary
                            total += elem.total
                            amount += len(elem.deliverygood_ids.split("&"))
                        update.message.reply_text(f'Статитстика общее\n'
                                                  f'Зарплата: {salary}\n'
                                                  f'Скинуто: {total}\n'
                                                  f'Продано штук: {amount}\n'
                                                  f'Средняя цена позиции: {(salary + total) / amount if amount > 0 else 0}\n')
                        return start(update, context)
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
        #
        # Меню доставщика
        elif update.message.chat.id in deliverymen.values():
            if context.user_data['locality'][len(context.user_data['locality'])] == 'Старт':
                if update.message.text == 'Продать':
                    reply_keyboard = [[elem.brend] for elem in db_session.create_session().query(
                        Brends).all()]
                    reply_keyboard.append(['Назад'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Продать 1'
                    update.message.reply_text('Выберите линейку',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Наличие':
                    db_sess = db_session.create_session()
                    deliver = db_sess.query(Deliverymen).get(context.user_data['user_id_db'])
                    text_amount = f'Жидкость в наличии у {deliver.name}:\n'
                    for elem in db_sess.query(Brends).all():
                        text_amount += f'\n{elem.brend}\n'
                        for el in db_sess.query(Goods).filter(Goods.brend == elem).all():
                            deliv_good = db_sess.query(Delivery_goods).filter(
                                Delivery_goods.good == el,
                                Delivery_goods.deliveryman == deliver).first()
                            text_amount += f'{el.title} {deliv_good.amount}\n'
                    update.message.reply_text(text_amount)
                    return start(update, context)
                elif update.message.text == 'Отправить на проверку':
                    send_on_check = db_session.create_session().query(Sales).filter(Sales.on_check == False).all()
                    if send_on_check:
                        context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Проверка 1'
                        reply_keyboard = [[str(elem.date) + ' ' + str(elem.total)] for elem in send_on_check]
                        reply_keyboard.append(['Отмена'])
                        update.message.reply_text('Выберите дату',
                                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                                   one_time_keyboard=True))
                    else:
                        update.message.reply_text('Ничего не найдено')
                        return start(update, context)
                elif update.message.text == 'Статистика за день':
                    today = db_session.create_session().query(Sales).filter(
                        Sales.deliveryman_id == context.user_data['user_id_db'],
                        Sales.date == datetime.datetime.now().date()).first()
                    if today:
                        sredn = (today.total + today.sales_salary) / len(today.deliverygood_ids.split("&"))
                        update.message.reply_text(f'Зарплата: {today.sales_salary}\n'
                                                  f'Скинуть: {today.total}\n'
                                                  f'Продано штук: {len(today.deliverygood_ids.split("&"))}\n'
                                                  f'Средняя цена позиции: {sredn}\n')
                    else:
                        update.message.reply_text('Пока что ничего не продано')
                    return start(update, context)
                elif update.message.text == 'Статистика за месяц':
                    month = db_session.create_session().query(Sales).filter(
                        Sales.deliveryman_id == context.user_data['user_id_db'],
                        extract('month', Sales.date) == datetime.datetime.now().date().month,
                        extract('year', Sales.date) == datetime.datetime.now().date().year,
                        Sales.is_send == True).all()
                    salary = 0
                    total = 0
                    amount = 0
                    for elem in month:
                        salary += elem.sales_salary
                        total += elem.total
                        amount += len(elem.deliverygood_ids.split("&"))
                    update.message.reply_text(f'Зарплата: {salary}\n'
                                              f'Скинуто: {total}\n'
                                              f'Продано штук: {amount}\n'
                                              f'Средняя цена позиции: {(salary + total) / amount if amount > 0 else 0}\n')
                    return start(update, context)
                elif update.message.text == 'Нужно перевести':
                    need_send = db_session.create_session().query(Sales).filter(
                        Sales.deliveryman_id == context.user_data['user_id_db'],
                        Sales.is_send == False).all()
                    stroka = ''
                    for elem in need_send:
                        stroka += f"{elem.date}\n" \
                                  f"{elem.total}\n\n"
                    if stroka != '':
                        update.message.reply_text(stroka + 'Не забывай приписку долг и сегодняшнюю дату')
                    else:
                        update.message.reply_text('Всё скинуто')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Продать 1':
                brend_id = check_brend(update.message.text)
                if update.message.text == 'Назад':
                    return start(update, context)
                elif brend_id:
                    db_sess = db_session.create_session()
                    context.user_data['sell_good'] = {'brend_id': brend_id}
                    reply_keyboard = [[f"{elem.title} - "
                                       f"{get_amount_2(db_sess, elem, context.user_data['user_id_db'])}"]
                                      for elem in db_sess.query(Goods).filter(Goods.brend_id == brend_id).all() if
                                      get_amount_2(
                                          db_sess,
                                          elem,
                                          context.user_data['user_id_db']) > 0]
                    reply_keyboard.append(['Отмена'])
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = \
                        'Продать 2'
                    update.message.reply_text('Выберите товар линейки',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Линейка не найдена')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Продать 2':
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif (update.message.text.split(' -')[0],) in db_session.create_session().query(Goods.title).all():
                    context.user_data['sell_good']['delivery_good_title'] = update.message.text.split(' -')[0]
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = \
                        'Продать 3'
                    update.message.reply_text('Скидка',
                                              reply_markup=ReplyKeyboardMarkup([['0'], ['1'], ['2'], ['Отмена']],
                                                                               resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Продать 3':
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif update.message.text in ['0', '1', '2']:
                    db_sess = db_session.create_session()
                    good_deliver = db_sess.query(Delivery_goods).filter(
                        Delivery_goods.good_id == db_sess.query(
                            Goods
                        ).filter(
                            Goods.title == context.user_data['sell_good']['delivery_good_title'],
                            Goods.brend_id == context.user_data['sell_good']['brend_id']
                        ).first().id,
                        Delivery_goods.deliveryman_id ==
                        context.user_data['user_id_db']).first()
                    if sell_good(good_deliver.id, context.user_data['user_id_db'],
                                 context.user_data['sell_good']['brend_id'], update.message.text):
                        good_deliver.amount -= 1
                        db_sess.add(good_deliver)
                        db_sess.commit()
                        update.message.reply_text('Успешно!')
                    else:
                        update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Проверка 1':
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif '-' in update.message.text:
                    db_sess = db_session.create_session()
                    sales_good = db_sess.query(Sales).filter(
                        Sales.date == datetime.date(int(update.message.text.split(' ')[0].split('-')[0]),
                                                    int(update.message.text.split(' ')[0].split('-')[1]),
                                                    int(update.message.text.split(' ')[0].split('-')[2]))
                    ).first()
                    if sales_good:
                        sales_good.on_check = True
                        db_sess.add(sales_good)
                        db_sess.commit()
                        update.message.reply_text('Отправлено на проверку платежа')
                        return start(update, context)
                    else:
                        update.message.reply_text('Ничего не найдено')
                        return start(update, context)
                else:
                    return start(update, context)
        else:
            if context.user_data['locality'][len(context.user_data['locality'])] == 'Старт':
                if update.message.text == 'Наличие':
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Наличие 1'
                    reply_keyboard = [[elem.name] for elem in db_session.create_session().query(Deliverymen).all()]
                    reply_keyboard.append(['Отмена'])
                    update.message.reply_text('Выберите доставщика',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                               one_time_keyboard=True))
                elif update.message.text == 'Доставка':
                    update.message.reply_text(text_chat)
                    return start(update, context)
                else:
                    update.message.reply_text('Ошибка')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Наличие 1':
                db_sess = db_session.create_session()
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif (update.message.text,) in db_sess.query(Deliverymen.name).all():
                    deliver = db_sess.query(Deliverymen).filter(
                        Deliverymen.name == update.message.text).first()
                    context.user_data['user'] = deliver.id
                    context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Наличие 2'
                    reply_keyboard = [[elem.brend] for elem in db_sess.query(Brends).all()]
                    reply_keyboard.append(['Отмена'])
                    update.message.reply_text('Выберите линейку',
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                               one_time_keyboard=True))
                else:
                    update.message.reply_text('Ничего не найдено')
                    return start(update, context)
            elif context.user_data['locality'][len(context.user_data['locality'])] == 'Наличие 2':
                db_sess = db_session.create_session()
                if update.message.text == 'Отмена':
                    return start(update, context)
                elif (update.message.text,) in db_sess.query(Brends.brend).all():
                    brend_good = db_sess.query(Brends).filter(Brends.brend == update.message.text).first()
                    deliver = db_sess.query(Deliverymen).get(context.user_data['user'])
                    text_amount = f'Жидкость {brend_good.brend + " " + str(brend_good.price)} рублей у' \
                                  f' {delyverymen_id[deliver.name]}:\n'
                    for el in db_sess.query(Goods).filter(Goods.brend == brend_good).all():
                        deliv_good = db_sess.query(Delivery_goods).filter(
                            Delivery_goods.good == el,
                            Delivery_goods.deliveryman == deliver).first()
                        text_amount += f'{el.title} {deliv_good.amount}\n'
                    update.message.reply_text(text_amount)
                    return start(update, context)
                else:
                    update.message.reply_text('Ничего не найдено')
                    return start(update, context)
    except Exception as e:
        update.message.reply_text(f'Ошибка {e}')
        return start(update, context)


def sell_good(delivery_id, deliveryman_id, brend_id, discount_number):
    db_sess = db_session.create_session()
    sold = db_sess.query(Sales).filter(Sales.date == datetime.datetime.now().date(),
                                       Sales.deliveryman_id == deliveryman_id).first()
    brend_delivery_good = db_sess.query(Brends).get(
        db_sess.query(Goods).get(
            db_sess.query(Delivery_goods).get(
                delivery_id).good_id).brend_id)
    if discount_number == '0':
        discount = 0
    elif discount_number == '1':
        discount = db_sess.query(Brends).get(brend_id).discount_1
    elif discount_number == '2':
        discount = db_sess.query(Brends).get(brend_id).discount_2
    if sold:
        sold.deliverygood_ids += f'&{delivery_id}.{discount}'
        sold.total += brend_delivery_good.price - brend_delivery_good.salary - discount
        sold.sales_salary += brend_delivery_good.salary
        db_sess.add(sold)
        db_sess.commit()
    else:
        db_sess.add(Sales(date=datetime.datetime.now().date(),
                          deliveryman_id=deliveryman_id,
                          deliverygood_ids=f'{delivery_id}.{discount}',
                          sales_salary=brend_delivery_good.salary,
                          total=brend_delivery_good.price - brend_delivery_good.salary - discount))
        db_sess.commit()
    return True


def get_amount_2(db_sess, elem, id):
    return db_sess.query(Delivery_goods).filter(
        Delivery_goods.good == elem,
        Delivery_goods.deliveryman_id == id).first().amount


def get_amount(db_sess, elem, context):
    return db_sess.query(Delivery_goods).filter(
        Delivery_goods.good == elem,
        Delivery_goods.deliveryman_id == context.user_data['add_amount']['deliveryman_id']).first().amount


def redact_good_title(id, old_title, new_title):
    db_sess = db_session.create_session()
    good = db_sess.query(Goods).filter(Goods.brend_id == id, Goods.title == old_title).first()
    good.title = new_title
    db_sess.add(good)
    db_sess.commit()
    return True


def check_brend(brend):
    brend_id = db_session.create_session().query(Brends).filter(Brends.brend == brend).first()
    if brend_id is not None:
        return brend_id.id
    else:
        return False


def redact_brend_price(id, price):
    db_sess = db_session.create_session()
    brend = db_sess.query(Brends).get(id)
    brend.price = price
    db_sess.add(brend)
    db_sess.commit()
    return True


def redact_brend_title(id, title):
    db_sess = db_session.create_session()
    brend = db_sess.query(Brends).get(id)
    brend.brend = title
    db_sess.add(brend)
    db_sess.commit()
    return True


def redact_brend_salary(id, salary):
    db_sess = db_session.create_session()
    brend = db_sess.query(Brends).get(id)
    brend.salary = salary
    db_sess.add(brend)
    db_sess.commit()
    return True


def add_good(id, title):
    db_sess = db_session.create_session()
    brend = db_sess.query(Brends).filter(Brends.id == id).first()
    if (title,) not in db_sess.query(Goods.title).filter(Goods.brend_id == id).all():
        db_sess.add(Goods(title=title, brend=brend))
        db_sess.commit()
        good = db_sess.query(Goods).filter(Goods.brend == brend, Goods.title == title).first()
        for el in db_sess.query(Deliverymen).all():
            delivery_good = Delivery_goods(amount=0, good=good, deliveryman=el)
            db_sess.add(delivery_good)
            db_sess.commit()
        return True


def add_goods(title, list_goods):
    db_sess = db_session.create_session()
    brend = db_sess.query(Brends).filter(Brends.brend == title).first()
    for elem in list_goods:
        db_sess.add(Goods(title=elem, brend=brend))
        db_sess.commit()
        good = db_sess.query(Goods).filter(Goods.brend == brend, Goods.title == elem).first()
        for el in db_sess.query(Deliverymen).all():
            delivery_good = Delivery_goods(amount=0, good=good, deliveryman=el)
            db_sess.add(delivery_good)
            db_sess.commit()
    return True


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    db_session.global_init(f"db/goods.db")
    add_deliverymen(deliverymen)
    main()
