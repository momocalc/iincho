from django.test.utils import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
from core import test_utils
from urllib.parse import urljoin


class AuthorizationTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        test_utils.create_test_user(2)

    def tearDown(self):
        self.browser.quit()

    ## フレームワーク提供の認証処理を使用しているため，IDだけ未入力，PWだけ未入力などのパターンは省略する。
    def test_login_with_id_and_pw(self):
        # トップページにアクセスする
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(3)
        # ログインページにリダイレクトされる
        self.assertRegex(self.browser.current_url, '^.+accounts/login/\?next=/$')
        # ユーザIDを入力する
        user_id_element = self.browser.find_element_by_id('id_username')
        user_id_element.send_keys('test_user_1')

        # パスワードを入力する
        pw_element = self.browser.find_element_by_id('id_password')
        pw_element.send_keys('password_1')
        # ログインボタンを押す
        self.browser.find_element_by_id('normalLogin').click()
        # トップページにリダイレクトされる
        self.browser.implicitly_wait(3)
        self.assertRegex(self.browser.current_url, '^' + self.live_server_url + '/?$')

    def test_login_with_id_and_wrong_pw(self):
        # ログインページにアクセスする
        self.browser.get(urljoin(self.live_server_url, 'accounts/login'))
        self.browser.implicitly_wait(3)
        self.assertRegex(self.browser.current_url, '^.+accounts/login/?$')
        # ユーザIDを入力する
        user_id_element = self.browser.find_element_by_id('id_username')
        user_id_element.send_keys('test_user_2')

        # 間違ったパスワードを入力する
        pw_element = self.browser.find_element_by_id('id_password')
        pw_element.send_keys('password_1')
        # ログインボタンを押す
        self.browser.find_element_by_id('normalLogin').click()
        self.browser.implicitly_wait(3)
        # ログインページのまま
        self.assertRegex(self.browser.current_url, '^.+accounts/login/?$')
        # エラーメッセージが表示される
        self.assertRegex(self.browser.find_element_by_class_name('alert-danger').text, '正しいユーザー名とパスワードを入力してください')


class GoogleAuthorizationTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        test_utils.create_test_user(2)

    def tearDown(self):
        self.browser.quit()

    def test_google_login(self):
        # ログインページにアクセスする
        self.browser.get(urljoin(self.live_server_url, 'accounts/login'))
        self.browser.implicitly_wait(3)
        # Googleログインボタンを押す
        self.browser.find_element_by_id('googleLogin').click()
        self.browser.implicitly_wait(3)
        google_login = GoogleLogin(self.browser)
        self.assertTrue(google_login.login())


class GoogleLogin(object):
    '''
    webDriverでGoogleログインを行う
    '''

    def __init__(self, browser):
        self.browser = browser

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

            email_elem = self.browser.find_element_by_id('identifierId')
            email_elem.send_keys(email)
            self.browser.find_element_by_id('identifierNext').click()
            self.browser.implicitly_wait(2)
            passwd_elem = self.browser.find_element_by_name('password')
            passwd_elem.send_keys(passwd)
            self.browser.find_element_by_id('passwordNext').click()
            self.__approve_if_hasnt_approved()

        except TimeoutException:
            print("took too much time to login with Google")

    def login(self):
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
