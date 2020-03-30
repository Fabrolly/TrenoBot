# -*- coding: utf-8 -*-

import messageResponder
import usersController
import re
import datetime
import time
import trip_search
import menuMessages
import adminFunctions

# import loginInfo


def messageParser(msg, chatId, msgComplete, isKeybboard):

    # print(msg, chatId, msgComplete, isKeybboard)
    if not isKeybboard:
        added = usersController.addUserIfNotExist(msgComplete)
        # print(added)
        if "Error" in added:
            return added

    if "/start" in msg:
        response = menuMessages.mainMenu()
        return response

    if "/rdir" in msg:
        response = removeDirRapidCommand(chatId, msg)
        return response

    if "menu direttrice" in msg:
        response = menuMessages.directressAddMenu()
        return response

    if "menu principale" in msg:
        response = menuMessages.mainMenu()
        return response

    if "menu treno" in msg:
        response = menuMessages.realTimeMenu()
        return response

    if "lista direttrici" in msg:
        response = messageResponder.showListDirec(chatId)
        return response

    if "rimuovi direttrice" in msg:
        response = removeDirParser(chatId, msg)
        return response

    if "menu ricerca" in msg:
        response = menuMessages.searchMenu()
        return response

    if "menu gprogrammazione" in msg:
        response = menuMessages.programMenu()
        return response

    if "menu programma" in msg:
        response = menuMessages.addListMenu()
        return response

    if "treno" in msg or msg.isdigit():
        response = realTimeParser(msg, chatId)
        return response

    if "programma" in msg:
        response = programParser(msg, chatId)
        return response

    if "rieplilogo" in msg:
        response = messageResponder.summary(chatId)
        return response

    if "direttrice" in msg:
        response = direParser(msg, chatId)
        return response

    if "ricerca" in msg:
        response = trip_search_parser(msg, chatId)
        return response

    if "lista" in msg:
        response = messageResponder.showList(chatId)
        return response

    if "rimuovi" in msg:
        response = removeParser(msg, chatId)
        return response

    if "pk" in msg:
        msg = msg[msg.index("pk") + 3 :]
        msg = msg.split("!")
        response = messageResponder.programInfoFromSearch(chatId, *msg)
        return response

    # ----admin functions

    if chatId == int(loginInfo.adminTelegramId()):
        if "/stats" in msg:
            return adminFunctions.systemStats()
        if "/broadcast" in msg:
            msg = msg[11:]
            if msg != "":
                return adminFunctions.broadcast(msg)

    return ("Sintassi comando non valida\nRiprova :interrobang:", ())


def realTimeParser(msg, chatId):
    message = msg
    numbers = re.findall("\d+", message)
    return messageResponder.realTimeInfo(numbers[0])

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

    return messageResponder.programInfo(numbers[0], chatId, days, departure, arrival)


def trip_search_parser(command, chatId):

    now = datetime.datetime.now()

    if " da " not in command and " a " not in command:
        partenza = command[command.index(" ") + 1 :]
        partenza = partenza[: partenza.index(" ")]

        if " il " not in command and " alle " not in command:
            arrivo = command[command.index(" ") + 1 :]
            arrivo = arrivo[arrivo.index(" ") + 1 :]
            data = trip_search.date_parser("")
            ora = "%s:%s" % (now.hour, now.minute)
        if " il " not in command and " alle " in command:
            arrivo = command[command.index(" ") + 1 :]
            arrivo = arrivo[arrivo.index(" ") + 1 :]
            arrivo = arrivo[: arrivo.index(" ") :]
            data = trip_search.date_parser("")
            ora = command[command.index(" alle ") + 6 :]
        if " il " in command and " alle " in command:
            arrivo = command[command.index(" ") + 1 :]
            arrivo = arrivo[arrivo.index(" ") + 1 :]
            arrivo = arrivo[: arrivo.index(" ") :]
            data = trip_search.date_parser(
                command[command.index(" il ") + 4 : command.index(" alle ")]
            )
            ora = command[command.index(" alle ") + 6 :]
        if " il " in command and " alle " not in command:
            arrivo = command[command.index(" ") + 1 :]
            arrivo = arrivo[arrivo.index(" ") + 1 :]
            arrivo = arrivo[: arrivo.index(" ")]
            data = trip_search.date_parser(command[command.index(" il ") + 4 :])
            ora = "%s:%s" % (now.hour, now.minute)
    else:
        partenza = command[command.index(" da ") + 4 : command.index(" a ")]
        if " il " not in command and " alle " not in command:
            arrivo = command[command.index(" a ") + 3 :]
            data = trip_search.date_parser("")
            ora = "%s:%s" % (now.hour, now.minute)
        if " il " not in command and " alle " in command:
            arrivo = command[command.index(" a ") + 3 : command.index(" alle ")]
            data = trip_search.date_parser("")
            ora = command[command.index(" alle ") + 6 :]
        if " il " in command and " alle " in command:
            arrivo = command[command.index(" a ") + 3 : command.index(" il ")]
            data = trip_search.date_parser(
                command[command.index(" il ") + 4 : command.index(" alle ")]
            )
            ora = command[command.index(" alle ") + 6 :]
        if " il " in command and " alle " not in command:
            arrivo = command[command.index(" a ") + 3 : command.index(" il ")]
            data = trip_search.date_parser(command[command.index(" il ") + 4 :])
            ora = "%s:%s" % (now.hour, now.minute)

    # Sostituisco spazi con _
    arrivo = arrivo.replace(" ", "_")
    partenza = partenza.replace(" ", "_")

    mese = data[data.index("-") + 1 :]
    giorno = data[: data.index("-")]

    print("\n\n")
    print(partenza)
    print("\n")
    print(arrivo)
    print("\n")
    print(mese)
    print("\n")
    print(giorno)

    trip_search.trip_search(
        command, arrivo, partenza, mese, giorno, ora, data, now, chatId
    )

    return ("", "")


def removeParser(msg, chatId):
    message = msg
    numbers = re.findall("\d+", message)
    return messageResponder.remove(numbers[0], chatId)


def removeDirRapidCommand(chatId, message):
    numbers = re.findall("\d+", message)
    msg = "rimuovi %s" % (numbers)
    return removeDirParser(chatId, msg)


def removeDirParser(chatId, msg):
    message = msg
    numbers = re.findall("\d+", message)
    return messageResponder.removeDir(numbers[0], chatId)


def direParser(msg, chatId):
    message = msg
    numbers = re.findall("\d+", message)
    return messageResponder.addDire(numbers[0], chatId)
