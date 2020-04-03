import sys
import os
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import datetime as dt
import unittest
import MySQLdb

from database_initialization import database_initialization as db_inizialization

server = os.environ.get("DATABASE_HOST")
user = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_PASSWORD")


def delete_database():
    database = MySQLdb.connect(server, user, password)
    cursor = database.cursor()
    cursor.execute("DROP DATABASE IF EXISTS TRENOBOT;")
    database.commit()
    database.close()


def find_statistics_db():
    cursor = cursor_database()
    cursor.execute("show databases;")
    for database in cursor:
        if database[0] == "TRENOBOT":
            return True
    return False


def execute_query(table_name):
    cursor = cursor_database()
    cursor.execute("use TRENOBOT;")
    cursor.execute(f"SELECT * FROM {table_name}")
    return list(cursor)


def cursor_database():
    database = MySQLdb.connect(server, user, password)
    return database.cursor()


# class TestMssageParser(unittest.TestCase):
class Monolithic(unittest.TestCase):
    def setUp(self):
        delete_database()

    def test_create_database(self):

        find_databases = find_statistics_db()
        self.assertFalse(find_databases)

        db_inizialization()

        find_databases = find_statistics_db()
        self.assertTrue(find_databases)

    def test_insert_data(self):

        db_inizialization()

        database = MySQLdb.connect(server, user, password)
        cursor = database.cursor()
        cursor.execute("use TRENOBOT;")

        query_result = execute_query("backend_trains")
        self.assertEqual(len(query_result), 0)
        departure_datetime = dt.datetime.strptime(
            "2020-03-31 16:08:00", "%Y-%m-%d %H:%M:%S"
        )
        arrival_datetime = dt.datetime.strptime(
            "2020-03-31 16:48:00", "%Y-%m-%d %H:%M:%S"
        )
        # stations = [{"Bergamo" : "16:08"}, {"Ponte S.Pietro" : "16:14"}, {"Cisano Caprino Berga" : "16:27"}, {"Lecco" : "16:48"}]
        stations = {}

        insert_query = f"INSERT INTO backend_trains (trainID, number, origin, destination, stations, departure_datetime, arrival_datetime, duration) VALUES (5050, 'S01529', 'Bergamo', 'Lecco', \"{stations}\", \"{departure_datetime}\", \"{arrival_datetime}\", 40);"
        cursor.execute(insert_query)
        database.commit()
        database.close()

        query_result = execute_query("backend_trains")
        self.assertEqual(len(query_result), 1)

    def test_delete_data(self):

        db_inizialization()
        database = MySQLdb.connect(server, user, password)
        cursor = database.cursor()
        cursor.execute("use TRENOBOT;")

        departure_datetime = dt.datetime.strptime(
            "2020-03-31 16:08:00", "%Y-%m-%d %H:%M:%S"
        )
        arrival_datetime = dt.datetime.strptime(
            "2020-03-31 16:48:00", "%Y-%m-%d %H:%M:%S"
        )
        stations = {}
        insert_query = f"INSERT INTO backend_trains (trainID, number, origin, destination, stations, departure_datetime, arrival_datetime, duration) VALUES (5050, 'S01529', 'Bergamo', 'Lecco', \"{stations}\", \"{departure_datetime}\", \"{arrival_datetime}\", 40);"
        cursor.execute(insert_query)
        database.commit()

        query_result = execute_query("backend_trains")
        self.assertEqual(len(query_result), 1)

        delete_query = "DELETE FROM backend_trains WHERE trainID = 5050"
        cursor.execute(delete_query)
        database.commit()
        database.close()

        query_result = execute_query("backend_trains")
        self.assertEqual(len(query_result), 0)


# launch unit test cases
if __name__ == "__main__":

    unittest.main()
