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


class AuthorizationTest(StaticLiveServerTestCase):
    def test_login_with_id_and_pw(self):
        # トップページにアクセスする
        # ログインページにリダイレクトされる
        # ユーザIDを入力する
        # パスワードを入力する
        # ログインボタンを押す
        # ログインできる
        # トップページにリダイレクトされる

        pass

    def test_login_with_id_and_wrong_pw(self):
        # トップページにアクセスする
        # ログインページにアクセスする
        # ユーザIDを入力する
        # 間違ったパスワードを入力する
        # ログインボタンを押す
        # エラーメッセージが表示される
        pass

