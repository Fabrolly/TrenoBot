"""
A module to expose various utilities for the bot
"""
# Trenobot Utility
import os
import warnings
import MySQLdb
import telepot


def create_bot() -> telepot.Bot:
    """
    Create the telepot instance as a bot

    Returns:
        the bot instance
    """
    TOKEN = os.environ.get("TELEGRAM_API_KEY")
    new_bot = telepot.Bot(TOKEN)
    return new_bot


def connect_db():
    """
    Connects to the database

    Returns:
        a connection to the database
    """
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
