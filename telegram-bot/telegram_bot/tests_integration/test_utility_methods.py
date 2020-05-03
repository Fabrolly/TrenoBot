import warnings
import random
import io
import sys
import re
from telepot.namedtuple import *
from telegram_bot.messageParser import messageParser as mp
from telegram_bot.messageResponder import remove

# from .messageParser import messageParser as mp
# from messageResponder import remove


# USER_ID = random.randint(10000000, 99999999)
USER_ID = 95054305

from telegram_bot.bot import create_db

create_db()


def create_message(text):
    msg_id = random.randint(1000, 9999)
    assert (len(str(msg_id))) == 4
    assert (len(str(USER_ID))) == 8
    msg = {
        "message_id": msg_id,
        "from": {
            "id": USER_ID,
            "is_bot": False,
            "first_name": "Simone",
            "last_name": "Vitali",
            "username": "SimoVita",
            "language_code": "it",
        },
        "chat": {
            "id": USER_ID,
            "first_name": "Simone",
            "last_name": "Vitali",
            "username": "SimoVita",
            "type": "private",
        },
        "date": 1585416801,
        "text": text,
    }
    return msg, msg["text"].lower(), msg["from"]["id"]


def call_mute_mp(text_msg):
    # disable warning
    warnings.filterwarnings("ignore")
    # create a text trap and redirect stdout
    text_trap = io.StringIO()
    sys.stdout = text_trap

    # execute our now mute function
    msg, message, id = create_message(text_msg)
    mp_object = mp(
        message, id, msg, False
    )  # Tested with only 'isKeybbord' param set to False
    # now restore stdout function
    sys.stdout = sys.__stdout__
    return mp_object


def call_mute_remove_train(train_code):
    warnings.filterwarnings("ignore")
    text_trap = io.StringIO()
    sys.stdout = text_trap
    remove(train_code, USER_ID)
    sys.stdout = sys.__stdout__


def text_in_msg(text, str_in_msg=[]):
    cond = isinstance(text, str)
    for string in str_in_msg:
        cond = cond and (string in text)
    return cond


def text_in_buttons(buttons, str_in_button=[], ignore_codes=False):
    if isinstance(buttons, InlineKeyboardMarkup):
        buttons = [buttons]
    cond = isinstance(buttons, list)
    for button_obj in buttons:
        cond = cond and isinstance(button_obj, InlineKeyboardMarkup)
        cond = cond and isinstance(button_obj.inline_keyboard, list)
        for button in button_obj.inline_keyboard:
            cond = cond and isinstance(button, list)
            cond = cond and isinstance(button[0], InlineKeyboardButton)
            cond = cond and isinstance(button[0].text, str)
            if ignore_codes:
                if re.search(r"\s\d{4}\s", button[0].text):
                    cond = cond and all(
                        i[0] == i[1]
                        for i in zip(button[0].text, " ".join(str_in_button))
                        if not i[0].isdigit()
                    )
            else:
                cond = cond and (button[0].text in str_in_button)
    return cond


def is_menu_principale(text, buttons):
    menu = isinstance(text, str)
    text_key_word = [
        "Menu' Principale",
        "Scegli l'operazione che desideri effettuare",
    ]
    menu = menu and text_in_msg(text, text_key_word)
    button_key_word = [
        "Treno Real Time",
        "Ricerca un Treno",
        "Menu' Treni Monitorati",
        "Menu' Direttrici Monitorate",
        "Riepilogo completo dei miei avvisi",
    ]
    menu = menu and text_in_buttons(buttons, button_key_word)
    return menu


def is_riepilogo_empty():
    response = call_mute_mp("riepilogo")
    key_word = [
        "Riepilogo del tuo account",
        "Non hai alcun Treno nella tua /lista",
        "Non hai alcuna Direttrice monitorata",
        "Per aggiungere, rimuovere o modificare la tua lista usa i pulsanti qui sotto",
    ]
    riepilogo = text_in_msg(response[0], key_word)
    riepilogo = riepilogo and text_in_buttons(
        response[1], ["Lista Treni", "Lista direttrici", "Menu' Principale"]
    )
    return riepilogo
