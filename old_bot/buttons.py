import telepot
from telepot.namedtuple import *


def removeButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Visualizza lista", callback_data="/lista")],
            [
                InlineKeyboardButton(
                    text="Torna al menu principale", callback_data="Menu Principale"
                )
            ],
        ]
    )

    return keyboard


def removeDirButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Torna al menu direttrici", callback_data="Menu Direttrice"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Le mie direttrici attive", callback_data="Lista Direttrici"
                )
            ],
        ]
    )
    return keyboard


def listButtons(trainNumber):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Stato in Real Time", callback_data="Treno %s" % (trainNumber)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Rimuovi Treno %s" % (trainNumber),
                    callback_data="Rimuovi %s" % (trainNumber),
                )
            ],
        ]
    )

    return keyboard


def listDicButtons(dire):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Rimuovi Direttrice %s" % (dire),
                    callback_data="Rimuovi Direttrice %s" % (dire),
                )
            ]
        ]
    )

    return keyboard


def RealTimeButtons(trainNumber):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Aggiorna", callback_data="Treno %s" % (trainNumber)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Aggiungi alla Lista",
                    callback_data="Programma %s" % (trainNumber),
                )
            ],
        ]
    )

    return keyboard


def backMainMenuButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Menu' principale", callback_data="Menu Principale"
                )
            ]
        ]
    )

    return keyboard


def alertMenuButtons(trainNumber):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Aggiorna", callback_data="Treno %s" % (trainNumber)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Smetti di seguire", callback_data="Rimuovi %s" % (trainNumber)
                )
            ],
        ]
    )

    return keyboard


def searchResultMenuButtons(
    chatid, trainNumber, departure_datetime, arrival_datetime, departure, arrival
):
    from messageResponder import programInfoFromSearch

    tast = []
    days = "12345"
    for train, dep_time, arr_time, dep, arr in zip(
        trainNumber, departure_datetime, arrival_datetime, departure, arrival
    ):
        dep = dep.replace(".", "")
        arr = arr.replace(".", "")
        tast.append(
            [
                InlineKeyboardButton(
                    text="Aggiungi %s alla lista" % train,
                    callback_data="pk %s!%s!%s!%s!%s!%s"
                    % (train, days, dep_time, arr_time, dep, arr),
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=tast)

    print("\n\n")
    print(keyboard)
    return keyboard


def trenordAlertButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Rimuovi avvisi", callback_data="Treno")],
            [
                InlineKeyboardButton(
                    text="Menu' Principale", callback_data="Menu Principale"
                )
            ],
        ]
    )
    return keyboard


def summaryButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Lista Treni", callback_data="/lista")],
            [
                InlineKeyboardButton(
                    text="Lista direttrici", callback_data="Lista Direttrici"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Menu' Principale", callback_data="Menu Principale"
                )
            ],
        ]
    )
    return keyboard


# ---------------------------Menu Keyboards--------------------------------


def mainMenuButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Treno Real Time", callback_data="Menu Treno")],
            [
                InlineKeyboardButton(
                    text="Ricerca un Treno", callback_data="Menu Ricerca"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Menu' Treni Monitorati", callback_data="Menu gprogrammazione"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Menu' Direttrici Monitorate", callback_data="Menu Direttrice"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Riepilogo completo dei miei avvisi",
                    callback_data="Rieplilogo",
                )
            ],
        ]
    )
    print("\n\n")
    print(keyboard)
    return keyboard


def programMenuButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Aggiungi un treno alla tua Lista",
                    callback_data="Menu Programma",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Visualizza la tua lista", callback_data="/lista"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Menu' Principale", callback_data="Menu Principale"
                )
            ],
        ]
    )
    print("\n\n")
    print(keyboard)
    return keyboard


def trainMenuButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Non conosco il numero del treno", callback_data="Menu Ricerca"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Menu' Principale", callback_data="Menu Principale"
                )
            ],
        ]
    )
    return keyboard


def searchMenuButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Menu' Principale", callback_data="Menu Principale"
                )
            ]
        ]
    )
    return keyboard


def addListButtons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Non conosco il numero del treno", callback_data="Menu Ricerca"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Visualizza la tua Lista Treni", callback_data="Lista"
                )
            ][
                InlineKeyboardButton(
                    text="Menu' Principale", callback_data="Menu Principale"
                )
            ],
        ]
    )
    return keyboard


def trenordAlertMenu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Le mie direttrici attive", callback_data="Lista Direttrici"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Menu' Principale", callback_data="Menu Principale"
                )
            ],
        ]
    )
    return keyboard
