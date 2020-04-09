# Trenobot Utility
import os
import warnings
import MySQLdb
import telepot


def create_bot():
    TOKEN = os.environ.get("TELEGRAM_API_KEY")
    new_bot = telepot.Bot(TOKEN)
    return new_bot


def connect_db():
    warnings.filterwarnings("ignore", category=MySQLdb.Warning)

    SERVER = os.environ.get("DATABASE_HOST")
    USER = os.environ.get("DATABASE_USER")
    PASSWORD = os.environ.get("DATABASE_PASSWORD")

    try:
        connect = MySQLdb.connect(SERVER, USER, PASSWORD)
        return connect
    except MySQLdb.Error as er:
        print(er)
    return "Connection Error!"
