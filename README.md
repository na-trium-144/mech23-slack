# mech23-slack

slackアプリ

.envに各種tokenやurlを書く

## サーバーとして
```sh
./main.sh
```

## 個別
* app.py
    * メンションやスラッシュコマンドに反応する
* ~~gcal-to-slack.py~~
    * https://github.com/jasonsnell/gcal-to-slack
    * googleカレンダーの予定をslackに送る
    * 現在使ってない
* mech_office.ipynb
    * スクレイピングしてお知らせをとってくる
