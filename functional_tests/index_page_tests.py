from django.test.utils import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# from django.contrib.auth.models import User
from core import test_utils


class TopPageVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        test_utils.create_test_user(2)

    def tearDown(self):
        self.browser.quit()

    def test_a_user_hasnt_logged_in_visit(self):
        # トップページにアクセス
        self.browser.get(self.live_server_url)

        # サイト名が表示されている
        brand = self.browser.find_element_by_class_name("navbar-brand")
        self.assertEqual('しっこくさん.io', brand.text)

        with self.assertRaises(NoSuchElementException):
            # 新規登録リンクが表示されていない
            self.browser.find_element_by_id("a_new_entry")
            # ユーザーメニューが表示されていない
            self.browser.find_element_by_id("a_users_menu")

        # ログインリンクが表示されている
        login_link = self.browser.find_element_by_id("a_login")
        self.assertEqual('ログイン', login_link.text)

        # ログインリンクをクリック
        login_link.click()
        self.browser.implicitly_wait(3)

        # googleのログインページに遷移する
        self.assertRegex(self.browser.current_url,'accounts\.google\.com\/ServiceLogin')