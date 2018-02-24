import telebot
import os

from flask import Flask, request
from models import User, Session, Product, NovusProduct, AuchanProduct, MMProduct
from config import TOKEN, ADMIN_CHAT_ID, APP_URL

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def get_updates():
    """This func provides url for telebot webhook."""

    json_string = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "All OK"


@app.route("/")
def webhook():
    """Set telebot webhook."""

    bot.remove_webhook()
    bot.set_webhook(url="{}{}".format(APP_URL, TOKEN))
    return "Succsess! Webhook is thrown"


def send_mess_to_admin(text='check_mess_to_ADMIN'):
    """Send message to administrator."""

    bot.send_message(ADMIN_CHAT_ID, text)


@app.route("/send_check")
def check_message():
    """Send check message to admin after click url."""

    send_mess_to_admin()
    return 'Sended succsessful!'


@app.route("/api_get_mess", methods=["POST"])
def send_metadata_message():
    """Send message to admin with metadata last update."""

    if request.method == "POST":
        data = str(request.form.to_dict())
        send_mess_to_admin(text=data)


@bot.message_handler(commands=['start'])
def start(message):
    """Register new user to db."""

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
    session = Session()
    text = ''
    for u in session.query(User).all():
        text += '{}|{}\n'.format(u.id, u.chat_id)
    bot.send_message(message.chat.id, text)
    session.close()


@bot.message_handler(commands=['barcode'])
def check_by_barcode(message):
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
            price = session.query(MMProduct).filter_by(barcode=barcode).first().price
            product_info += '\nAUCHAN: {}\n'.format(price)
        if product.barcode_mm:
            price = session.query(AuchanProduct).filter_by(barcode=barcode).first().price
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
    text = 'Commands:\n' \
           '/barcode ************* - get product price by barcode\n' \
           '/start - start using this bot'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def unrecognized_command(message):
    bot.send_message(message.chat.id, 'Unrecognized command\n'
                                      'Use /help to get list of commands')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # bot.remove_webhook()
    # bot.polling(none_stop=True)
