from win10toast import ToastNotifier
from bs4 import BeautifulSoup
import time
import requests

country = "Tunisia"
notification_duration = 10
refresh_time = 10 #minutes
worldmetersLink = "https://www.worldometers.info/coronavirus/"


def data_cleanup(array):
    L = []
    for i in array:
        i = i.replace("+","")
        i = i.replace("-","")
        i = i.replace(",",".")
        if i == "":
            i = "0"
        L.append(i.strip())
    return L

while True:
    try:
        html_page = requests.get(worldmetersLink)
    except requests.exceptions.RequestException as e: 
        print(e) #ConnectionError
        continue
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
    
    data= data_cleanup(data)
    message = "Total infected = {}, New Case = {}, Total Deaths = {}, New Deaths = {}, Recovred = {}, Active Case = {}, Serious Critical = {}".format(*data)
   
   # message = "Total infected : {}, New Case : {}, Total Deaths : {}, New Deaths : {}, Recovred : {}, Active Case : {}, Serious Critical : {}".format(*data)
   
    toaster = ToastNotifier()
    toaster.show_toast("Coronavirus {}".format(country) , message, duration = notification_duration , icon_path ="icon.ico")
    time.sleep(refresh_time*60)
