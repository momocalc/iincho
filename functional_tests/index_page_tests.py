from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core import test_utils
from .tests import GoogleOAuthTestMixin
import os


class TopPageVisitorTest(GoogleOAuthTestMixin, StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        test_utils.create_test_user(2)

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

        # ログインリンクをクリック
        login_link.click()
        # googleのログインをする
        google_id = os.environ.get('TEST_GOOGLE_ID')
        google_pw = os.environ.get('TEST_GOOGLE_PASSWD')
        self._login_with_google(google_id, google_pw)

        delay = 3
        try:
            WebDriverWait(self.browser, delay).until(
                EC.title_contains('Iincho'))

        except TimeoutException:
            self.fail('login failed or took too much time to redirect to Iincho')
