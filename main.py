from bot import bot
from telebot import types
from config import APP_URL, TOKEN, PORT
from flask import Flask, request
from utils import send_mess_to_admin


app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def get_updates():
    """This func provides url for telebot webhook."""

    json_string = request.stream.read().decode("utf-8")
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "All OK"


@app.route("/")
def webhook():
    """Set telebot webhook."""

    bot.remove_webhook()
    bot.set_webhook(url="{}{}".format(APP_URL, TOKEN))
    return "Succsess! Webhook is thrown"


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
    # bot.remove_webhook()
    # bot.polling(none_stop=True)
