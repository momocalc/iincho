from django.test.utils import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from core import test_utils

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

class EditArticleTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        test_utils.create_test_user(2)

    def tearDown(self):
        self.browser.quit()

    def _show_body_textarea(self):
        '''
        現在表示中のページ内のCodeMirrorのテキストエリアを表示する
        '''

        self.browser.execute_script(
            'document.getElementById(\'div_hidden_textarea\').style.overflow = \'visible\''
        )

    @override_settings(DEBUG=True)
    def test_can_create_a_article_and_can_update_it(self):
        # テスト用ログイン画面でログイン
        self.browser.get(self.live_server_url + '/test_login/test_user_1/password_1/')
        self.browser.implicitly_wait(3)

        # ヘッダーの「新規登録」を押下
        a_new_entry = self.browser.find_element_by_id('a_new_entry')
        a_new_entry.click()
        self.browser.implicitly_wait(3)

        # 新規登録ページに遷移する
        new_entry_url = self.browser.current_url
        self.assertRegex(new_entry_url, '^.+/articles/new/$')

        # プレイスホルダーに「タイトル」と表示されているテキストボックスにタイトルを入力する
        title_box = self.browser.find_element_by_id('article-title')
        self.assertEqual(
            title_box.get_attribute('placeholder'),
            'タイトル'
        )
        title_box.send_keys('this is title')

        # 本文の入力
        self._show_body_textarea()
        body = self.browser.find_element_by_id('codemirror_hidden_textarea')
        body.click()
        body.send_keys(Keys.SHIFT + "3") # '#'の入力
        body.send_keys(' This is Body')
        body.send_keys(Keys.ENTER)
        body.send_keys('`spam`')

        # 右にプレビューが表示されている
        title_out = self.browser.find_element_by_id('title-out').text
        self.assertEqual(title_out, 'this is title')

        body_out = self.browser.find_element_by_id('out')
        h1 = body_out.find_element_by_tag_name('h1')
        self.assertEqual(h1.text, 'This is Body')

        # 登録ボタンを押下する
        self.browser.find_element_by_xpath('//input[@type=\'submit\']').click()
        self.browser.implicitly_wait(3)

        # 詳細ページに遷移する
        detail_url = self.browser.current_url
        self.assertRegex(detail_url, '/articles/[0-9]+/')

        # 登録したタイトルが表示されている
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, 'this is title')
        # 登録した本文が整形されて表示されている（Markdown To HTML)
        detail_body_out = self.browser.find_element_by_id('out')
        detail_body_h1 = detail_body_out.find_element_by_tag_name('h1')
        self.assertEqual(detail_body_h1.text, 'This is Body')

        # 編集画面に遷移する
        self.browser.find_element_by_id('a_update').click()
        self.browser.implicitly_wait(3)
        edit_url = self.browser.current_url
        self.assertRegex(edit_url, 'articles/[0-9]+/edit/')

        # タイトルを入力する
        self.browser.find_element_by_id('article-title').send_keys(' mod title')

        # 本文を入力する
        self._show_body_textarea()
        body = self.browser.find_element_by_id('codemirror_hidden_textarea')
        body.send_keys(Keys.ENTER)
        body.send_keys('## add header ')
        body.send_keys(Keys.ENTER)

        # 登録ボタンを押下する
        self.browser.find_element_by_xpath('//input[@type=\'submit\']').click()
        self.browser.implicitly_wait(3)

        # 詳細ページに遷移する
        detail_url = self.browser.current_url
        self.assertRegex(detail_url, '/articles/[0-9]+/')
        # 登録したタイトルが表示されている
        self.assertRegex(self.browser.find_element_by_tag_name('h1').text, 'mod title')
        # 登録した本文が整形されて表示されている（Markdown To HTML)
        detail_body_out = self.browser.find_element_by_id('out')
        detail_body_h2 = detail_body_out.find_element_by_tag_name('h2')
        self.assertEqual(detail_body_h2.text, 'add header')

    def test_can_delete_a_owner_self_article(self):
        # テスト用ログイン画面でログイン

        # 自分の記事一覧ページに遷移

        # 一番上の記事のタイトルをクリック
        # 詳細ページに遷移

        # 削除リンクをクリック

        # 削除確認メッセージが表示される
        # キャンセルボタンをクリック
        # 削除確認メッセージが消える

        # 再度，削除リンクをクリック
        # 削除確認ページに遷移
        # 削除ボタンクリック
        # 自分の記事一覧ページに遷移
        # 一番上の記事が削除した記事ではない

        # 削除ページにgetアクセス
        # 詳細ページに遷移

        # 他者の一覧ページに遷移
        # 一番上の記事のタイトルをクリック
        # 詳細ページに遷移
        # 削除リンクが表示されていない

        # 他者の記事の削除ページにgetでアクセス
        # 詳細ページに遷移

        # 他者の記事の削除ページにpostでアクセス
        # 詳細ページに遷移
        pass


class GoogleOAuthTestMixin(object):
    '''
    webDriverでGoogleログインを行う
    '''

    def __approve_if_hasnt_approved(self):

        delay = 5
        try:
            WebDriverWait(self.browser, delay).until(
                EC.presence_of_element_located((By.ID, 'submit_approve_access')))

            approve = self.browser.find_element_by_id('submit_approve_access')

            # wait to enable approve button
            for i in range(5):
                if approve.is_enabled():
                    approve.click()
                    break
                else:
                    time.sleep(1)

        except TimeoutException:
            pass

    def _login_with_google(self, email, passwd):
        '''
        Googleアカウントでログイン
        アカウント，パスワードの正当性は確認しない．
        :param email: gmail account
        :param passwd: gmail password
        :return: None
        '''

        delay = 3
        try:
            WebDriverWait(self.browser, delay).until(
                EC.title_contains('Google'))

            email_elem = self.browser.find_element_by_id('Email')
            email_elem.send_keys(email)
            passwd_elem = self.browser.find_element_by_id('Passwd')
            passwd_elem.send_keys(passwd)
            self.browser.find_element_by_id('signIn').click()
            self.__approve_if_hasnt_approved()

        except TimeoutException:
            print("took too much time to login with Google")

    def login(self):
        # ログインリンクをクリック
        login_link = self.browser.find_element_by_id("a_login")
        login_link.click()
        # googleのログインをする
        google_id = os.environ.get('TEST_GOOGLE_ID')
        google_pw = os.environ.get('TEST_GOOGLE_PASSWD')
        self._login_with_google(google_id, google_pw)

        delay = 3
        try:
            WebDriverWait(self.browser, delay).until(
                EC.title_contains('Iincho'))
            return True

        except TimeoutException:
            return False
