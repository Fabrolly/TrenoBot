import telepot
import messageParser
from emoji import emojize

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

    response, keyboard = messageParser.messageParser(message, chatId, msg, isKeyboard)

    if response != None and len(response) > 0:
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


# TOKEN = loginInfo.telegramKey()
with open('token.txt', 'r') as content_file:
        TOKEN = content_file.read()

bot = telepot.Bot(TOKEN)
bot.message_loop({"chat": on_chat_message, "callback_query": keyboardParser})

print("Listening ...")

import time

while 1:
    time.sleep(5)
