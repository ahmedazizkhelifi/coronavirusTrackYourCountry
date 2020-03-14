from win10toast import ToastNotifier
from bs4 import BeautifulSoup
import time
import requests

country = "Tunisia"
notification_duration = 5
refresh_time = 10 #minutes

def data_cleanup(data):
    for i in range(len(data)):
        if data[i] == " " :
            data[i] = "0"
            continue
        try:
            while data[i][0] in ["+","-"," "]:
                data[i] = data[i][1:]
            if data[i][-1] == " " :
                data[i] = data[i][:-1]
                
        except :
            continue
             
while True:
    html_page = requests.get("https://www.worldometers.info/coronavirus/")
    bs = BeautifulSoup(html_page.content, 'html.parser')

    search = bs.select("div tbody tr td")
    start = -1
    for i in range(len(search)):
        if search[i].get_text().find(country) !=-1:
            start = i
            break
    data = []
    for i in range(1,8):
        try:
            data = data + [search[start+i].get_text()]
        except:
            data = data + ["0"]
    
    data_cleanup(data)
    data = [case.replace(',','.') for case in data]
    message = "Total infected = {}, New Case = {}, Total Deaths = {}, New Deaths = {}, Recovred = {}, Active Case = {}, Serious Critical = {}".format(*data)
   
   # message = "Total infected : {}, New Case : {}, Total Deaths : {}, New Deaths : {}, Recovred : {}, Active Case : {}, Serious Critical : {}".format(*data)
   
    toaster = ToastNotifier()
    toaster.show_toast("Coronavirus {}".format(country) , message, duration = notification_duration , icon_path ="icon.ico")
    time.sleep(refresh_time*60)
    
