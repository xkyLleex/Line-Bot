from flask import Flask, request, abort
import appfunc

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
    input_text_list = input_text.split(" ")
    FrontText = input_text_list[0]
    if FrontText == "//help":#####_help_##### 
        try:
            func = appfunc.helps(input_text_list[1])
        except:
            text_message = '''指令：(前面加上//，之間要空格) EX://rand 1 5
____________//map [地圖名稱] 或是 //地圖 [地圖名稱]
____________//rand [a,b] 或是 //隨機 [a,b] (a,b為整數)
____________//weather [功能] [參數] 或是 //天氣 [功能] [參數]
____________指令詳情請打//help [指令] EX://help map
            '''
        else:
            text_message = func.helpsfunc()
        finally:
            if text_message == None:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="未知指令，請輸入指令//help來查詢指令")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=text_message.replace("_",""))
                )
                
    elif FrontText == "//map" or FrontText == "//地圖":#####_map_##### 
        try:
            func = appfunc.maps(input_text_list[1])
        except:
            text_message = "請輸入地圖名，有\ntaipeimrt"
            png = ""
        else:
            png = func.mapfunc()
            if png == None:
                text_message = func.message
            else:
                message = ImageSendMessage(
                    original_content_url = png,
                    preview_image_url = png
                )
        finally:
            if isinstance(png,str):
                line_bot_api.reply_message(
                    event.reply_token, 
                    TextSendMessage(text=text_message)
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, 
                    message
                )

    elif FrontText == "//rand" or FrontText == "//隨機":#####_rand_##### 
        a = 0;b = 0
        try:
            a = (int)(input_text_list[1])
            b = (int)(input_text_list[2])
        except Exception as e:
            text_message = "參數錯誤，請輸入//help rand來查詢用法"
        else:
            func = appfunc.rand(a,b)
            text_message = "隨機整數輸出:{}".format(func.randfunc())
        finally:
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text=text_message)
            )
    elif FrontText == "//weather" or FrontText == "//天氣":#####_weather_#####
        func = appfunc.weather(input_text_list)
        png = func.weatherfunc()
        if png.find("https",0,5) == 0:
            message = ImageSendMessage(
                original_content_url = png,
                preview_image_url = png
            )
            line_bot_api.reply_message(
                event.reply_token, 
                message
            )
        else:
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text=png)
            )  
    else:
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=input_text)
        )

if __name__ == "__main__":
    app.run()