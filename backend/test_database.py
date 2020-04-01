import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import datetime as dt
import unittest
import MySQLdb

from database_initialization import database_initialization as db_inizialization


def delete_database():
    database = MySQLdb.connect("localhost", "root", "password")
    cursor = database.cursor()
    cursor.execute("DROP DATABASE IF EXISTS TRAINSTATISTICS;")
    database.commit()
    database.close()

def show_database():
    cursor = cursor_database()
    cursor.execute("show databases;")
    print("Database esistenti:")
    for databases in cursor:
        print(databases[0])
    return list(cursor)

def execute_query(table_name):
    cursor = cursor_database()
    cursor.execute("use TRAINSTATISTICS;")
    cursor.execute(f"SELECT * FROM {table_name}")
    print('Righe in Trains:')
    for query_element in cursor:
        print(query_element)
    return list(cursor)

def cursor_database():
    database = MySQLdb.connect("localhost", "root", "password")
    return database.cursor()



#class TestMssageParser(unittest.TestCase):
class Monolithic(unittest.TestCase):

    def setUp(self):
        delete_database()

    def test_create_database(self):

        print('\n\nTEST - CREAZIONE DATABASE\n')
        databases = show_database()
        self.assertEqual(len(databases), 3)

        db_inizialization()

        print('\nCREAZIONE E INIZIALIZZAZIONE DATABASE\n')

        databases = show_database()
        self.assertEqual(len(databases), 4)

        print('\nTEST PASSED')

    def test_insert_data(self):

        print('\n\nTEST - INSERIMENTO RIGA\n')
        db_inizialization()
        database = MySQLdb.connect("localhost", "root", "password")
        cursor = database.cursor()
        cursor.execute("use TRAINSTATISTICS;")

        query_result = execute_query('trains')
        self.assertEqual(len(query_result), 0)

        departure_datetime = dt.datetime.strptime("2020-03-31 16:08:00", "%Y-%m-%d %H:%M:%S")
        arrival_datetime = dt.datetime.strptime("2020-03-31 16:48:00", "%Y-%m-%d %H:%M:%S")

        #stations = [{"Bergamo" : "16:08"}, {"Ponte S.Pietro" : "16:14"}, {"Cisano Caprino Berga" : "16:27"}, {"Lecco" : "16:48"}]
        stations = {}

        insert_query = f"INSERT INTO trains (trainID, number, origin, destination, stations, departure_datetime, arrival_datetime, duration) VALUES (5050, 'S01529', 'Bergamo', 'Lecco', \"{stations}\", \"{departure_datetime}\", \"{arrival_datetime}\", 40);"
        cursor.execute(insert_query)
        database.commit()
        database.close()
        print('\nAGGIUNTA ESEGUITA\n')

        query_result = execute_query('trains')
        self.assertEqual(len(query_result), 1)

        print('\nTEST PASSED')

    def test_delete_data(self):

        print('\n\nTEST - CANCELLAMENTO RIGA\n')
        db_inizialization()
        database = MySQLdb.connect("localhost", "root", "password")
        cursor = database.cursor()
        cursor.execute("use TRAINSTATISTICS;")

        departure_datetime = dt.datetime.strptime("2020-03-31 16:08:00", "%Y-%m-%d %H:%M:%S")
        arrival_datetime = dt.datetime.strptime("2020-03-31 16:48:00", "%Y-%m-%d %H:%M:%S")
        stations = {}
        insert_query = f"INSERT INTO trains (trainID, number, origin, destination, stations, departure_datetime, arrival_datetime, duration) VALUES (5050, 'S01529', 'Bergamo', 'Lecco', \"{stations}\", \"{departure_datetime}\", \"{arrival_datetime}\", 40);"
        cursor.execute(insert_query)
        database.commit()

        query_result = execute_query('trains')
        self.assertEqual(len(query_result), 1)

        delete_query = "DELETE FROM trains WHERE trainID = 5050"
        cursor.execute(delete_query)
        database.commit()
        database.close()

        print('\nRIMOZIONE ESEGUITA\n')

        query_result = execute_query('trains')
        self.assertEqual(len(query_result), 0)

        print('\nTEST PASSED')

# launch unit test cases
if __name__ == "__main__":
    unittest.main()