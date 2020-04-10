#import io
#import sys
#from os import path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import random
import unittest
import test.test_utility_methods as utility


class TestFunctionality(unittest.TestCase):
    def setUp(self):
        self.assertTrue(utility.is_riepilogo_empty())

    def tearDown(self):
        self.assertTrue(utility.is_riepilogo_empty())

    # TEST FUNCTIONALITY - MONITORA RIMUOVI DIRETTRICE
    def test_monitora_rimuovi_direttrice(self):
        response = utility.call_mute_mp("direttrice 1")
        response = utility.call_mute_mp("lista direttrici")
        self.assertTrue(utility.text_in_msg(
            response[0],
            [
                "Ecco le tue direttrici",
                "Direttrice 1",
                "Novara-Milano-Treviglio",
                "Rimuovi: /rdir1",
            ],
        ))
        self.assertTrue(utility.text_in_buttons(
            response[1], ["Menu' principale"]
        ))
        response = utility.call_mute_mp("/rdir1")
        self.assertTrue(utility.text_in_msg(
            response[0], ["Direttrice 1 <b>rimossa</b>"]
        ))
        self.assertTrue(utility.text_in_buttons(
            response[1], ["Torna al menu direttrici", "Le mie direttrici attive"]
        ))

    # TEST FUNCTIONALITY - MONITORA LA STESSA DIRETTRICE
    def test_monitora_stessa_direttrice(self):
        response = utility.call_mute_mp("direttrice 1")
        response = utility.call_mute_mp("direttrice 1")
        self.assertTrue(utility.text_in_msg(
            response[0], ["Questa direttrice e' gia' monitorata."]
        ))
        self.assertTrue(utility.text_in_buttons(
            response[1], ["Torna al menu direttrici", "Le mie direttrici attive"]
        ))
        response = utility.call_mute_mp("/rdir1")
        self.assertTrue(utility.text_in_msg(
            response[0], ["Direttrice 1 <b>rimossa</b>"]
        ))
        self.assertTrue(utility.text_in_buttons(
            response[1], ["Torna al menu direttrici", "Le mie direttrici attive"]
        ))

    # TEST FUNCTIONALITY - MONITORA PIU' DIRETTRICI
    def test_monitora_piu_direttrici(self):
        response = utility.call_mute_mp("direttrice 1")
        response = utility.call_mute_mp("direttrice 2")
        response = utility.call_mute_mp("lista direttrici")
        key_word = [
            "Ecco le tue direttrici",
            "Direttrice 1",
            "Novara-Milano-Treviglio",
            "Rimuovi: /rdir1",
            "Direttrice 2",
            "Saronno-Seregno-Milano-Albairate",
            "Rimuovi: /rdir2",
        ]
        self.assertTrue(utility.text_in_msg(response[0], key_word))
        response = utility.call_mute_mp("/rdir1")
        response = utility.call_mute_mp("/rdir2")

    # TEST FUNCTIONALITY - MONITORA DIRETTRICE INESISTENTE
    def test_monitora_direttrice_inesistente(self):
        test_msg = [
            "direttrice 100",
            "direttrice 41",
            "direttrice 38",
            "direttrice 43",
            "direttrice 49",
            "direttrice 51",
            "direttrice 0",
            "direttrice -1",
            "direttrice 0.12",
        ]
        for msg in test_msg:
            response = utility.call_mute_mp(msg)
            self.assertTrue(isinstance(response, tuple))
            self.assertTrue(
                utility.text_in_msg(
                    response[0], ["Error: direttrice <b>non valida!</b> :pensive:"]
                )
            )
            self.assertEqual(response[1], "")

    # TEST FUNCTIONALITY - AGGIUNGI RIMUOVI TRENO"
    def test_aggiungi_rimuovi_treno(self):
        train_code = 5050
        test_msg = [
            "programma " + str(train_code) + " da Bergamo a Lecco",
            "programma " + str(train_code) + " Bergamo Lecco",
            "programma " + str(train_code),
        ]
        for msg in test_msg:
            response = utility.call_mute_mp(msg)
            response = utility.call_mute_mp("lista")
            self.assertTrue(isinstance(response, tuple))
            self.assertTrue(isinstance(response[0], list))
            self.assertEqual(len(response[0]), 2)
            self.assertTrue(isinstance(response[1], list))
            self.assertEqual(len(response[1]), 2)
            key_word = [
                "Ecco la tua lista",
                "<b>Treno " + str(train_code) + "</b>",
                "BERGAMO :arrow_right: LECCO",
                "Giorni:",
            ]
            self.assertTrue(utility.text_in_msg(" ".join(response[0]), key_word))
            self.assertEqual(response[1][0], "")
            self.assertTrue(
                utility.text_in_buttons(
                    response[1][1],
                    ["Stato in Real Time", "Rimuovi Treno " + str(train_code)],
                )
            )
            utility.call_mute_remove_train(train_code)

    # TEST FUNCTIONALITY - AGGIUNGI RIMUOVI TRENO CON GIORNI
    def test_aggiungi_rimuovi_treno_con_giorni(self):
        train_code = 5050
        days = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica']
        cont_iter = 0
        while cont_iter < 10:
            rand_days = random.sample(days, 2)
            self.assertEqual(len(rand_days), 2)
            self.assertNotEqual(rand_days[0], rand_days[-1])
            response = utility.call_mute_mp("programma " + str(train_code) + " " + rand_days[0] + " " + rand_days[-1])
            response = utility.call_mute_mp("lista")
            self.assertTrue(isinstance(response, tuple))
            self.assertTrue(isinstance(response[0], list))
            self.assertEqual(len(response[0]), 2)
            self.assertTrue(isinstance(response[1], list))
            self.assertEqual(len(response[1]), 2)
            key_word = [
                "Ecco la tua lista",
                "<b>Treno " + str(train_code) + "</b>",
                "BERGAMO :arrow_right: LECCO",
                "Giorni:",
                rand_days[0],
                rand_days[-1],
            ]
            self.assertTrue(utility.text_in_msg(" ".join(response[0]), key_word))
            self.assertEqual(response[1][0], "")
            self.assertTrue(
                utility.text_in_buttons(
                    response[1][1],
                    ["Stato in Real Time", "Rimuovi Treno " + str(train_code)],
                )
            )
            utility.call_mute_remove_train(train_code)
            cont_iter = cont_iter + 1

    # TEST FUNCTIONALITY - PROGRAMMA TRENO DA A CON ERROR
    def test_programma_da_a_error(self):
        train_code = 5050
        test_msg = [
            "programma " + str(train_code) + " da Bergamo a Milano",
            "programma " + str(train_code) + " da Milano a Bergamo",
            "Programma " + str(train_code) + " da Lecco a Bergamo",
        ]
        for msg in test_msg:
            response = utility.call_mute_mp(msg)
            self.assertTrue(isinstance(response, tuple))
            cond_partenza = utility.text_in_msg(response[0], ['ERRORE', 'Stazione di partenza NON esistente per questo treno'])
            cond_arrivo = utility.text_in_msg(response[0], ['ERRORE', 'Stazione di arrivo NON esistente per questo treno'])
            cond_successiva = utility.text_in_msg(response[0], ['ERRORE', 'La stazione di arrivo deve essere successiva a quella di partenza'])
            self.assertTrue(cond_partenza or cond_arrivo or cond_successiva)
            self.assertEqual(response[1], "")

    # TEST FUNCTIONALITY - AGGIUNGI STESSO TRENO
    def test_aggiungi_stesso_treno(self):
        train_code = 5050
        response = utility.call_mute_mp("programma " + str(train_code))
        response = utility.call_mute_mp("programma " + str(train_code))
        self.assertTrue(isinstance(response, tuple))
        self.assertTrue(utility.text_in_msg(
            response[0],
            [
                "Questo treno e' gia' nella tua lista.",
                "Se vuoi modificarlo, <b>rimuovilo</b> dalla tua lista e <b>raggiungilo</b>",
            ],
        ))
        self.assertTrue(utility.text_in_buttons(
            response[1], ["Visualizza lista", "Torna al menu principale"]
        ))
        utility.call_mute_remove_train(train_code)

    # TEST FUNCTIONALITY - AGGIUNGI PIU' TRENI
    def test_aggiungi_piu_treni(self):
        train_code_1 = 5050
        train_code_2 = 4949
        response = utility.call_mute_mp("programma " + str(train_code_1))
        response = utility.call_mute_mp("programma " + str(train_code_2))
        response = utility.call_mute_mp("lista")
        self.assertEqual(len(response[0]), 3)
        self.assertEqual(len(response[1]), 3)
        key_word = [
            "Ecco la tua lista",
            "<b>Treno " + str(train_code_2) + "</b>",
            "CHIAVENNA :arrow_right: COLICO",
            "<b>Treno " + str(train_code_1) + "</b>",
            "BERGAMO :arrow_right: LECCO",
        ]
        self.assertTrue(utility.text_in_msg(" ".join(response[0]), key_word))
        self.assertTrue(utility.text_in_buttons(
            response[1][1:],
            [
                "Stato in Real Time",
                "Rimuovi Treno " + str(train_code_2),
                "Rimuovi Treno " + str(train_code_1),
            ],
        ))
        utility.call_mute_remove_train(train_code_1)
        utility.call_mute_remove_train(train_code_2)


# launch unit test cases
if __name__ == "__main__":
    unittest.main()
