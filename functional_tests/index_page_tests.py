from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core import test_utils
from .tests import GoogleOAuthTestMixin
import os


class TopPageVisitorTest(GoogleOAuthTestMixin, StaticLiveServerTestCase):
    fixtures = ['test_users.json', 'test_2articles.json']
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_a_user_login(self):
        # トップページにアクセス
        self.browser.get(self.live_server_url)

        # サイト名が表示されている
        brand = self.browser.find_element_by_class_name("navbar-brand")
        self.assertEqual('Iincho', brand.text)

        with self.assertRaises(NoSuchElementException):
            # 新規登録リンクが表示されていない
            self.browser.find_element_by_id("a_new_entry")
            # ユーザーメニューが表示されていない
            self.browser.find_element_by_id("a_users_menu")

        # ログインリンクが表示されている
        login_link = self.browser.find_element_by_id("a_login")
        self.assertEqual('Login with Google', login_link.text)

        if not self.login():
            self.fail('login failed or took too much time to redirect to Iincho')


