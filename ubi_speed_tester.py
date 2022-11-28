#!/usr/bin/python

from var import *

import speedtest
import requests
import re, os

def check_CPU_temp():
    temp = None
    msg = os.popen("vcgencmd measure_temp").readline()
    m = re.search(r'-?\d\.?\d*', msg)
    temp = float(m.group())
    return temp

def toggle_fan():
    power = os.popen("sudo uhubctl -l 1-1 -p 2 -a toggle").read()
    return power

temp = check_CPU_temp()
#fan = toggle_fan()

try:
 st = speedtest.Speedtest(secure=True)
 st.get_best_server()
 
 upload = round(st.upload() / 1000000, 2)
 download = round(st.download() / 1000000, 2)
 ping = round(st.results.ping, 2)

 payload = {'Download': download, 'Upload': upload, 'Ping': ping, 'Temp': temp}
 message = 'Download: ' + str(download) + ' Mbps \n' + 'Upload: ' + str(upload) + ' Mbps \n' + 'Ping: ' + str(ping) + ' ms \n' + 'CPU temp: ' + str(temp) + ' °C'

 r = requests.post('http://industrial.api.ubidots.com/api/v1.6/devices/raspberry-pi/?token='+ubiToken, data=payload)
 r = requests.get('https://api.telegram.org/bot'+telegramBot+'/sendMessage?chat_id='+chatId+'&text='+str(message))
 
 #Print the server's response Uncomment the next line for debugging purposes
 #print(r.content)
 #print(fan)
except Exception as identifier:

 print(identifier)
