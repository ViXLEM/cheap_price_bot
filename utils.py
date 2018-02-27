import requests

from bot import bot
from config import ADMIN_CHAT_ID
from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image
from io import BytesIO


def send_mess_to_admin(text='check_mess_to_ADMIN'):
    """Send message to administrator."""

    bot.send_message(ADMIN_CHAT_ID, text)


def get_barcode_from_photo(url):

    response = requests.get(url)
    photo = Image.open(BytesIO(response.content))
    decoded_data = decode(image=photo, symbols=[ZBarSymbol.EAN13])
    if len(decoded_data) < 1:
        barcode = decoded_data[0].data.decode("utf-8")
    else:
        barcode = None
    return barcode
