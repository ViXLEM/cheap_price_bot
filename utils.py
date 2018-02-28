import requests

from bot import bot
from config import ADMIN_CHAT_ID
from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image
from io import BytesIO
from models import Session, Product, NovusProduct, AuchanProduct, MMProduct


def send_mess_to_admin(text='check_mess_to_ADMIN'):
    """Send message to administrator.

    Args:
    text (str): String line which will be send to admin.
    """

    bot.send_message(ADMIN_CHAT_ID, text)


def search_in_db(barcode):
    """Search product in main db by barcode and return product data.

    Args:
    barcode (str): Product's barcode which need search.

    Returns:
    str: Product data if product was search. Standart responsee if wasn't search
    """

    session = Session()
    product = session.query(Product).filter_by(barcode=barcode).first()
    response_message = ''
    if product:
        response_message += '{}\n'.format(product.name)
        if product.barcode_auchan:
            price = session.query(AuchanProduct).filter_by(barcode=barcode).first().price
            response_message += '\nAUCHAN: {}\n'.format(price)
        if product.barcode_mm:
            price = session.query(MMProduct).filter_by(barcode=barcode).first().price
            response_message += 'MegaMarket: {}\n'.format(price)
        if product.barcode_novus:
            price = session.query(NovusProduct).filter_by(barcode=barcode).first().price
            response_message += 'NOVUS: {}\n'.format(price)
        response_message += '\nBarcode: {}'.format(barcode)
    else:
        response_message = 'This product was not found in our DB. Maybe you send wrong barcode?'
    session.close()
    return response_message


def get_barcode_from_photo(url):
    """Separate barcode from picture.

    Args:
    url (str): Photo url.

    Returns:
    str: Barcode value if was found, None otherwise.
    """

    response = requests.get(url)
    photo = Image.open(BytesIO(response.content))
    decoded_data = decode(image=photo, symbols=[ZBarSymbol.EAN13])
    if decoded_data:
        barcode = decoded_data[0].data.decode("utf-8")
    else:
        barcode = None
    return barcode
