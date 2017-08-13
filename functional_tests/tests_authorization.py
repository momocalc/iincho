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
        self.browser.get(urljoin(self.live_server_url,'accounts/login'))
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
        pass


