import telebot

from config import TOKEN
from models import User, Session, Product, NovusProduct, AuchanProduct, MMProduct


bot = telebot.TeleBot(TOKEN)


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

    session = Session()
    product = session.query(Product).filter_by(barcode=barcode).first()
    product_info = ''
    if product:
        product_info += '{}\n\n'.format(product.name)
        if product.barcode_auchan:
            price = session.query(AuchanProduct).filter_by(barcode=barcode).first().price
            product_info += '\nAUCHAN: {}\n'.format(price)
        if product.barcode_mm:
            price = session.query(MMProduct).filter_by(barcode=barcode).first().price
            product_info += 'MegaMarket: {}\n'.format(price)
        if product.barcode_novus:
            price = session.query(NovusProduct).filter_by(barcode=barcode).first().price
            product_info += 'NOVUS: {}\n'.format(price)
        bot.send_message(message.chat.id, product_info)
    else:
        bot.send_message(message.chat.id, 'This product was not found in our DB. '
                                          'Maybe you send wrong barcode?')
    session.close()


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