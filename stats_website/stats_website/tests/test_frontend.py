import unittest
from splinter import Browser
from stats_website.stats_website import app


class TestFrontend(unittest.TestCase):
    def test_home(self):
        browser = Browser("flask", app=app)
        browser.visit("/")
        self.assertTrue(browser.is_text_present("Provalo ora"))

    def test_search_working(self):
        browser = Browser("flask", app=app)
        browser.visit("/")
        browser.find_by_css('input[name="train"]').fill("with_stats")
        browser.find_by_css('[data-test="submit-search"]').first.click()
        self.assertTrue(browser.is_text_present("Treno with_stats"))

    def test_train_with_stats(self):
        browser = Browser("flask", app=app)
        browser.visit("/stats/view?train=with_stats")
        self.assertTrue(browser.is_text_present("Ecco le statistiche"))
        self.assertTrue(browser.is_text_present("corse monitorate: 7"))

    def test_train_with_stats_filtered_date(self):
        browser = Browser("flask", app=app)
        browser.visit("/stats/view?train=with_stats&from=2020-05-11&to=2020-05-14")
        self.assertTrue(browser.is_text_present("Ecco le statistiche"))
        self.assertTrue(browser.is_text_present("corse monitorate: 4"))

    def test_train_with_stats_all_filters(self):
        browser = Browser("flask", app=app)
        browser.visit(
            "/stats/view?train=with_stats&from=2020-05-11&to=2020-05-14&only_status=MODIFIED"
        )
        self.assertTrue(browser.is_text_present("Ecco le statistiche"))
        self.assertTrue(browser.is_text_present("corse monitorate: 1"))
        self.assertTrue(browser.is_text_present("Pulisci filtri"))
        self.assertTrue(
            browser.is_element_present_by_css('input[value="MODIFIED"][checked]')
        )

    def test_train_no_stats(self):
        browser = Browser("flask", app=app)
        browser.visit("/stats/view?train=no_stats")
        self.assertTrue(browser.is_text_present("Nessuna statistica"))

    def test_train_just_created(self):
        browser = Browser("flask", app=app)
        browser.visit("/stats/view?train=just_created")
        self.assertTrue(browser.is_text_present("Nessuna statistica"))
        self.assertTrue(browser.is_text_present("non era ancora tracciato"))

    def test_ranking(self):
        browser = Browser("flask", app=app)
        browser.visit("/stats/ranking")
        self.assertTrue(browser.is_text_present("Treni peggiori"))
        self.assertTrue(browser.is_text_present("Treni migliori"))
        self.assertTrue(browser.is_text_present("Ritardo medio"))
        self.assertTrue(browser.is_text_present("Affidabilità"))

    def test_average_delay(self):
        browser = Browser("flask", app=app)
        browser.visit("/")
        self.assertTrue(browser.is_text_present("ritardo medio"))
        self.assertTrue(browser.is_text_present("30 giorni"))

    def test_train_compare(self):
        browser = Browser("flask", app=app)
        browser.visit("/stats/compare?trains=with_stats&trains=with_stats_2")
        self.assertTrue(browser.is_text_present("Treno with_stats"))
        self.assertTrue(browser.is_text_present("Treno with_stats_2"))
