import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from data import db_session
from data.brends import Brends
from data.goods import Goods

# бот @echoyandbot
TOKEN = '5301614535:AAGAjCg3CopbFtvzUQVGLAkE9lOpNsbnX-Q'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def start(update, context):
    context.user_data['locality'] = {}
    context.user_data['locality'][1] = 'Старт'
    reply_keyboard = [['Наличие', 'Изменить количество'],
                      ['Добавить линейку', 'Изменить линейку'],
                      ['Статистика']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Нажмите кнопки снизу', reply_markup=markup)


def handler(update, context):
    if context.user_data['locality'][len(context.user_data['locality'])] == 'Старт':
        if update.message.text == 'Наличие':
            pass
        elif update.message.text == 'Добавить линейку':
            reply_keyboard = [['Назад']]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Добавить линейку'
            update.message.reply_text('Введите название и цену, каждый с новой строки', reply_markup=markup)
        elif update.message.text == 'Изменить линейку':
            db_sess = db_session.create_session()
            brends = db_sess.query(Brends).all()
            reply_keyboard = [[elem.brend] for elem in brends]
            reply_keyboard.append(['Назад'])
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Изменить линейку'
            update.message.reply_text('Выберите линейку для изменения', reply_markup=markup)
    elif context.user_data['locality'][len(context.user_data['locality'])] == 'Добавить линейку':
        if update.message.text == 'Назад':
            # update.message.reply_text('Введите вкусы')
            # context.user_data['locality'].pop(1)
            return start(update, context)
        else:
            context.user_data['new_good'] = {}
            context.user_data['new_good'][0] = update.message.text.split('\n')[0]
            context.user_data['new_good'][1] = int(update.message.text.split('\n')[1])
            db_sess = db_session.create_session()
            brend = Brends(brend=context.user_data['new_good'][0], price=int(context.user_data['new_good'][1]))
            db_sess.add(brend)
            db_sess.commit()
            context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Добавить вкус новой линейки'
            reply_keyboard = [['Отмена']]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            update.message.reply_text(f'Введите вкусы {context.user_data["new_good"][0]}, каждый с новой строки',
                                      reply_markup=markup)
    elif context.user_data['locality'][len(context.user_data['locality'])] == 'Добавить вкус новой линейки':
        if update.message.text == 'Отмена':
            return start(update, context)
        else:
            if add_goods(context.user_data['new_good'][0], update.message.text.split('\n')):
                update.message.reply_text('Бренд и вкусы успешно добавлены')
            else:
                update.message.reply_text('Ошибка')
            return start(update, context)
    elif context.user_data['locality'][len(context.user_data['locality'])] == 'Изменить линейку':
        if update.message.text == 'Назад':
            return start(update, context)
        else:
            brend_id = check_brend(update.message.text)
            if brend_id:
                context.user_data['redactor_brend'] = {}
                context.user_data['redactor_brend'][0] = brend_id
                reply_keyboard = [['Цену'],
                                  ['Название'],
                                  ['Изменить вкус'],
                                  ['Добавить вкус'],
                                  ['Отмена']]
                context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Выбор изменения в линейке'
                markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
                update.message.reply_text('Что вы хотите изменить?', reply_markup=markup)
            else:
                update.message.reply_text('Линейка не найдена')
                return start(update, context)
    elif context.user_data['locality'][len(context.user_data['locality'])] == 'Выбор изменения в линейке':
        if update.message.text == 'Отмена':
            return start(update, context)
        elif update.message.text == 'Цену':
            reply_keyboard = [['Отмена']]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Изменение цены в линейке'
            update.message.reply_text('Введите новую цену', reply_markup=markup)
        elif update.message.text == 'Название':
            reply_keyboard = [['Отмена']]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Изменение названия в линейке'
            update.message.reply_text('Введите новое название', reply_markup=markup)
        elif update.message.text == 'Изменить вкус':
            db_sess = db_session.create_session()
            goods = db_sess.query(Goods.title).filter(Goods.brend_id == context.user_data['redactor_brend'][0]).all()
            reply_keyboard = [[elem.title] for elem in goods]
            reply_keyboard.append(['Отмена'])
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Изменить вкус'
            update.message.reply_text('Выберите вкус для изменения', reply_markup=markup)
        elif update.message.text == 'Добавить вкус':
            reply_keyboard = [['Отмена']]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Добавить вкус'
            update.message.reply_text('Введите название вкуса', reply_markup=markup)
        else:
            reply_keyboard = [['Цену'],
                              ['Название'],
                              ['Изменить вкус'],
                              ['Добавить вкус'],
                              ['Отмена']]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            update.message.reply_text('Нажмите кнопку', reply_markup=markup)
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
    elif context.user_data['locality'][len(context.user_data['locality'])] == 'Изменить вкус':
        if update.message.text == 'Отмена':
            return start(update, context)
        else:
            context.user_data['redactor_brend'][1] = update.message.text
            context.user_data['locality'][len(context.user_data['locality']) + 1] = 'Новое название вкуса'
            reply_keyboard = [['Отмена']]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            update.message.reply_text('Введите новое название вкуса', reply_markup=markup)
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


def redact_good_title(id, old_title, new_title):
    db_sess = db_session.create_session()
    good = db_sess.query(Goods).filter(Goods.brend_id == id, Goods.title == old_title).first()
    good.title = new_title
    db_sess.add(good)
    db_sess.commit()
    return True


def check_brend(brend):
    db_sess = db_session.create_session()
    brend_id = db_sess.query(Brends).filter(Brends.brend == brend).first()
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


def add_good(id, title):
    db_sess = db_session.create_session()
    brend = db_sess.query(Brends).filter(Brends.id == id).first()
    if (title,) not in db_sess.query(Goods.title).filter(Goods.brend_id == id).all():
        good = Goods(title=title, amount=0, brend=brend)
        db_sess.add(good)
        db_sess.commit()
        return True


def add_goods(title, list_goods):
    db_sess = db_session.create_session()
    brend = db_sess.query(Brends).filter(Brends.brend == title).first()
    for elem in list_goods:
        goods = Goods(title=elem, amount=0, brend=brend)
        db_sess.add(goods)
        db_sess.commit()
    return True


# def stop(update, context):
#     pass


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handler))
    # conv_handler = ConversationHandler(
    #     # Точка входа в диалог.
    #     # В данном случае — команда /start. Она задаёт первый вопрос.
    #     entry_points=[CommandHandler('start', start)],
    #
    #     # Состояние внутри диалога.
    #     # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
    #     states={
    #         1: [MessageHandler(Filters.text & ~Filters.command, handler)]
    #         # Функция читает ответ на первый вопрос и задаёт второй.
    #     },
    #
    #     # Точка прерывания диалога. В данном случае — команда /stop.
    #     fallbacks=[CommandHandler('stop', stop)]
    # )
    #
    # dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    db_session.global_init(f"db/goods.db")
    main()
