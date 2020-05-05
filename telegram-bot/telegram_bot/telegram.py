import telepot
from .messageParser import *
from .trenordAlertChecker import main as trenord_alert_check
from .scheduledChecker import main as scheduled_train_check

# import messageParser
from emoji import emojize
from .bot_utility import create_bot

import time
import os
import threading

# import loginInfo


def keyboardParser(msg):
    query_id, chatId, command = telepot.glance(msg, flavor="callback_query")

    command += ".chatId%s" % (chatId)
    on_chat_message(command)


def on_chat_message(msg):

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
    bot.sendMessage(
        chatId,
        emojize(msg, use_aliases=True),
        parse_mode="html",
        disable_web_page_preview=None,
        disable_notification=None,
        reply_markup=keyboard,
    )


def check_users_train_loop():
    while True:
        print("Controllo automatico treni utente programmati")
        scheduled_train_check()
        print("Prossimo controllo treni in partenza tra 2 minuti")
        time.sleep(2 * 60)  # sleep 2 minutes


def check_users_trenord_alert_loop():
    while True:
        print("Controllo automatico direttrici utente monitorate")
        trenord_alert_check()
        print("Prossimo controllo direttrici tra 10 minuti")
        time.sleep(10 * 60)  # sleep 10 minutes


def main():
    bot = create_bot()
    bot.message_loop({"chat": on_chat_message, "callback_query": keyboardParser})

    x = threading.Thread(target=check_users_train_loop)
    x.start()

    y = threading.Thread(target=check_users_trenord_alert_loop)
    y.start()

    print("Listening ...")

    while 1:
        time.sleep(5)


if __name__ == "__main__":
    main()
