from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .tests import GoogleOAuthTestMixin
from selenium.webdriver.common.by import By


class ArticleSearchTest(StaticLiveServerTestCase):
    fixtures = ['test_users.json', 'test_categories.json', 'test_3articles.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


