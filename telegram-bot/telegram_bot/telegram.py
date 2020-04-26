"""
This module contains general handlers for setting up and running the bot
"""
import telepot
import time
from .messageParser import *

# import messageParser
from emoji import emojize
from .bot_utility import create_bot

# import loginInfo


def keyboardParser(msg):
    query_id, chatId, command = telepot.glance(msg, flavor="callback_query")

    command += ".chatId%s" % (chatId)
    on_chat_message(command)


def on_chat_message(msg):
    """
    Handle an incoming message
    Args:
        message: the incoming message
    """
    if isinstance(msg, str) and ".chatId" in msg:
        message = msg[: msg.index(".")].lower()
        chatId = msg[msg.index(".chatId") + 7 :]
        isKeyboard = True
    else:
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == "text":
            message = msg["text"].lower()
            chatId = msg["chat"]["id"]
            isKeyboard = False
        else:
            return

    response, keyboard = messageParser(message, chatId, msg, isKeyboard)

    if response is not None and len(response) > 0:
        if isinstance(response, str):
            if response is not None:
                if keyboard is not None:
                    bot.sendMessage(
                        chatId,
                        emojize(response, use_aliases=True),
                        parse_mode="html",
                        disable_web_page_preview=None,
                        disable_notification=None,
                        reply_markup=keyboard,
                    )
                else:
                    bot.sendMessage(
                        chatId,
                        emojize(response, use_aliases=True),
                        parse_mode="html",
                        disable_web_page_preview=None,
                        disable_notification=None,
                    )
            else:
                print("messaggio non valido")
        else:
            for item, key in zip(response, keyboard):
                if response is not None:
                    if isinstance(item, tuple):  # caso menu direttrice
                        if item[1] == "url":
                            bot.sendPhoto(chatId, item[0])
                    else:
                        bot.sendMessage(
                            chatId,
                            emojize(item, use_aliases=True),
                            parse_mode="html",
                            disable_web_page_preview=None,
                            disable_notification=None,
                            reply_markup=key,
                        )
                else:
                    print("messaggio non valido")


def sendMessageKeyboard(chatId, msg, keyboard):
    """
    Send an inline keyboard

    Params:
        chatId: where to send the message
        msg: the text
        keyboard: the inline keyboard instance to send
    """
    bot.sendMessage(
        chatId,
        emojize(msg, use_aliases=True),
        parse_mode="html",
        disable_web_page_preview=None,
        disable_notification=None,
        reply_markup=keyboard,
    )


def run():
    """
    Run the bot
    """
    bot = create_bot()
    bot.message_loop({"chat": on_chat_message, "callback_query": keyboardParser})

    print("Listening ...")

    while 1:
        time.sleep(5)
