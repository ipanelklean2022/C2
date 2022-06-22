import os
from time import sleep
from threading import Thread
import schedule
from urllib.request import urlopen
from datetime import datetime, timedelta
from mqtt_lib import MqttHandler
from a_v import *

class Amy(Thread):
    def mode_job(self,m,c,mqtt):       
        a = Switcher()
        a.numbers_to_modes(m,c,mqtt)

    def mainfunction(self,mqtt):
        m=1
        c=1
        while True:
          schedule.run_pending()          
          recv_data = mqtt._recv()
          if recv_data:
            print(recv_data)
            m_data= json.loads(recv_data.split('#')[0])
            t_data=recv_data.split('#')[1]
            
            if(t_data == "$aws/things/1/shadow/name/mode/update"):  
              #{"state":{"desired":{"mode":3}}}    
              print(type( m_data["state"]["desired"]["mode"]))
              try:
                m = int( m_data["state"]["desired"]["mode"])
                print("mode ", m)
                #mqtt._publish('$aws/things/1/shadow/name/mode/update/accepted','OK')
                a = Switcher()
                a.numbers_to_modes(m,1,mqtt)
              except:
                print("An exception occurred")

            elif(t_data == "$aws/things/1/shadow/name/modeconfiguration/update"):
              #{"state":{"desired":{"modes":[{"name":341,"nootcycles":3,"timings":["17:32","17:34","17:35"]}]}}}
              try:
                time = m_data["state"]["desired"]["modes"][0]["timings"]
                nc= m_data["state"]["desired"]["modes"][0]["noofcycles"]        
                m = int(m_data["state"]["desired"]["modes"][0]["name"])
                m =2
                for x in range(len(time)):
                  print("scheduler config set , mode:: ", time[x], m)
                  schedule.every().day.at(time[x]).do(self.mode_job,int(m),int(nc),mqtt)
              except:
                print("An exception occurred")

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
       mqtt=MqttHandler()
       mqtt
       while True:
         self.mainfunction(mqtt)


if __name__ == '__main__':
    res = urlopen('http://just-the-time.appspot.com/')
    result = res.read().strip()
    result_str = result.decode('utf-8')

    date_time_obj = datetime.strptime(result_str, '%Y-%m-%d %H:%M:%S')
    cur_datetime= str(date_time_obj + timedelta(hours=5.50))
    print(cur_datetime)
    cmd = "date -s '%s'"%(cur_datetime)
    os.system(cmd)

    amy = Amy()
    amy
    while True:
        pass
