from bot import bot
from config import ADMIN_CHAT_ID


def send_mess_to_admin(text='check_mess_to_ADMIN'):
    """Send message to administrator."""

    bot.send_message(ADMIN_CHAT_ID, text)
