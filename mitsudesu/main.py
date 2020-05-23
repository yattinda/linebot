from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage
)
import os
import random
import json
import time
import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNErint("+++++++++++++++++++++++++++++++++++++++;")L_SECRET)

#DB

class Remark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String, unique=False)
    remark_time = db.Column(db.DateTime, unique=False)

    def __init__(self, room_id, remark_time):
        self.room_id = room_id
        self.remark_time = remark_time

class Recall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mention = db.Column(db.String, unique=False)

    def __init__(self, mention):
        self.mention = mention

getout = ["やめろ",
          "かえれ",
          "出ていけ",
          "退陣",
          "収束した",
          "税金の無駄",
          "リコール",
          "辞任",
          "いらない",
          "うざい",
          "だるい",
          "石原",
          "都民ファースト",
          "ホリエモン",
          ]
#5分間に１０人発言
def five_minitue(contents, ROOM_ID):
    count = 10
    state = 1
    list = []
    while (count > 0):
        if contents[-state].room_id == ROOM_ID:
            list.append(contents[-state].remark_time)
            count -= 1

        state+= 1

    return(list)





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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    status = False
    print(event)
    ROOM_ID = event.source.group_id
    time = datetime.datetime.fromtimestamp(event.timestamp/1000)
    print(time)
    remark = Remark(ROOM_ID, time)
    db.session.add(remark)
    db.session.commit()
    contents = db.session.query(Remark).all()
    print("+++++++++++++++++++++++++++++++++++++++;")
    print(contents)
    print("**********+*++++++++++++++++++++*+*+*+*+*+*+*+")
    print(event.type)
    print("+++++++++++++++++++++++++++++++++++++++;")
    if event.type == "join":
        member_ids_res = line_bot_api.get_room_member_ids(ROOM_ID)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("member_ids_res")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if len(json.loads(member_ids_res.memberIds)) >= 1:
            message = "密です"

    elif event.message.text in getout:
        recall = Recall(event.message.text)
        db.session.add(recall)
        db.session.commit()
        recall_log = db.session.query(Recall).all()
        if recall_log[-1].id % 5 == 0:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage("東京改革")
            )
            status = True


            #グループトークからの退出処理
            if hasattr(event.source,"group_id"):
                line_bot_api.leave_group(event.source.group_id)
                db.session.query(Recall).delete()
                db.session.commit()



    #elif contents[-1].room_id == ROOM_ID:
    #    message = "happy"
    elif contents[-1].room_id == ROOM_ID and contents[-1].id > 10:

        first = five_minitue(contents, ROOM_ID)[9]
        last = five_minitue(contents, ROOM_ID)[0]
        print("####################################")
        print(last)
        print(first)
        print(first + datetime.timedelta(minutes = 10))
        print("#######################################")

        if first + datetime.timedelta(minutes = 10) > last:
            message = "mitudesu"
    else:
        message = "hogehoge"

    if status == False:
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(message)
            )





if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
