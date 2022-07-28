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

temp = check_CPU_temp()

try:
 st = speedtest.Speedtest()
 st.get_best_server()

 payload = {'Download': round(st.download() / 1000000, 2) , 'Upload': round(st.upload() / 1000000, 2), 'Ping': round(st.results.ping, 2), 'Temp': temp}
 
 r = requests.post('http://industrial.api.ubidots.com/api/v1.6/devices/raspberry-pi/?token='+ubiToken, data=payload)
 r = requests.get('https://api.telegram.org/bot'+telegramBot+'/sendMessage?chat_id='+chatId+'&text='+str(payload))
 
 # Print the server's response Uncomment the next line for debugging purposes
 #print(r.content)
except Exception as identifier:

 print(identifier)
