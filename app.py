from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)

app = Flask(__name__)

channel_secret = '13d5c994d2cf69a6dfec00d8c2e38ade' #SECRET_GET_FROM_HEROKU
channel_access_token = '5qlESxRJZWdeKuRH60FNDJAtPtA96RfMxLtTIliG4qeYUVpKPjTfuJT5rZ92U8fPiM4qmzWT96fnmam7Zf5AFE5KuIt4F9LL9qzEVxnG3sxHLBkA1bxLo9MAfU1N+gOjdi1GcxkYGj9ZxxjFsXJJpwdB04t89/1O/w1cDnyilFU=' #ACCESS_TOKEN_GET_FROM_HEROKU

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
        png = "https://www.travelking.com.tw/eng/tourguide/taipei/taipeimrt/images/map.png"
        message = ImageSendMessage(
            original_content_url = png,
            preview_image_url = png
        )
        line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    app.run()