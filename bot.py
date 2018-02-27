import telebot

from config import TOKEN
from models import User, Session

bot = telebot.TeleBot(TOKEN)
from utils import get_barcode_from_photo, search_in_db


@bot.message_handler(commands=['start'])
def start(message):
    """Start use bot and register new user to db."""

    session = Session()
    u = session.query(User).filter_by(chat_id=message.chat.id).first()
    if u:
        return bot.send_message(message.chat.id, "You already use this serviсe")
    user = User(chat_id=message.chat.id)
    session.add(user)
    session.commit()
    session.close()
    bot.send_message(message.chat.id, "You are registered successful! "
                                      "Send /barcode that get informations "
                                      "about alcohol product")


@bot.message_handler(commands=['get_users_id'])
def get_users_id(message):
    """Send message with table id's registered users."""

    session = Session()
    text = ''
    for u in session.query(User).all():
        text += '{}|{}\n'.format(u.id, u.chat_id)
    bot.send_message(message.chat.id, text)
    session.close()


@bot.message_handler(commands=['barcode'])
def search_by_barcode(message):
    """Search barcode in db and send message with product price."""

    if len(message.text) == 8:
        bot.send_message(message.chat.id, 'Please, enter barcode\n'
                                          'For example:\n/barcode 4820000455848')
        return 'error'
    barcode = message.text.split()[1]

    response_message = search_in_db(barcode)
    bot.send_message(message.chat.id, response_message)


@bot.message_handler(commands=['help'])
def help(message):
    """Send help message with list of commands."""

    text = 'Commands:\n' \
           '/barcode ************* - get product price by barcode\n' \
           '/start - start using this bot'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def unrecognized_command(message):
    """Send message if command was unrecognized."""

    bot.send_message(message.chat.id, 'Unrecognized command\n'
                                      'Use /help to get list of commands')


@bot.message_handler(content_types=['photo'])
def get_product_from_photo(message):
    """Send mess with barcode from photo"""

    file_id = message.photo[-1].file_id
    file_path = bot.get_file(file_id).file_path
    photo_url = 'https://api.telegram.org/file/bot{token}/{path}'.format(
                token=TOKEN, path=file_path)

    barcode = get_barcode_from_photo(photo_url)
    if barcode:
        response_message = search_in_db(barcode)
    else:
        response_message = '404\nBarcode was not found :)\nPlease take '\
                           'new photo and send again'
    bot.send_message(message.chat.id, response_message)
