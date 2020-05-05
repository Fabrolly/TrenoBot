from .databaseController import *
from .trip_search import *
from .buttons import *

# import databaseController
# import trip_search
# import buttons
from dateutil import parser
import MySQLdb
from .bot_utility import connect_db

# import loginInfo


def realTimeInfo(number):

    requestedTrain = createTrain(number)
    try:
        if "Error" in requestedTrain:
            return (requestedTrain, "")
    except:
        pass

    return (requestedTrain.realTimeMsg(), RealTimeButtons(number))


def programInfoFromSearch(
    chatId, number, days, departure_datetime, arrival_datetime, origin, destination
):

    requestedTrain = createTrain(number)
    try:
        if "Error" in requestedTrain:
            return (requestedTrain, "")
    except:
        pass

    departure_datetime = parser.parse(departure_datetime)
    arrival_datetime = parser.parse(arrival_datetime)

    origin = origin.upper()
    destination = destination.upper()

    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("USE TRENOBOT;")
        cursor.execute(
            "INSERT INTO user_train (user_id, train_id, train_number, days, departure_datetime, arrival_datetime, origin, destination, created_at) VALUES (%s, '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s');"
            % (
                chatId,
                requestedTrain.id,
                requestedTrain.number,
                days,
                departure_datetime,
                arrival_datetime,
                origin,
                destination,
                now,
            )
        )  # Use REPLACE instead of INSERT for update old records if exists
        database.commit()
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])

        if "Duplicate" in error:
            return (
                ":bell: Questo treno e' gia' nella tua lista.\n\nSe vuoi modificarlo, <b>rimuovilo</b> dalla tua lista e <b>raggiungilo</b>",
                removeButtons(),
            )
        else:
            return (error, "")

        database.close()

    return (
        ":white_check_mark: Riceverai aggiornamenti sul\n\n<b>Treno %s</b>\n%s -> %s\n%s:%s -> %s:%s\n\nNei giorni: <i>%s</i>"
        % (
            requestedTrain.number,
            origin,
            destination,
            departure_datetime.hour,
            departure_datetime.minute,
            arrival_datetime.hour,
            arrival_datetime.minute,
            daysParser(days),
        ),
        removeButtons(),
    )  # TODO: sistemare questa conferma


def programInfo(number, chatId, days, departure, arrival):

    requestedTrain = createTrain(number)
    try:
        if "Error" in requestedTrain:
            return (requestedTrain, "")
    except:
        pass

    if (
        departure == "" and arrival == ""
    ):  # if are none, I use the whole route from the train object
        departure_datetime = requestedTrain.departure_datetime
        origin = requestedTrain.origin

        arrival_datetime = requestedTrain.arrival_datetime
        destination = requestedTrain.destination

    else:
        departure_datetime, origin = requestedTrain.station_time(departure)
        arrival_datetime, destination = requestedTrain.station_time(arrival)

    if "Error" in str(departure_datetime):
        return ("ERRORE\nStazione di partenza NON esistente per questo treno", "")
    if "Error" in str(arrival_datetime):
        return ("ERRORE\nStazione di arrivo NON esistente per questo treno", "")
    if arrival_datetime < departure_datetime:
        return (
            "ERRORE\nLa stazione di arrivo deve essere successiva a quella di partenza",
            "",
        )

    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("USE TRENOBOT;")
        cursor.execute(
            "INSERT INTO user_train (user_id, train_id, train_number, days, departure_datetime, arrival_datetime, origin, destination, last_alert, created_at) VALUES (%s, '%s', %s, '%s', '%s', '%s', '%s', '%s', 'regolare','%s');"
            % (
                chatId,
                requestedTrain.id,
                requestedTrain.number,
                days,
                departure_datetime,
                arrival_datetime,
                origin,
                destination,
                now,
            )
        )  # Use REPLACE instead of INSERT for update old records if exists
        database.commit()
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])

        if "Duplicate" in error:
            return (
                ":bell: Questo treno e' gia' nella tua lista.\n\nSe vuoi modificarlo, <b>rimuovilo</b> dalla tua lista e <b>raggiungilo</b>",
                removeButtons(),
            )
        else:
            return (error, "")

        database.close()
    return (
        ":white_check_mark: Riceverai aggiornamenti sul\n\n<b>Treno %s</b>\n%s -> %s\n%s:%s -> %s:%s\n\nNei giorni: <i>%s</i>"
        % (
            requestedTrain.number,
            origin,
            destination,
            departure_datetime.hour,
            departure_datetime.minute,
            arrival_datetime.hour,
            arrival_datetime.minute,
            daysParser(days),
        ),
        removeButtons(),
    )  # TODO: sistemare questa conferma


def showList(user_id):

    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)

    try:
        cursor.execute("USE TRENOBOT;")
        row = cursor.execute(
            "SELECT * FROM user_train WHERE user_id=%s" % (user_id)
        )  # Use REPLACE instead of INSERT for update old records if exists
        dbLine = cursor.fetchall()
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        return error

    database.close()
    if row > 0:
        response = [":arrow_double_down: Ecco la tua lista :arrow_double_down:"]
        listButton = [""]
        c = 0
        for item in dbLine:
            c = c + 1
            response.append(
                "<b>%d)</b> :bullettrain_front: <b>Treno %s</b>      :clock3: %s:%s :arrow_right: %s:%s\n\n%s :arrow_right: %s\n<b>Giorni:</b> <i>%s</i>"
                % (
                    c,
                    item["train_number"],
                    item["departure_datetime"].hour,
                    item["departure_datetime"].minute,
                    item["arrival_datetime"].hour,
                    item["arrival_datetime"].minute,
                    item["origin"],
                    item["destination"],
                    daysParser(item["days"]),
                )
            )
            listButton.append(listButtons(item["train_number"]))
    else:
        return (
            "<b>Non hai alcun Treno nella tua /lista </b> :pensive:",
            backMainMenuButtons(),
        )

    return (response, listButton)


def showListDirec(user_id):
    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("USE TRENOBOT;")
        row = cursor.execute(
            "SELECT * FROM user_directress_alert WHERE user_id=%s" % (user_id)
        )  # Use REPLACE instead of INSERT for update old records if exists
        dbLine = cursor.fetchall()
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        return error

    if row > 0:
        response = ":arrow_double_down: Ecco le tue direttrici :arrow_double_down:"
        c = 0
        for item in dbLine:
            c = c + 1
            cursor.execute(
                "SELECT * FROM directress_alerts WHERE id=%s" % (item["directress_id"])
            )  # Use REPLACE instead of INSERT for update old records if exists
            dbDicLine = cursor.fetchone()
            response += (
                "\n\n:bullettrain_front: <b>Direttrice %s</b>\n<i>%s</i>\nRimuovi: /rdir%s"
                % (item["directress_id"], dbDicLine["name"], item["directress_id"])
            )
    else:
        return (
            "<b>Non hai alcuna Direttrice monitorata</b> :pensive:",
            backMainMenuButtons(),
        )

    database.close()
    return (response, backMainMenuButtons())


def daysParser(days):
    parsed = ""

    if "1" in days:
        parsed += "Lunedi "
    if "2" in days:
        parsed += "Martedi "
    if "3" in days:
        parsed += "Mercoledi "
    if "4" in days:
        parsed += "Giovedi "
    if "5" in days:
        parsed += "Venerdi "
    if "6" in days:
        parsed += "Sabato "
    if "7" in days:
        parsed += "Domenica"

    return parsed


def removeDir(dirNumber, userId):

    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("USE TRENOBOT;")
        row = cursor.execute(
            "DELETE FROM user_directress_alert WHERE directress_id=%s AND user_id=%s"
            % (dirNumber, userId)
        )  # Use REPLACE instead of INSERT for update old records if exists
        database.commit()
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        return error

    database.close()

    if row == 0:
        return (
            "La direttrice %s <b>non e' monitorata </b>:flushed: " % (dirNumber),
            removeDirButtons(),
        )
    else:
        return (
            "Direttrice %s <b>rimossa</b>:innocent: " % (dirNumber),
            removeDirButtons(),
        )


def remove(trainNumber, userId):

    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("USE TRENOBOT;")
        row = cursor.execute(
            "DELETE FROM user_train WHERE train_number=%s AND user_id=%s"
            % (trainNumber, userId)
        )  # Use REPLACE instead of INSERT for update old records if exists
        database.commit()
        print(row)
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        return error

    database.close()

    if row == 0:
        return (
            "Nella tua /lista <b>non esiste</b> il Treno %s :flushed: " % (trainNumber),
            removeButtons(),
        )
    else:
        return (
            "Treno %s <b>rimosso</b> dalla tua /lista :innocent: " % (trainNumber),
            removeButtons(),
        )


def addDire(number, chatId):

    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("USE TRENOBOT;")
        cursor.execute(
            "INSERT INTO user_directress_alert (user_id, directress_id, created_datetime) VALUES (%s, %s, '%s');"
            % (chatId, number, now)
        )  # Use REPLACE instead of INSERT for update old records if exists
        database.commit()
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])

        if "Duplicate" in error:
            return (
                ":bell: Questa direttrice e' gia' monitorata.",
                removeDirButtons(),
            )
        else:
            return (error, "")

        database.close()

    return (
        ":white_check_mark: <b>Riceverai aggiornamenti sulla direttrice selezionata non appena ci saranno novita'!</b>",
        removeDirButtons(),
    )  # TODO: sistemare questa conferma


def summary(chatId):

    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    response = "<b>Riepilogo del tuo account</b>\n\n"

    try:
        cursor.execute("USE TRENOBOT;")
        row = cursor.execute(
            "SELECT * FROM user_train WHERE user_id=%s" % (chatId)
        )  # Use REPLACE instead of INSERT for update old records if exists
        dbLine = cursor.fetchall()
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        print(error)
        return error

    if row > 0:
        response += ":arrow_double_down: I tuoi treni programmati :arrow_double_down:\n"
        c = 0
        for item in dbLine:
            c = c + 1
            response += (
                "\n<b>%d)</b> :bullettrain_front: <b>Treno %s</b> %s:%s :arrow_right: %s:%s\n      %s :arrow_right: %s\n      <i>%s</i>"
                % (
                    c,
                    item["train_number"],
                    item["departure_datetime"].hour,
                    item["departure_datetime"].minute,
                    item["arrival_datetime"].hour,
                    item["arrival_datetime"].minute,
                    item["origin"],
                    item["destination"],
                    daysParser(item["days"]),
                )
            )
    else:
        response += "\n\n<b>Non hai alcun Treno nella tua /lista </b> :pensive:"

    try:
        cursor.execute("USE TRENOBOT;")
        row = cursor.execute(
            "SELECT * FROM user_directress_alert WHERE user_id=%s" % (chatId)
        )  # Use REPLACE instead of INSERT for update old records if exists
        dbLine = cursor.fetchall()
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        print(error)
        return error

    response += "\n\n---------------------\n\n"

    if row > 0:
        response += (
            ":arrow_double_down: Le tue direttrici monitorate :arrow_double_down:\n"
        )
        c = 0
        for item in dbLine:
            c = c + 1
            cursor.execute(
                "SELECT * FROM directress_alerts WHERE id=%s" % (item["directress_id"])
            )  # Use REPLACE instead of INSERT for update old records if exists
            dbDicLine = cursor.fetchone()
            response += (
                "\n:bullettrain_front: <b>Direttrice %s</b>\n      <i>%s</i>"
                % (item["directress_id"], dbDicLine["name"])
            )
    else:
        response += "\n\n<b>Non hai alcuna Direttrice monitorata</b> :pensive:"

    response += "\n\n\n<i>Per aggiungere, rimuovere o modificare la tua lista usa i pulsanti qui sotto</i>"

    database.close

    return (response, summaryButtons())
