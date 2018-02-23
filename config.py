import os

TOKEN = os.environ.get('TOKEN')
APP_URL = os.environ.get('APP_URL')
DATABASE_URL = os.environ.get('DATABASE_URL')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')
PORT = int(os.environ.get("PORT", 5000))
