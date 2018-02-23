import telebot
import os
import sqlalchemy

from flask import Flask, request
from models import Base, User
from config import TOKEN, ADMIN_CHAT_ID, DATABASE_URL, APP_URL

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)
Session = sqlalchemy.orm.sessionmaker(bind=engine)


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
    bot.send_message(message.chat.id, "You are registered successful!"
                                      "Send /barcode that get informations "
                                      "about buhlo product")


@bot.message_handler(commands=['get_users_id'])
def get_users_id(message):
    session = Session()
    text = ''
    for u in session.query(User).all():
        text += '{}|{}\n'.format(u.id, u.chat_id)
    bot.send_message(message.chat.id, text)
    session.close()


@bot.message_handler(commands=['barcode'])
def main(message):
    text = 'thomething text'
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('/barcode', '/thomethingelse')
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def resend_message(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # bot.remove_webhook()
    # bot.polling(none_stop=True)
