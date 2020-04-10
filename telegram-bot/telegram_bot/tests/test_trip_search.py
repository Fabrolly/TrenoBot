import re
import datetime
import unittest
from .test_utility_methods import *


def extract_assert_hour(text, time):
    solutions = text.split("!")
    cond = len(solutions) == 2
    dt = datetime.datetime.today()
    start_date = str(dt.day) + "-" + str(dt.month) + "-" + str(dt.year) + " " + time
    start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y %H:%M")
    for solution in solutions:
        dates = re.findall(r"\d{2}-\d{2}-\d{4}", solution)
        times = re.findall(r"\d{2}:\d{2}", solution)
        date = dates[0] + " " + times[1]
        date = datetime.datetime.strptime(date, "%d-%m-%Y %H:%M")
        cond = cond and (date >= start_date)
    return cond


def extract_assert_day(text, msg_date):
    dates = re.findall(r"\d{2}-\d{2}-\d{4}", text)
    cond = len(dates) == 2
    if msg_date[0] != "0" and msg_date[1] == "-":
        msg_date = msg_date[:0] + "0" + msg_date[0:]
    if msg_date[-2] == "-" and msg_date[-2] != "0":
        msg_date = msg_date[:-1] + "0" + msg_date[-1:]
    msg_date = msg_date + "-" + str(datetime.datetime.today().year)
    msg_date = datetime.datetime.strptime(msg_date, "%d-%m-%Y")
    for date in dates:
        date = datetime.datetime.strptime(date, "%d-%m-%Y")
        cond = cond and (msg_date <= date)
    return cond


class TestTripSearch(unittest.TestCase):

    # TEST FUNCTIONALITY - RICERCA UN TRENO
    def test_ricerca_treno(self):
        test_search_msg = ["Ricerca da Milano a Roma", "Ricerca Milano Roma"]
        if datetime.datetime.now().hour <= 15:
            test_search_msg.append("Ricerca da Roma Tiburtina a Milano Lambrate")
        for msg in test_search_msg:
            response = call_mute_mp(msg)
            self.assertTrue(isinstance(response, tuple))
            self.assertTrue(isinstance(response[0], list))
            self.assertTrue(len(response[0]) <= 2)
            self.assertTrue(isinstance(response[1], list))
            self.assertTrue(
                text_in_msg(
                    " ".join(response[0]),
                    ["Soluzione", "Treno", "Durata", "Milano", "Roma"],
                )
            )
            self.assertTrue(
                text_in_buttons(
                    response[1],
                    ["Aggiungi 1111 alla lista", "Aggiungi 2222 alla lista"],
                    True,
                )
            )

    # TEST FUNCTIONALITY - RICERCA UN TRENO ERROR
    def test_ricerca_treno_error_stazione(self):
        test_search_msg = [
            "Ricerca da Cosenza a Oggiono",
            "Ricerca da Milano a Roma il 31-12",
        ]
        for msg in test_search_msg:
            response = call_mute_mp(msg)
            self.assertTrue(isinstance(response, tuple))
            key_word = [
                "Le API di viaggiotreno non sono in grado di rispondere a questa richeiesta anche se il tuo comando e' valido.",
                "Il motivo e' sconosciuto e da attributire a viaggiatreno.it",
                "Cerca qui il tuo treno: http://www.trenitalia.com/",
                "Quando sai il numero del tuo treno torna qui!",
            ]
            self.assertTrue(text_in_msg(response[0], key_word))
            self.assertTrue(text_in_buttons(response[1], ["Menu' principale"]))

    # TEST FUNCTIONALITY - RICERCA UN TRENO ERROR STAZIONE PARTENZA
    def test_ricerca_treno_error_partenza(self):
        response = call_mute_mp("Ricerca da Peslago a Lecco")
        self.assertTrue(isinstance(response, tuple))
        key_word = [
            "Stazione di <b>PARTENZA</b> non esistente.",
            "CONSIGLI:",
            "Prova a scrivere solo le <b>prime parole chiave</b>, non il nome completo!",
            "Oppure prova a scrivere il <b>nome completo!</b>",
            "Esempio: Milano Porta Garibaldi",
        ]
        self.assertTrue(text_in_msg(response[0], key_word))
        self.assertEqual(response[1], "")

    # TEST FUNCTIONALITY - RICERCA UN TRENO ERROR STAZIONE ARRIVO
    def test_ricerca_treno_error_arrivo(self):
        response = call_mute_mp("Ricerca da Lecco a Peslago")
        self.assertTrue(isinstance(response, tuple))
        key_word = [
            "Errore\n\n-Prova a scrivere solo le <b>prime parole chiave</b>, non il nome completo!",
            "Esempio:\nMilano Porta\n\n-Oppure prova a scrivere il <b>nome completo!",
            "Esempio: Milano Porta Garibaldi",
            "Se il nome della stazione comprende piu' parole <b>usa i connettivi 'da' e 'a'</b> come in questo formato:",
            "Da Milano Centrale a Reggio Calabria",
            "Esempi Corretti:",
            "Da Roma a Milano\nDa Roma a Milano il 10-8",
        ]
        self.assertTrue(text_in_msg(response[0], key_word))
        self.assertEqual(response[1], "")

    # TEST FUNCTIONALITY - RICERCA UN TRENO CON DATA E/O ORA SBAGLIATE
    def test_ricerca_treno_data_ora_error(self):
        test_msg = [
            "Ricerca da Milano a Roma il 30-2",
            "Ricerca da Milano a Roma il 31-11",
            "Ricerca da Milano a Roma il 0-8",
            "Ricerca da Milano a Roma il 8-0",
            "Ricerca da Milano a Roma il 15-13",
            "Ricerca da Milano a Roma il 1013",
            "Ricerca da Milano a Roma alle 25:30",
            "Ricerca da Milano a Roma alle 20:65",
            "Ricerca da Milano a Roma alle 1530",
        ]
        for msg in test_msg:
            response = call_mute_mp(msg)
            self.assertTrue(isinstance(response, tuple))
            key_word = [
                u"Attenzione, l'ora o la data inserita è <b>errata</b>",
                "Input ricevuto =",
                "La preghiamo di riprovare.",
            ]
            self.assertTrue(text_in_msg(response[0], key_word))
            self.assertEqual(response[1], "")

    # TEST FUNCTIONALITY - RICERCA UN TRENO CON ORA
    def test_ricerca_treno_ora(self):
        test_times = ["15:00", "00:00", "9:15", "07:10", "13:47", "20:00", "23:55"]
        test_msg = ["Ricerca da Milano a Roma alle ", "Ricerca Milano Roma alle "]
        for msg in test_msg:
            for start_time in test_times:
                response = call_mute_mp(msg + start_time)
                self.assertTrue(isinstance(response, tuple))
                self.assertTrue(isinstance(response[0], list))
                self.assertTrue(len(response[0]) <= 2)
                self.assertTrue(isinstance(response[1], list))
                self.assertTrue(extract_assert_hour("!".join(response[0]), start_time))
                self.assertTrue(
                    text_in_msg(
                        " ".join(response[0]),
                        ["Soluzione", "Treno", "Durata", "Milano", "Roma"],
                    )
                )
                self.assertTrue(
                    text_in_buttons(
                        response[1],
                        ["Aggiungi 1111 alla lista", "Aggiungi 2222 alla lista"],
                        True,
                    )
                )

    # TEST FUNCTIONALITY - RICERCA UN TRENO CON GIORNO
    def test_ricerca_treno_giorno(self):
        day = (datetime.datetime.now() + datetime.timedelta(days=1)).day
        date = str(day) + "-" + str(datetime.datetime.now().month)
        test_dates = [
            date,
            "5-2",
            "05-8",
            "6-09",
            "07-04",
            "10-3",
            "4-10",
            "11-12",
            "10-04",
            "03-12",
            "10-10",
            "28-2",
            "30-11",
            "15-08",
        ]
        test_msg = ["Ricerca da Milano a Roma il ", "Ricerca Milano Roma il "]
        if datetime.datetime.now().hour <= 15:
            test_msg.append("Ricerca da Roma Tiburtina a Milano Lambrate il ")
        for msg in test_msg:
            for date in test_dates:
                response = call_mute_mp(msg + date)
                self.assertTrue(isinstance(response, tuple))
                self.assertTrue(isinstance(response[0], list))
                self.assertTrue(len(response[0]) <= 2)
                self.assertTrue(isinstance(response[1], list))
                self.assertTrue(extract_assert_day(" ".join(response[0]), date))
                self.assertTrue(
                    text_in_msg(
                        " ".join(response[0]),
                        ["Soluzione", "Treno", "Durata", "Milano", "Roma"],
                    )
                )
                self.assertTrue(
                    text_in_buttons(
                        response[1],
                        ["Aggiungi 1111 alla lista", "Aggiungi 2222 alla lista"],
                        True,
                    )
                )

    # TEST FUNCTIONALITY - RICERCA UN TRENO CON ORA & GIORNO
    def test_ricerca_treno_ora_giorno(self):
        start_time = "10:30"
        day = (datetime.datetime.now() + datetime.timedelta(days=1)).day
        date = str(day) + "-" + str(datetime.datetime.now().month)
        test_msg = [
            "Ricerca da Milano a Roma alle " + start_time + " il " + date,
            "Ricerca da Milano a Roma il " + date + " alle " + start_time,
            "Ricerca Milano Roma alle " + start_time + " il " + date,
            "Ricerca Milano Roma il " + date + " alle " + start_time,
            "Ricerca Da Roma Tiburtina a Milano Lambrate alle "
            + start_time
            + " il "
            + date,
            "Ricerca Da Roma Tiburtina a Milano Lambrate il "
            + date
            + " alle "
            + start_time,
        ]
        for msg in test_msg:
            response = call_mute_mp(msg)
            self.assertTrue(isinstance(response, tuple))
            self.assertTrue(isinstance(response[0], list))
            self.assertTrue(len(response[0]) <= 2)
            self.assertTrue(isinstance(response[1], list))
            self.assertTrue(extract_assert_hour("!".join(response[0]), start_time))
            self.assertTrue(extract_assert_day(" ".join(response[0]), date))
            self.assertTrue(
                text_in_msg(
                    " ".join(response[0]),
                    ["Soluzione", "Treno", "Durata", "Milano", "Roma"],
                )
            )
            self.assertTrue(
                text_in_buttons(
                    response[1],
                    ["Aggiungi 1111 alla lista", "Aggiungi 2222 alla lista"],
                    True,
                )
            )


# launch unit test cases
if __name__ == "__main__":
    unittest.main()
