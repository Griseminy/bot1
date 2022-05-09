import logging
from random import shuffle

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler

from data import db_session
from data.goods import Goods
from data.brends import Brends


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
            update.message.reply_text('Введите название и цену через пробел', reply_markup=markup)
    elif context.user_data['locality'][len(context.user_data['locality'])] == 'Добавить линейку':
        if update.message.text == 'Назад':
            # update.message.reply_text('Введите вкусы')
            # context.user_data['locality'].pop(1)
            return start(update, context)
        else:
            context.user_data['new_good'] = {}
            context.user_data['new_good'][0] = update.message.text.split(' ')[0]
            context.user_data['new_good'][1] = int(update.message.text.split(' ')[1])
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
            db_sess = db_session.create_session()
            brend = db_sess.query(Brends).filter(Brends.brend == context.user_data['new_good'][0]).first()
            for elem in update.message.text.split('\n'):
                goods = Goods(title=elem, amount=0, brend=brend)
                db_sess.add(goods)
                db_sess.commit()
            update.message.reply_text('Бренд и вкусы успешно добавлены')
            return start(update, context)

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