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

app = Flask(__name__)

channel_secret = 'SECRET_GET_FROM_HEROKU'
channel_access_token = 'ACCESS_TOKEN_GET_FROM_HEROKU'

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

    
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text
    input_text = str.lower(input_text)
    if input_text == "//help":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="input:taipeimrt"))
    if input_text == "taipeimrt":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="https://www.travelking.com.tw/eng/tourguide/taipei/taipeimrt/images/map.png"))


if __name__ == "__main__":
    app.run()