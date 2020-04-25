# This class initialize the database and the necessary tables
# For more information about DB see: /Documentation/Infrastructure and technologies.md
from crontab import CronTab
from .bot_utility import connect_db
from .telegram import *


def main():
    # Connecting to database as root
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor()

    # Print all the databases in the system (for debug purpose only, can be removed)
    cursor.execute("show databases;")
    print("\nEXISTING DATABASE:")
    for databases in cursor:
        print(databases[0])

    # If the TRENOBOT database doses not exist, create and open it (if already exist a warning will be generated)
    cursor.execute("CREATE DATABASE IF NOT EXISTS TRENOBOT;")
    cursor.execute("use TRENOBOT;")

    # If tables doses not exist, create it (if already exist a warning will be generated)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS trains (id TEXT, number INT PRIMARY KEY, origin TEXT, destination TEXT, departure_datetime DATETIME, arrival_datetime DATETIME, duration TEXT, delay INT, state TEXT, last_detection_time TEXT, last_detection_station TEXT, stations JSON, alert TEXT, last_update DATETIME NOT NULL)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT, registration_date DATETIME)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS user_train (user_id INT, train_id TEXT, train_number INT, days TEXT, departure_datetime DATETIME, arrival_datetime DATETIME, origin TEXT, destination TEXT, last_alert TEXT, created_at DATETIME, PRIMARY KEY(user_id, train_id(10), train_number))"
    )
    cursor.execute("DROP TABLE IF EXISTS directress_alerts;")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS directress_alerts (id INT PRIMARY KEY, name TEXT, trenord_link TEXT, last_alert_text TEXT, last_update_datetime DATETIME)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS user_directress_alert (user_id INT, directress_id INT, last_alert_text TEXT, last_alert_datetime DATETIME, created_datetime DATETIME, PRIMARY KEY(user_id, directress_id))"
    )
    cursor.execute("show tables;")
    print("\nTRENOBOT - TABLES:")
    for table in cursor:
        print(table[0])

    cont = 0
    with open("./trenordLinkAlerts.txt") as f:
        content = f.readlines()
        for lines in content:
            cont = cont + 1
            # jump these lines
            if cont == 38 or cont == 41:
                cont = cont + 1
            elif cont == 43:
                cont = 50
            assert cont <= 50
            args = lines.split(" ")
            cursor.execute(
                "INSERT IGNORE INTO directress_alerts (id, name, trenord_link) VALUES (%s, '%s', '%s');"
                % (cont, args[0], args[1])
            )  # Use REPLACE instead of INSERT for update old records if exists, TODO: remove warning from terminal

    database.commit()
    f.close()

    # Disconnecting
    database.close()

    run()


##THIS IS TO RUN 1 TIME ONLY. REMOVE COMMENTS, EXECUTE starter.py AND RE-ADD COMMENTS

# my_cron = CronTab(user='fabrolly')
# job = my_cron.new(command='python /home/fabrolly/TrenoBot/Application/scheduledChecker.py')
# job.minute.every(2)
# my_cron.write()

# job = my_cron.new(command='python /home/fabrolly/TrenoBot/Application/trenordAlertChecker.py')
# job.minute.every(8)
# my_cron.write()


if __name__ == "__main__":
    main()
