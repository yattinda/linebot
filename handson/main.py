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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]


line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

class Timedata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    usertime = db.Column(db.int(60*1000), unique = True)

        def __init__(self,username,usertime):
            self.username = username
            self.usertime = usertime


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body:" + body)

    # handle webhook body
    try:
        profile = line_bot_api.get_profile(event.sorce.displayName)
        usertime = line_bot_api.get_message_content(event.message.timestamp)
        userId = line_bot_api.get_profile(event.sorce.userId)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def start_set(time):
    while True:
        try:
            time = int(time)
            #message_1をLINE上へ
            message_1 = "スタートを入力してください,開始します"
            input()
            if#startが入力されたら
                start_status = 1


            return time
            break
        except:
            message_1 = "ERROR!もう一度やりなおしてね！"
            start_status = 0




def time_start(start_status):
    if start_status == 1:
        sleep(3)
        message_2 = "スタート！"
        start = time.time()

def get_user_status(userId):
    user_status = db.session.query(Timedata).filter_by(user_id=user_id).first()
    if not user_status:
        user_status = UserStatus()
        user_status.user_id = userId
        user_status.usertime = usertime
        db.session.add(user_status)
        db.session.commit()
    return user_status



def timeresult(userId,usertime,time):
    #DBで要素ワケできないかな？DBの降順あると楽
    usertime = usertime/1000
    if usertime > time:
        dif_time = 9999999999999999
    elif usertime <= time:
        dif_time = time - usertime
    return dif_time





@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):


    usertime = Timedata(event.message.timestamp)
    username = Timedata(event.sorce.displayName)
    db.session.add(Timedata)
    db.session.commit()

    start_set(event.message.text)











    line_bot_api.reply_message(
        event.reply_token,

        TextSendMessage(text=)


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
