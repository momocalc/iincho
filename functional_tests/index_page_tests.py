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

    def test_a_logged_in_user_visit_index_page(self):
        if not self.login():
            self.fail('login failed or took too much time to redirect to Iincho')

        delay = 3
        try:
            WebDriverWait(self.browser, delay).until(
                EC.title_contains('Iincho'))
        except TimeoutException:
            self.fail('too much time to load index page')

        # 記事の一覧が表示されている
        # カテゴリが表示されている
        # 投稿日時がyyyy/mm/ddで表示されている
        # オーナー名が表示されている
        # 記事名が表示されている
        # タグが表示されている

        # カテゴリをクリックする
        # クリックしたカテゴリページに遷移
        # トップページに戻る
        # オーナー名をクリックする
        # オーナーの記事一覧に遷移する
        # 記事名をクリックする
        # 記事詳細ページに遷移する
        # タグをクリックする
        # タグの検索結果に遷移する
