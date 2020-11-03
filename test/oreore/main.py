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
    FollowEvent,
)
import os
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=False)

    def __init__(self, user_id):
        self.user_id = user_id
"""
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

"""
@handler.add(FollowEvent)
def handle_join(event):
    user_id = line_bot_api.get_profile(event.source.user_id)
    db.session.add(user_id)
    db.session.commit()
    msg = []
    msg.append(TextSendMessage(text="anan"))
    line_bot_api.reply_message(event.reply_token,msg)



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    contents = db.session.query(User.user_id).all()
    for i in contents:
        line_bot_api.push_message('i', TextSendMessage(text="AhiAhi"))

"""
@handler.add(MessageEvent, message=TextMessage)
def main(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    print(profile.user_id)

    messages = TextSendMessage(text=profile.user_id)
    line_bot_api.push_message(profile.user_id, messages=messages)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
