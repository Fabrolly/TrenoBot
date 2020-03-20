import MySQLdb
import loginInfo
import telepot
from emoji import emojize

def systemStats():
    msg="<b>Statistiche</b>\n\n"
    # Connecting to database
    database = MySQLdb.connect("localhost","root", loginInfo.databasePWS())
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("USE TRENOBOT;")
        usersNumber=cursor.execute("SELECT * from users;") #Use REPLACE instead of INSERT for update old records if exists
        msg+="Utenti registrati: <b>%s</b>"%(usersNumber)
    except MySQLdb.Error as e:
        database.rollback()
        error='Got Error {!r}, errno is {}'.format(e, e.args[0])
        msg+= error

    try:
        trainsNumber=cursor.execute("SELECT * from trains;") #Use REPLACE instead of INSERT for update old records if exists
        msg+="\n\nTreni in locale: <b>%s</b>"%(trainsNumber)
    except MySQLdb.Error as e:
        database.rollback()
        error='Got Error {!r}, errno is {}'.format(e, e.args[0])
        msg+= error

    try:
        updatedTrainsNumber=cursor.execute("SELECT * from trains WHERE last_update >= CURDATE();") #Use REPLACE instead of INSERT for update old records if exists
        msg+="\nDi cui aggiornati oggi: <b>%s</b>"%(updatedTrainsNumber)
    except MySQLdb.Error as e:
        database.rollback()
        error='Got Error {!r}, errno is {}'.format(e, e.args[0])
        msg+=error

    try:
        prgNumber=cursor.execute("SELECT * from user_train;") #Use REPLACE instead of INSERT for update old records if exists
        msg+="\n\nTreni Monitorati: <b>%s</b>"%(prgNumber)
    except MySQLdb.Error as e:
        database.rollback()
        error='Got Error {!r}, errno is {}'.format(e, e.args[0])
        msg+= error
    
    try:
        fini=cursor.execute("SELECT * from user_train WHERE arrival_datetime >= CURDATE();") #Use REPLACE instead of INSERT for update old records if exists
        msg+="\nDi cui gia' a destinazione: <b>%s</b>"%(fini)
    except MySQLdb.Error as e:
        database.rollback()
        error='Got Error {!r}, errno is {}'.format(e, e.args[0])
        msg+= error

    try:
        direcNumbers=cursor.execute("SELECT * from user_directress_alert;") #Use REPLACE instead of INSERT for update old records if exists
        msg+="\n\nDirettrici monitorate da utenti: <b>%s</b>"%(direcNumbers)
    except MySQLdb.Error as e:
        database.rollback()
        error='Got Error {!r}, errno is {}'.format(e, e.args[0])
        msg+= error



    database.close()
    print msg
    return (msg, "")


def broadcast(msg):
    # Connecting to database
    database = MySQLdb.connect("localhost","root", loginInfo.databasePWS())
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    msgAdmin="<b>Messaggio mandato a:</b>\n\n"
    try:
        cursor.execute("USE TRENOBOT;")
        usersNumber=cursor.execute("SELECT id from users;") #Use REPLACE instead of INSERT for update old records if exists
        dbLines=cursor.fetchall()
    except MySQLdb.Error as e:
        database.rollback()
        error='Got Error {!r}, errno is {}'.format(e, e.args[0])
        return (error, "")
    
    TOKEN = loginInfo.telegramKey()
    bot = telepot.Bot(TOKEN)

    for row in dbLines:
        bot.sendMessage(row['id'], emojize(msg, use_aliases=True), parse_mode='html', disable_web_page_preview=None, disable_notification=None)
        print row['id']
        msgAdmin+="Mandato a %s\n" %(row['id'])

    return (msgAdmin, "")
    

