from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .tests import GoogleOAuthTestMixin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import date

class ArticleTest(GoogleOAuthTestMixin, StaticLiveServerTestCase):
    fixtures = ['test_users.json', 'test_categories.json', 'test_articles.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        self.login()

    def tearDown(self):
        # self.browser.quit()
        pass


    def test_create_a_article_and_edit_it(self):
        # 新規投稿ページを開く
        self.browser.get(self.live_server_url + '/articles/new')

        # タイトル欄にプレースホルダが設定されている
        title = self.browser.find_element_by_id('article-title')
        self.assertEqual('category1/category2/.../タイトル #tag1, tag2',
                         title.get_attribute('placeholder'))

        # テンプレートから"日報"を選択する
        templates = Select(self.browser.find_element_by_id('id_templates'))
        templates.select_by_visible_text('/日報/%year/%month/%day/%name')
        self.browser.implicitly_wait(2)
        # タイトルに「日報/<年>/<月>/<日>/」が入力されている
        # TODO:ユーザー名のテスト
        title = self.browser.find_element_by_id('article-title')
        print(title.get_attribute('value'))
        self.assertRegex(title.get_attribute('value'),
                         '日報/{}/'.format(date.today().strftime("%Y/%m/%d")))
        # 本文に「# 作業内容」,「# 所感」が表示されている
        body = self.browser.find_element_by_id('editor_area')
        self.assertRegex(body.text, '# 作業内容')
        self.assertRegex(body.text, '# 所感')

        # タイトルの末尾に「 #日報」を追加
        title.send_keys(Keys.END)
        title.send_keys(' #日報')
        # 投稿ボタンを押下
        self.browser.find_element_by_id('btn_post').click()
        # 明細ページに遷移する
        # タイトル「test1」が表示されている
        # カテゴリ「/日報/<年>/<月>/<日>/」表示されている
        # タグ「日報」が表示されている
        # 本文が表示されている
        # 編集ボタンを押下
        # 編集ページに遷移する
        # タイトルに「 #テスト日報」を追加する
        # 本文に「タグにテスト日報を追加」と追記
        # 投稿ボタンを押下
        # 明細ページに遷移する
        # タイトル，カテゴリは新規投稿時と変わっていない
        # テスト日報タグが表示されている
        # 本文に「タグにテスト日報を追加」が含まれている

