import random, datetime, pytz

class helps:
    def __init__(self,command):
        self.command = command
    def helpsfunc(self):
        if self.command == "map" or self.command == "地圖":
            return '''使用方式：//map [地圖名稱] 或是 //地圖 [地圖名稱]
________________可查看地圖(輸出為圖片檔)
________________EX://map taipeimrt
________________地圖名稱:taipeimrt(台北捷運or臺北捷運)
                '''
        elif self.command == "rand" or self.command == "隨機":
            return '''使用方式：//rand a b 或是 //隨機 a b
________________可輸出a-b(a,b為整數)間的隨機整數
________________EX://rand 1 5
                '''
        elif self.command == "weather" or self.command == "天氣":
            return '''使用方式：//weather [功能] [參數] 或是 //天氣 [功能] [參數]
________________可查看天氣(輸出為圖片檔)EX://weather radar 30 (輸出雷達回波圖前調30分鐘)
________________功能：radar(雷達) [參數]往前調整回波圖時間，可不輸入，若輸入只能輸入0-120(以分為單位)
________________analysis(地面天氣圖) [參數空即可](Taiwan:UTC+8)
                '''
class maps:
    def __init__(self,maptext):
        self.message = ""
        self.maptext = maptext
    def mapfunc(self):
        png = ""
        if self.maptext == "taipeimrt" or self.maptext == "台北捷運" or self.maptext == "臺北捷運":
            png = "https://www.travelking.com.tw/eng/tourguide/taipei/taipeimrt/images/map.png"
        else:
            self.message = "未知地圖名，詳情請輸入\n//help map"
        if png != "":
            return png

class rand:
    def __init__(self,num1,num2):
        self.num1 = num1
        self.num2 = num2
    def randfunc(self):
        return random.randint(self.num1,self.num2)

class weather:
    def __init__(self,args):
        self.message = ""
        self.input_text = args
    def weatherfunc(self):
        try:
            if self.input_text[1] == "radar" or self.input_text[1] == "雷達":
                return self.radar()
            elif self.input_text[1] == "analysis" or self.input_text[1] == "地面天氣圖":
                return self.analysis()
            else:
                return "功能錯誤，詳情輸入//help weather"
        except Exception as e:
            return "請輸入功能，詳情輸入//help weather"

    def radar(self):#input_text = //weather radar [min]
        delaytime=0
        try:
            if self.input_text[2] != "":
                if self.input_text[2] == "no" or self.input_text[2] == "none" or self.input_text[2] == "沒圖":
                    return "如果沒有圖就表示還未產生，把時間往前調就行(預設已往前調10Min)\n往前調 x 分鐘指令=>//weather rader x"
                try:
                    delaytime=int(self.input_text[2]) + 10
                except:
                    return "請輸入的文字並非數字，將以原始模式跑圖！"
                else:
                    if 120 < delaytime or delaytime < 0:
                        delaytime=10
                        return "數字加10後只能介於0-120之間，將以原始模式跑圖！"
        except:
            delaytime=10
        finally:
            TW_time = pytz.timezone(pytz.country_timezones('tw')[0])
            nowtimes = datetime.datetime.now(TW_time) - datetime.timedelta(minutes=delaytime)
        minute = int(nowtimes.strftime("%M"))
        if minute >= 10:
            return "https://www.cwb.gov.tw/V7/observe/radar/Data/HD_Radar/CV1_3600_{}{}.png".format(nowtimes.strftime("%Y%m%d%H"),int(minute/10)*10)
        else:
            return "https://www.cwb.gov.tw/V7/observe/radar/Data/HD_Radar/CV1_3600_{}.png".format(nowtimes.strftime("%Y%m%d%H00"))
    def analysis(self):
        return "https://www.cwb.gov.tw/Data/fcst_img/I04.jpg"