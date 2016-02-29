from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core import test_utils
from .tests import GoogleOAuthTestMixin


class TopPageVisitorTest(GoogleOAuthTestMixin, StaticLiveServerTestCase):
    fixtures = ['test_users.json', 'test_categories.json', 'test_2articles.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_a_user_login_and_visit_index_page(self):
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

        # 記事の一覧が投稿日時新しい順で表示されている
        articles = self.browser.find_elements_by_class_name('article_media')
        titles = []
        for a in articles:
            titles.append(a.find_element_by_class_name('media-heading').text)
        self.assertListEqual(['spam', 'ham', 'eggs'], titles)
        # カテゴリが表示されている

        # 1件目
        self.assertEqual(
            articles[0].find_element_by_class_name('li_category').text,
            '(not categorized)')

        # 2件目はカテゴリの階層がリストで表示されている
        categories = []
        for c in articles[1].find_elements_by_class_name('li_category'):
            categories.append(c.text)

        self.assertListEqual(['category1', 'category2', 'category3'], categories)
        # 投稿日時が表示されている
        self.assertRegex(
            articles[0].find_element_by_class_name('article_status').text,
            '2016/03/01')

        # オーナーのidが表示されている
        self.assertRegex(
            articles[0].find_element_by_class_name('article_status').text,
            'admin')

        # TODO:タグが表示されている

        # カテゴリをクリックする
        # クリックしたカテゴリページに遷移
        # トップページに戻る
        # オーナー名をクリックする
        # オーナーの記事一覧に遷移する
        # 記事名をクリックする
        # 記事詳細ページに遷移する
        # タグをクリックする
        # タグの検索結果に遷移する
