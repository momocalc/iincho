# Iincho とは
Djangoで作った[qiita](http://qiita.com/)や[esa](https://esa.io/) のなんちゃってクローン（パクリ）です．  
Django学習のために作成しました．  
アプリケーション名は，開発を始めたときに観てたアニメのキャラからとっただけで意味はありません．

## DEMO
[DEMOサイト](http://iin-cho.herokuapp.com/)  
**DEMOではファイルアップロードは出来ません**

### デモ用アカウント
| ユーザー名 | パスワード |
|------------|------------|
| test       | passwd     |


# 環境
+ Django:1.8
+ python:3.5

# 設定
## 環境変数 or .env
| key                         | value                                  |
|-----------------------------|----------------------------------------|
| IINCHO_SECRET_KEY           | Djangoで使うseacret_keyです            |
| DEBUG                       | debug modeの設定です.  1:debug mode ON |
| GOOGLE_OAUTH2_CLIENT_ID     | google oauthのclient_idです            |
| GOOGLE_OAUTH2_CLIENT_SECRET | google oauthのclient_secretです        |
| DEMO                        | demo modeの設定です．  1:demo mode ON   |

## demo mode
Iinchoはグーグルアカウントでログインすることを前提としていますが，  
デモモードの場合，ログイン画面でユーザー名とパスワードでログインできるようになります．  
また，デモモードではファイルアップロードはできません．

# エディタで利用したライブラリ
* [Markdown-Editor](https://github.com/jbt/markdown-editor)
    * [markdown-it](https://github.com/markdown-it/markdown-it)
    * [CodeMirror](http://codemirror.net/)
    * [highlight.js](http://softwaremaniacs.org/soft/highlight/en/)
    * [js-deflate](https://github.com/dankogai/js-deflate)
* [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload)


# QA
ご利用を検討されることがあるかもしれませんので念のためにQAを書いておきます．

|               Q              |                                    A                                   |
|:----------------------------:|:----------------------------------------------------------------------:|
| ウォッチはないの？           | ない． [esa](https://esa.io/) or [qiita](http://qiita.com/)をご利用ください． |
| 記事の共同編集はできないの？ | ない． [esa](https://esa.io/) or [qiita](http://qiita.com/)をご利用ください． |
| 記事の履歴はないの？         | ない． [esa](https://esa.io/) or [qiita](http://qiita.com/)をご利用ください． |
| 通知機能はないの？           | ない． [esa](https://esa.io/) or [qiita](http://qiita.com/)をご利用ください． |
| テンプレートはないの？       | ない． [esa](https://esa.io/) or [qiita](http://qiita.com/)をご利用ください． |
| 下書き，WIPはないの？        | ない． [esa](https://esa.io/) or [qiita](http://qiita.com/)をご利用ください． |
| プライベート機能はないの？   | ない． [qiita](http://qiita.com/)をご利用ください．                           |
