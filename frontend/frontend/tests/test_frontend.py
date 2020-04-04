import unittest
from splinter import Browser
from frontend.frontend import app


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

    def test_train_no_stats(self):
        browser = Browser("flask", app=app)
        browser.visit("/stats/view?train=no_stats")
        self.assertTrue(browser.is_text_present("Nessuna statistica"))
