import unittest
from backend import app
from flask import json

# python -m unittest test_app


class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    # RealTime informaton

    def test_home_data(self):
        rv = self.app.get("/")

    def test_existing_train0(self):  # ok
        rv = self.app.get("/api/train/5050")
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data["compNumeroTreno"], "REG 5050")

    def test_existing_train1(self):  # ok
        rv = self.app.get("/api/train/2345")
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data["compNumeroTreno"], "REG 2345")

    def test_unexisting_train(self):
        rv = self.app.get("/api/train/1")
        self.assertEqual(rv.status_code, 404)

    def test_wrongformatted_train(self):
        rv = self.app.get("/api/train/50nm323dfdsjk")
        self.assertEqual(rv.status_code, 404)

    # Search trip solution

    def test_trip_solution0(self):  # ok
        rv = self.app.get(
            "/api/trip/search?from=lecco&to=milano&date=2020-04-15T18:00:0"
        )
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data["origine"], "Lecco")
        self.assertEqual(data["destinazione"], "Milano Centrale")

    def test_trip_solution1(self):  # wrong departure station
        rv = self.app.get(
            "/api/trip/search?from=lekko&to=milano&date=2020-04-15T18:00:0"
        )
        self.assertEqual(rv.status_code, 500)
        data = rv.data.decode("UTF-8")
        self.assertEqual(data, "Departure station not existing")

    def test_trip_solution2(self):  # wrong destination station
        rv = self.app.get(
            "/api/trip/search?from=lecco&to=mi4dno&date=2020-04-15T18:00:0"
        )
        self.assertEqual(rv.status_code, 500)
        data = rv.data.decode("UTF-8")
        self.assertEqual(data, "Destination station not existing")

    def test_trip_solution3(self):  # miss parameter from
        rv = self.app.get("/api/trip/search?&to=milano&date=2020-04-15T18:00:0")
        self.assertEqual(rv.status_code, 500)
        data = rv.data.decode("UTF-8")
        self.assertEqual(data, "No from string received")

    def test_trip_solution4(self):  # miss parameter to
        rv = self.app.get("/api/trip/search?from=lecco&date=2020-04-15T18:00:0")
        self.assertEqual(rv.status_code, 500)
        data = rv.data.decode("UTF-8")
        self.assertEqual(data, "No to string received")

    def test_trip_solution5(self):  # miss parameter date
        rv = self.app.get("/api/trip/search?from=lecco")
        self.assertEqual(rv.status_code, 500)
        data = rv.data.decode("UTF-8")
        self.assertEqual(data, "No to string received")

    def test_trip_solution6(self):  # datetime format error
        rv = self.app.get("/api/trip/search?from=lecco&to=palermo&date=2020-04-15T00:0")
        self.assertEqual(rv.status_code, 500)
        data = rv.data.decode("UTF-8")
        self.assertEqual(data, "Data format is wrong. Use YYYY-MM-GGTHH:MM:SS")

    def test_trip_solution7(self):  # datetime format error
        rv = self.app.get(
            "/api/trip/search?from=lecco&to=palermo&date=2020-04-15T18:00"
        )
        self.assertEqual(rv.status_code, 500)
        data = rv.data.decode("UTF-8")
        self.assertEqual(data, "Data format is wrong. Use YYYY-MM-GGTHH:MM:SS")

    def test_trip_solution8(self):  # datetime format error
        rv = self.app.get("/api/trip/search?from=lecco&to=palermo&date=-04-1518:00:0")
        self.assertEqual(rv.status_code, 500)
        data = rv.data.decode("UTF-8")
        self.assertEqual(data, "Data format is wrong. Use YYYY-MM-GGTHH:MM:SS")

    def test_trip_solution9(self):  # ok
        rv = self.app.get(
            "/api/trip/search?from=lecco&to=palermo&date=2020-04-15T18:00:0"
        )
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data["origine"], "Lecco")
        self.assertEqual(data["destinazione"], "Palermo C.le")
