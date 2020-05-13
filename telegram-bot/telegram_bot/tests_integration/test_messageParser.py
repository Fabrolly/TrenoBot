import unittest
import validators
from telegram_bot.tests_integration.test_utility_methods import *

from telegram_bot.bot import create_db
from telegram_bot.messageResponder import getTrainList


class TestMessageParser(unittest.TestCase):
    def setUp(self):
        create_db(drop_tables=True)

    # TEST MESSAGE PARSER - TRENO
    def test_messageParser_ricerca_treno(self):
        search_train = "Treno 5050"
        response = call_mute_mp(search_train)
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(
            text_in_msg(
                response[0], [search_train, "BERGAMO", "LECCO", "Durata", "Stato"]
            )
        )
        self.assertTrue(
            text_in_buttons(
                response[1],
                [
                    "Aggiorna",
                    "Aggiungi alla Lista",
                    "Visualizza statistiche complete",
                    "Menu' principale",
                ],
            )
        )
        response = call_mute_mp("rimuovi 5050")
        self.assertTrue(is_riepilogo_empty())

    # TEST MESSAGE PARSER - SINTASSI NON VALIDA
    def test_messageParser_syntax_error(self):
        response = call_mute_mp("Ciao")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertFalse("Sintassi comando non valida" not in response[0])
        self.assertEqual(response[1], None)

    # TEST MESSAGE PARSER - TRENO NON ESISTE
    def test_messageParser_ricerca_treno_error(self):
        response = call_mute_mp("Treno 0001")
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Error" in response[0])
        self.assertEqual(response[1], "")

    # TEST MESSAGE PARSER - START
    def test_messageParser_start(self):
        response = call_mute_mp("/start")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(is_menu_principale(response[0], response[1]))

    # TEST MESSAGE PARSER - RDIR & RIMUOVI DIRETTRICE
    def test_messageParser_rdir_rimuovi_direttrice(self):
        response = call_mute_mp("/rdir1")
        response1 = call_mute_mp("rimuovi direttrice 1")
        self.assertEqual(response, response1)
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(
            text_in_msg(response[0], ["La direttrice 1", "non e' monitorata"])
        )
        self.assertTrue(
            text_in_buttons(
                response[1], ["Torna al menu direttrici", "Le mie direttrici attive"]
            )
        )

    # TEST MESSAGE PARSER - MENU PRINCIPALE
    def test_messageParser_menu_principale(self):
        response = call_mute_mp("menu principale")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(is_menu_principale(response[0], response[1]))

    # TEST MESSAGE PARSER - MENU TRENO
    def test_messageParser_menu_treno(self):
        response = call_mute_mp("menu treno")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        key_word = [
            "Visualizza lo stato di un Treno in tempo reale",
            "Ti basta scrivere il numero del tuo treno come l'esempio che segue:",
            "Treno 5050",
        ]
        self.assertTrue(text_in_msg(response[0], key_word))
        self.assertTrue(
            text_in_buttons(
                response[1], ["Non conosco il numero del treno", "Menu' Principale"]
            )
        )

    # TEST MESSAGE PARSER - MENU RICERCA
    def test_messageParser_menu_ricerca(self):
        response = call_mute_mp("menu ricerca")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        key_word = [
            "Cerca una soluzione di viaggio!",
            "Per esempio</b> per cercare da <b>Milano</b> a <b>Roma",
            "Ricerca da Milano a Roma",
            "Ricerca da Milano a Roma alle 20:30",
            "Ricerca da Milano a Roma alle 20:30 il 10-2",
            "Se ometti la data o l'ora viene considerata la data/ora attuale",
        ]
        self.assertTrue(text_in_msg(response[0], key_word))
        self.assertTrue(text_in_buttons(response[1], ["Menu' Principale"]))

    # TEST MESSAGE PARSER - MENU PROGRAMMAZIONE
    def test_messageParser_menu_programmazione(self):
        response = call_mute_mp("menu programmazione")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        text_key_word = [
            "Con Trenobot puoi tenere monitorato un treno e ricevere avvisi prima e durante la sua corsa.",
            "Terro' monitorato il tuo treno a partire da 30 minuti prima della partenza fino a quando non sarai arrivato.",
            "In caso di problemi e poco prima della partenza, ti avvisero' sui binari e sui dettagli degli eventuali disagi.",
            "Usa il menu' qui sotto per aggiungere un treno, oppure per visualizzare quelli gia' monitorati.",
        ]
        button_key_word = [
            "Aggiungi un treno alla tua Lista",
            "Visualizza la tua lista",
            "Menu' Principale",
        ]
        self.assertTrue(text_in_msg(response[0], text_key_word))
        self.assertTrue(text_in_buttons(response[1], button_key_word))

    # TEST MESSAGE PARSER - MENU PROGRAMMA
    def test_messageParser_menu_programma(self):
        response = call_mute_mp("menu programma")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        key_word = [
            "Aggiungi un treno alla tua Lista!",
            "Verrai aggiornato automaticamente sui ritardi, cancellazioni, modifiche e binari del tuo treno!",
            "Esempio</b>\nper aggiungere il treno <b>35091</b>, puoi scrivere:",
            "Programma 35091",
            "Se ometti i giorni della settimana viene considerato da Lunedi' a Venerdi'.",
            "Se ometti le stazioni intermedie viene considerata l'intera tratta",
        ]
        self.assertTrue(text_in_msg(response[0], key_word))
        self.assertTrue(text_in_buttons(response[1], ["Menu' Principale"]))

    # TEST MESSAGE PARSER - RIEPILOGO
    def test_messageParser_riepilogo(self):
        response = call_mute_mp("riepilogo")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        key_word = [
            "Riepilogo del tuo account",
            "Non hai alcun Treno nella tua /lista",
            "Non hai alcuna Direttrice monitorata",
            "Per aggiungere, rimuovere o modificare la tua lista usa i pulsanti qui sotto",
        ]
        self.assertTrue(text_in_msg(response[0], key_word))
        self.assertTrue(
            text_in_buttons(
                response[1], ["Lista Treni", "Lista direttrici", "Menu' Principale"]
            )
        )

    # TEST MESSAGE PARSER - LISTA
    def test_messageParser_lista(self):
        response = call_mute_mp("lista")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(
            text_in_msg(response[0], ["Non hai alcun Treno nella tua /lista"])
        )
        self.assertTrue(text_in_buttons(response[1], ["Menu' principale"]))

    # TEST MESSAGE PARSER - LISTA DIRETTRICI
    def test_messageParser_lista_direttrici(self):
        response = call_mute_mp("lista direttrici")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(
            text_in_msg(response[0], ["Non hai alcuna Direttrice monitorata"])
        )
        self.assertTrue(text_in_buttons(response[1], ["Menu' principale"]))

    # TEST MESSAGE PARSER - MENU DIRETTRICE
    def test_messageParser_menu_direttrice(self):
        response = call_mute_mp("menu direttrice")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(isinstance(response[0], list))
        self.assertTrue(isinstance(response[1], list))
        self.assertTrue(isinstance(response[0][0], tuple))
        self.assertTrue(validators.url(response[0][0][0]))
        self.assertEqual(response[0][0][1], "url")
        key_word = [
            "Aggiungi una Direttrice Trenord alla tua Lista!",
            "Quando trenord pubblica un tweet o un avviso relativo a delle problematiche su una direttrice verrai immediatamente avvisato!",
            "Individua la tua direttrice nell'elenco qui sopra.",
            "Per aggiungere una direttrice, scrivi:",
            "Direttrice Numero",
            "Esempio:</b>\n<i>Direttrice 1</i>",
        ]
        self.assertTrue(text_in_msg(response[0][1], key_word))
        self.assertEqual(response[1][0], "")
        self.assertTrue(
            text_in_buttons(
                response[1][1], ["Le mie direttrici attive", "Menu' Principale"]
            )
        )

    # TEST MESSAGE PARSER - PROGRAMMA
    def test_messageParser_programma(self):
        train_code = 5050
        response = call_mute_mp("programma " + str(train_code))
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(
            text_in_msg(
                response[0],
                [
                    "Riceverai aggiornamenti sul",
                    "Treno " + str(train_code),
                    "BERGAMO",
                    "LECCO",
                    "Nei giorni:",
                    "Lunedi Martedi Mercoledi Giovedi Venerdi",
                ],
            )
        )
        self.assertTrue(
            text_in_buttons(response[1], ["Visualizza lista", "Menu principale"])
        )
        call_mute_remove_train(train_code)
        self.assertTrue(is_riepilogo_empty())

    # TEST MESSAGE PARSER - DIRETTRICE
    def test_messageParser_direttrice(self):
        response = call_mute_mp("direttrice 1")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(
            text_in_msg(
                response[0],
                [
                    "Riceverai aggiornamenti sulla direttrice selezionata non appena ci saranno novita'!"
                ],
            )
        )
        self.assertTrue(
            text_in_buttons(
                response[1], ["Torna al menu direttrici", "Le mie direttrici attive"]
            )
        )
        response = call_mute_mp("/rdir1")
        self.assertTrue(is_riepilogo_empty())

    # TEST MESSAGE PARSER - RIMUOVI
    def test_messageParser_rimuovi(self):
        response = call_mute_mp("rimuovi 5050")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(
            text_in_msg(
                response[0], ["Nella tua /lista <b>non esiste</b> il Treno 5050"]
            )
        )
        self.assertTrue(
            text_in_buttons(response[1], ["Visualizza lista", "Menu principale"])
        )

    # TEST MESSAGE PARSER - PK
    def test_messageParser_pk(self):
        train_code = 2573
        response = call_mute_mp(
            "pk " + str(train_code) + "!12345!18:01!18:40!Lecco!Milano Centrale"
        )
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        self.assertTrue(
            text_in_msg(
                response[0],
                [
                    "Riceverai aggiornamenti sul\n\n<b>Treno "
                    + str(train_code)
                    + "</b>",
                    "LECCO -> MILANO CENTRALE",
                    "Nei giorni:",
                ],
            )
        )
        self.assertTrue(
            text_in_buttons(response[1], ["Visualizza lista", "Menu principale"])
        )
        call_mute_remove_train(train_code)
        self.assertTrue(is_riepilogo_empty())

    # TEST MESSAGE PARSER - MENU STATISTICHE
    def test_messageParser_statistiche(self):
        response = call_mute_mp("menu statistiche")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        text_key_word = [
            "Classifica dei treni migliori e peggiori",
            "Treni Migliori:",
            "Treni Peggiori:",
        ]
        button_key_word = [
            "Statistiche dettagliate",
            "Menu principale",
        ]
        self.assertTrue(text_in_msg(response[0], text_key_word))
        self.assertTrue(text_in_buttons(response[1], button_key_word))

    # TEST MESSAGE PARSER - STATISTICHE
    def test_messageParser_statistiche(self):
        train_code = 5050
        response = call_mute_mp(f"statistiche {train_code}")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        text_key_word = [
            f"STATISTICHE Treno {train_code}",
            "<b>Il Treno %s sarà monitorato!</b>" % (train_code),
            "Potrai vederne le statistiche a partire dalla prossima corsa",
        ]
        button_key_word = [
            "Visualizza lista",
            "Menu principale",
        ]
        self.assertTrue(text_in_msg(response[0], text_key_word))
        self.assertTrue(text_in_buttons(response[1], button_key_word))

        response = call_mute_mp(f"statistiche {train_code}")
        self.assertTrue("Error" not in response)
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue("Sintassi comando non valida" not in response[0])
        text_key_word = [
            f"STATISTICHE Treno {train_code}",
            "<b>Il Treno %s è già monitorato</b>" % (train_code),
            "potrai vederne le statistiche a partire dalla prossima corsa!",
        ]
        button_key_word = [
            "Visualizza lista",
            "Menu principale",
        ]
        self.assertTrue(text_in_msg(response[0], text_key_word))
        self.assertTrue(text_in_buttons(response[1], button_key_word))

    # TEST MESSAGE PARSER - STATISTICHE ERROR
    def test_messageParser_statistiche_error(self):
        response = call_mute_mp("statistiche")
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue(
            text_in_msg(
                response[0],
                ["Errore! Inserire il codice del treno per vederne le statistiche!"],
            )
        )
        self.assertEqual(response[1], "")


# launch unit test cases if main
if __name__ == "__main__":
    unittest.main()
