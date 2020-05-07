"""
This module contains functions to parse messages and act according to their content

"""

from .messageResponder import *
from .usersController import *
from .trip_search import *
from .menuMessages import *
from .adminFunctions import *
from .statistics_interface import *

# import messageResponder
# import usersController
import re
import datetime
import time
import os

# import trip_search
# import menuMessages
# import adminFunctions

ADMIN_IDS = os.environ.get("ADMINS", "").split(",")


def messageParser(msg, chatId, msgComplete, isKeybboard):
    """
    Generate response based on the message content
    Params:
        msg: the message text to parse
        chatId: the chat where the message come from
        msgComplete: the complete message instance
        isKeybboard: if the message comes from a inline keyboard reply
    Returns:
        the response to send

    """

    # print(msg, chatId, msgComplete, isKeybboard)
    if not isKeybboard:
        added = addUserIfNotExist(msgComplete)
        # print(added)
        if "Error" in added:
            return added

    if "/start" in msg:
        response = mainMenu()
        return response

    if "/rdir" in msg:
        response = removeDirRapidCommand(chatId, msg)
        return response

    if "menu direttrice" in msg:
        send_msg, send_buttons = directressAddMenu()
        send_msg = [("https://imgur.com/a/wIfQbz2", "url"), send_msg]
        send_buttons = ["", send_buttons]
        return (send_msg, send_buttons)

    if "menu principale" in msg:
        response = mainMenu()
        return response

    if "menu treno" in msg:
        response = realTimeMenu()
        return response

    if "menu statistiche" in msg:
        ranking_readable = train_ranking_readable()
        response = statsMenu(ranking_readable)
        return response

    if "lista direttrici" in msg:
        response = showListDirec(chatId)
        return response

    if "rimuovi direttrice" in msg:
        response = removeDirParser(chatId, msg)
        return response

    if "menu ricerca" in msg:
        response = searchMenu()
        return response

    if "treno" in msg or msg.isdigit():
        response = realTimeParser(msg, chatId)
        return response

    if "programma" in msg:
        if "menu programmazione" in msg:
            response = programMenu()
        elif "menu programma" in msg:
            response = addListMenu()
        else:
            response = programParser(msg, chatId)
        return response

    if "riepilogo" in msg:
        response = summary(chatId)
        return response

    if "direttrice" in msg:
        response = direParser(msg, chatId)
        return response

    if "ricerca" in msg:
        response = trip_search_parser(msg, chatId)
        return response

    if "lista" in msg:
        response = showList(chatId)
        return response

    if "rimuovi" in msg:
        response = removeParser(msg, chatId)
        return response

    if "statistiche" in msg:
        print("Statistiche")
        response = statsParser(msg, chatId)
        return response

    if "pk" in msg:
        msg = msg[msg.index("pk") + 3 :]
        msg = msg.split("!")
        response = programInfoFromSearch(chatId, *msg)
        return response

    # ----admin functions
    if str(chatId) in ADMIN_IDS:
        if "/stats" in msg:
            return systemStats()
        if "/broadcast" in msg:
            msg = msg[11:]
            if msg != "":
                return broadcast(msg)

    return ("Sintassi comando non valida:interrobang:\nRiprova ", None)


def realTimeParser(msg, chatId):
    message = msg
    numbers = re.findall("\d+", message)
    return realTimeInfo(numbers[0])


def programParser(msg, chatId):
    numbers = re.findall("\d+", msg)

    msg = msg.replace("ì", "i")

    days = ""  # 1=Monday, 2=Tuseday...

    if "lunedi" in msg:
        days += "1"
    if "martedi" in msg:
        days += "2"
    if "mercoledi" in msg:
        days += "3"
    if "giovedi" in msg:
        days += "4"
    if "venerdi" in msg:
        days += "5"
    if "sabato" in msg:
        days += "6"
    if "domenica" in msg:
        days += "7"

    if days == "":
        days = "12345"

    command = msg

    departure = ""
    arrival = ""
    if " a " in command and " da " in command:
        departure = command[command.index(" da ") + 4 : command.index(" a ")]
        arrival = command[command.index(" a ") + 3 :]

    return programInfo(numbers[0], chatId, days, departure, arrival)


def trip_search_parser(command, chatId):
    """
    Handle the search for a trip

    """
    now = datetime.datetime.now()

    if " da " not in command and " a " not in command:
        partenza = command[command.index(" ") + 1 :]
        partenza = partenza[: partenza.index(" ")]

        if " il " not in command and " alle " not in command:
            arrivo = command[command.index(" ") + 1 :]
            arrivo = arrivo[arrivo.index(" ") + 1 :]
            data = date_parser("")
            ora = "%s:%s" % (now.hour, now.minute)
        if " il " not in command and " alle " in command:
            arrivo = command[command.index(" ") + 1 :]
            arrivo = arrivo[arrivo.index(" ") + 1 :]
            arrivo = arrivo[: arrivo.index(" ") :]
            data = date_parser("")
            ora = command[command.index(" alle ") + 6 :]
        if " il " in command and " alle " in command:
            arrivo = command[command.index(" ") + 1 :]
            arrivo = arrivo[arrivo.index(" ") + 1 :]
            arrivo = arrivo[: arrivo.index(" ") :]
            if command.index(" il ") <= command.index(" alle "):
                data = date_parser(
                    command[command.index(" il ") + 4 : command.index(" alle ")]
                )
                ora = command[command.index(" alle ") + 6 :]
            else:
                data = date_parser(command[command.index(" il ") + 4 :])
                ora = command[command.index(" alle ") + 6 : command.index(" il ")]
        if " il " in command and " alle " not in command:
            arrivo = command[command.index(" ") + 1 :]
            arrivo = arrivo[arrivo.index(" ") + 1 :]
            arrivo = arrivo[: arrivo.index(" ")]
            data = date_parser(command[command.index(" il ") + 4 :])
            ora = "%s:%s" % (now.hour, now.minute)
    elif " da " in command and " a " in command:
        partenza = command[command.index(" da ") + 4 : command.index(" a ")]
        if " il " not in command and " alle " not in command:
            arrivo = command[command.index(" a ") + 3 :]
            data = date_parser("")
            ora = "%s:%s" % (now.hour, now.minute)
        if " il " not in command and " alle " in command:
            arrivo = command[command.index(" a ") + 3 : command.index(" alle ")]
            data = date_parser("")
            ora = command[command.index(" alle ") + 6 :]
        if " il " in command and " alle " in command:
            if command.index(" il ") <= command.index(" alle "):
                arrivo = command[command.index(" a ") + 3 : command.index(" il ")]
                ora = command[command.index(" alle ") + 6 :]
                data = date_parser(
                    command[command.index(" il ") + 4 : command.index(" alle ")]
                )
            else:
                arrivo = command[command.index(" a ") + 3 : command.index(" alle ")]
                ora = command[command.index(" alle ") + 6 : command.index(" il ")]
                data = date_parser(command[command.index(" il ") + 4 :])
        if " il " in command and " alle " not in command:
            arrivo = command[command.index(" a ") + 3 : command.index(" il ")]
            data = date_parser(command[command.index(" il ") + 4 :])
            ora = "%s:%s" % (now.hour, now.minute)

    try:
        datetime.datetime(
            year=now.year,
            month=int(data[(data.index("-") + 1) :]),
            day=int(data[: data.index("-")]),
            hour=int(ora[: ora.index(":")]),
            minute=int(ora[(ora.index(":") + 1) :]),
        )
    except ValueError:
        return (
            u"Attenzione, l'ora o la data inserita è <b>errata</b>.\n\nInput ricevuto = %s-%s %s\nLa preghiamo di riprovare. :pensive:"
            % (data, now.year, ora),
            "",
        )

    # Sostituisco spazi con _
    arrivo = arrivo.replace(" ", "_")
    partenza = partenza.replace(" ", "_")

    mese = data[data.index("-") + 1 :]
    giorno = data[: data.index("-")]

    if ":" not in ora:
        ora += str(":00")

    trip_response = trip_search(
        command, arrivo, partenza, mese, giorno, ora, data, now, chatId
    )

    return trip_response


def removeParser(msg, chatId):
    message = msg
    numbers = re.findall("\d+", message)
    return remove(numbers[0], chatId)


def removeDirRapidCommand(chatId, message):
    numbers = re.findall("\d+", message)
    msg = "rimuovi %s" % (numbers)
    return removeDirParser(chatId, msg)


def removeDirParser(chatId, msg):
    message = msg
    numbers = re.findall("\d+", message)
    return removeDir(numbers[0], chatId)


def direParser(msg, chatId):
    message = msg
    numbers = re.findall("\-?\d+", message)
    exluded_index = [38, 41] + list(range(43, 50))
    num_direttrici = [x for x in range(1, 51) if x not in exluded_index]
    if int(numbers[0]) not in num_direttrici:
        return ("Error: direttrice <b>non valida!</b> :pensive:", "")
    return addDire(int(numbers[0]), chatId)


def statsParser(msg: str, chatId: int) -> tuple:
    """
    Function to extract from the input message the train code and to call the viewStatistic function.

    Args:
        msg: input message.
        chatId: id of the user who is writing to the bot.

    Returns:
       A message containing some interesting train statistic..

    """
    message = msg
    numbers = re.findall("\d+", message)
    if not numbers:
        return (
            "Errore! Inserire il codice del treno per vederne le statistiche! :pensive:\n",
            "",
        )
    return viewStatistics(int(numbers[0]))
