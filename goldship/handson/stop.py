from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import time

app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def start_set(time):
    while True:
        try:
            time = int(time)
            message_1 = "スタートを入力してください,開始します"
            break
            return message_1
            return time
        except:
            message_1 = "ERROR!もう一度やりなおしてね！"
            return message_1

def timer(time):
    start = time.time()
        #timetime()でスタンプを押した人の名前と時間を記録
        #もし全員がスタンプを押したら終了
        #時間を超えた人は終了



def timeresult(usertime,time):
    #DBで要素ワケできないかな？DBの降順あると楽
    if usertime > time:
        dif_time = 9999999999999999
    elif usertime <= time:
        dif_time = time - usertime
    return dif_time

def judge():
    message_2 = ("")



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):


    while True:
        try:
        time = int(("秒数を指定してください") )
        signal = input("スタートを入力してください")
        except:
            print("ERROR!もう一度やりなおしてね！")

    print("3秒後に開始します")
    sleep(3)
    print("start!!")
    start = time.time()
        #timetime()でスタンプを押した人の名前と時間を記録
        #もし全員がスタンプを押したら終了
        #時間を超えた人は終了
    winnername =
    winnertime =
    print("勝者は"+winnername+"で、時間は"+winnertime+"です")
    onemore = input("もう一度繰り返しますか（Y/N）")
    if onemore == N or onemore == n:
        break


    line_bot_api.reply_message(
        event.reply_token,

        TextSendMessage(text=finalreturn))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)