# Iincho とは
qiitaの簡易クローン．Djangoの習作．

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
| IINCHO_SECRET_KEY           | Djangoで使う. seacret_key|
| DEBUG                       | debug modeの設定.  1:debug mode ON |
| GOOGLE_OAUTH2_CLIENT_ID     | google oauthのclient_id|
| GOOGLE_OAUTH2_CLIENT_SECRET | google oauthのclient_secret|
| DEMO                        | demo modeの設定． 1:demo mode ON   |

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
