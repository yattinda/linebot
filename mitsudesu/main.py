from flask import Flask, request, abort

from linebot import (
    LineBotApi,
    WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageSendMessage,
    VideoSendMessage,
    StickerSendMessage,
    AudioSendMessage,
    JoinEvent
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
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

#word list
getout = ["やめろ",
          "かえれ",
          "出ていけ",
          "退陣",
          "収束",
          "税金",
          "無駄",
          "リコール",
          "辞任",
          "いらない",
          "うざい",
          "だるい",
          "石原",
          "都民ファースト",
          "ホリエモン",
         ]

def five_minitue(contents, ROOM_ID):
    """１０人発言したときの最新のlistを返す"""
    count = 10
    state = 1
    list = []
    while (count > 0):
        try:
            if contents[-state].room_id == ROOM_ID:
                list.append(contents[-state].remark_time)
                count -= 1
            state+= 1
        except:
            break

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

#グループ招待イベント
@handler.add(JoinEvent)
def handle_join(event):
    """ 課金必須
    ROOM_ID = event.source.group_id
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(ROOM_ID)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    member_ids_res = line_bot_api.get_group_member_id(ROOM_ID)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(member_ids_res)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    if len(json.loads(member_ids_res.memberIds)) >= 2:
    """
    msg = []
    msg.append(TextSendMessage
    (text="追加いただきありがとうございます\uDBC0\uDC1A\uDBC0\uDC1A\uDBC0\uDC1A\nコロナウイルスはあなたのすぐ近くに存在します！\n三密を防ぎ、手洗いうがいで感染拡大を防止しましょう！")
        )

    line_bot_api.reply_message(
    event.reply_token,
    msg
        )

#メッセージイベント
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    status = False
    ROOM_ID = event.source.group_id
    time = datetime.datetime.fromtimestamp(event.timestamp/1000)
    remark = Remark(ROOM_ID, time)
    db.session.add(remark)
    db.session.commit()
    contents = db.session.query(Remark).all()
    group_num = len(five_minitue(contents,ROOM_ID))

    #退出イベント
    if event.message.text in getout:
        recall = Recall(event.message.text)
        db.session.add(recall)
        db.session.commit()
        recall_log = db.session.query(Recall).all()
        if recall_log[-1].id % 5 == 0:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage("私はソーシャルメディアディスタンスをとりますね\n東京改革！！\uDBC0\uDC30\uDBC0\uDC30")
            )
            status = True


            #グループトークからの退出処理
            if hasattr(event.source,"group_id"):
                line_bot_api.leave_group(event.source.group_id)
                db.session.query(Recall).delete()
                db.session.commit()

    elif contents[-1].room_id == ROOM_ID and group_num == 10:

        first = five_minitue(contents, ROOM_ID)[9]
        last = five_minitue(contents, ROOM_ID)[0]

        if first + datetime.timedelta(minutes = 3) > last:
            message = "三密状態です\nこれ以上の発言を控えましょう\uDBC0\uDC7E\uDBC0\uDC7E"

        elif "密" in event.message.text and "です" in event.message.text:
            message = "それは私のセリフです\uDBC0\uDC26\uDBC0\uDC26"

        elif "コロナ" in event.message.text:
            message = "こちらで情報を確認しましょう！\nhttps://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000164708_00001.html"

        elif "corona" in event.message.text.lower():
            message = "check the information here!\nhttps://www.who.int/emergencies/diseases/novel-coronavirus-2019"

        elif "感染者数" in event.message.text:
            message = "こちらでコロナウイルスの感染者が確認できます！\nhttps://www3.nhk.or.jp/news/special/coronavirus/data/"

        else:
            num = random.randrange(3)
            image_list = [
                        "mitsu1.jfif",
                        "mitsu2.png",
                        "mitsu3.png",
                        "distance1.jfif",
                        "distance2.png",
                        "distance3.png",
                        "new_lifestyle1.jpg",
                        "new_lifestyle2.jpg",
                        "new_lifestyle3.jpg",
                        "new_lifestyle4.jpg",
                          ]
            if num == 0:
                random_image = random.choice(image_list)
                line_bot_api.reply_message(
                    event.reply_token,ImageSendMessage(
                        original_content_url = "https://mitsudesu.herokuapp.com/static/images/"+random_image,
                        preview_image_url = "https://mitsudesu.herokuapp.com/static/images/"+random_image
                        )
                    )
            status = True
    elif "コロナ" in event.message.text:
        message = "こちらで情報を確認しましょう！\nhttps://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000164708_00001.html"

    elif "corona" in event.message.text.lower():
        message = "check the information here!\nhttps://www.who.int/emergencies/diseases/novel-coronavirus-2019"

    elif "感染者数" in event.message.text:
        message = "こちらでコロナウイルスの感染者が確認できます！\nhttps://www3.nhk.or.jp/news/special/coronavirus/data/"
    else:
        num = random.randrange(2)
        if num == 0:
            message = "このグループは比較的ソーシャルメディアディスタンスがとれています\uDBC0\uDC33\uDBC0\uDC33\uDBC0\uDC33\nこの調子で頑張ろう！"

    if status == False:
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(message)
            )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
