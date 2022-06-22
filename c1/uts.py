import time
import serial
import pycrc
import json
import sys
import ssl
import datetime
import logging, traceback
import paho.mqtt.client as mqtt
from a_v import *
from mqtt_lib import MqttHandler


'''    
    V1-wire1== V100 #present 
    V2-wire1== V101 #present 
    V3-wire1== V200 #present 
    V4-wire1== V201 #present 
    V5-wire1== V701 #present 
    V6-wire1== V801 #present 
    WV1 == WV201 #Not Present Relay
    WV2 == WV202 #present 
    WV3 == WV203 #present 
    WV4 == WV204 #present 
    WP == WP207 #Not Present Relay
    AC == AC206 #not present Relay
    AV1 == AV205 #Present

   
'''
'''
#older code sequence deviceID

number_of_remote_valves=110
remote_valves_offset=95
number_of_air_valves = 10
air_valves_offset = 200
number_of_water_valves = 10
water_valves_offset = 300
number_of_water_pumps = 10
water_pumps_offset = 400
number_of_air_compressor = 10
air_compressor_offset = 500

valves = []
address = []


for i in range(int(remote_valves_offset),int(remote_valves_offset)+int(number_of_remote_valves)):
    valves.append('V'+str(i+1))
    address.append(i+1)
for i in range(int(air_valves_offset),int(air_valves_offset)+int(number_of_air_valves)):
    valves.append('AV'+str(i+1))
    address.append(i+1)
for i in range(int(water_valves_offset),int(water_valves_offset)+int(number_of_water_valves)):
    valves.append('WV'+str(i+1))
    address.append(i+1)
for i in range(int(water_pumps_offset),int(water_pumps_offset)+int(number_of_water_pumps)):
    valves.append('WP'+str(i+1))
    address.append(i+1)
for i in range(int(air_compressor_offset),int(air_compressor_offset)+int(number_of_air_compressor )):
    valves.append('AC'+str(i+1))
    address.append(i+1)
'''

cy_status_wireless = []
cy_status_wired = []
v_s_wireless = {}
v_s_wired = {}

#randam device add
valves = ['V100','V101','V200','V201','V701','V801','AV205','AC206','WV201','WV202','WV203','WV204','WP207']
address =[100,101,200,201,701,801,205,206,201,202,203,204,207]

lookup_table = dict( zip(valves,address ))

def modbus_status(status):
    ser = serial.Serial(
      port = "/dev/ttymxc5",
      baudrate = 9600,
      parity = serial.PARITY_NONE,
      bytesize = serial.EIGHTBITS,
      stopbits = serial.STOPBITS_ONE,
      xonxoff = 0,
      rtscts = 0,
      timeout = 1
      )
    #s = serial.Serial("/dev/ttymxc5",9600)
    cmd = [0, 0, 0, 0, 0, 0, 0, 0]
    cmd[0] = 0x01  #Device address
    cmd[1] = 0x05  #command   
    #print("two digits: 0 to 7 (8 channels) and [0 (OFF) or 1 [ON]]")
    #k = input("enter the signal ")
    k=status
    if k[-1] == '1':
        i = str(int(k[-2])-1)
        cmd[2] = 0
        cmd[3] = int(i)
        cmd[4] = 0xFF
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        #print(cmd)
        ser.write(cmd)
        time.sleep(0.2)
    elif k[-1] == '0':
        j = str(int(k[-2])-1)
        cmd[2] = 0
        cmd[3] = int(j)
        cmd[4] = 0
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        #print(cmd)
        ser.write(cmd)
        time.sleep(0.2)
    return


def send_signal(signal):
    port_name = "/dev/ttymxc5"
    ser = serial.Serial(
      port = port_name,
      baudrate = 115200,
      parity = serial.PARITY_NONE,
      bytesize = serial.EIGHTBITS,
      stopbits = serial.STOPBITS_ONE,
      xonxoff = 0,
      rtscts = 0,
      timeout = 1
      )
    ser.write(signal.encode())
    wait(1)
    ser.close()
    return

def wait(wait_duration):    
    time.sleep(int(wait_duration)) #time is in sec

def ch_status_valves(valve_name, status, cy_number, mqtt):
   #valve name = V1,V2... WP3, AC1 etc
   #status = ON or OFF S_D['ON'] S_D['OFF']
   print("in UTS.py")
   deviceName = "0000001"
   if  valve_name[0] != 'E':
    S_D ={'ON':1, 'OFF':0}
    k = (str(lookup_table[valve_name])+str(S_D[status]))
    
    print("k value ",k, str(lookup_table[valve_name])) 
    v_id =  str(lookup_table[valve_name])
    if valve_name[0]=='V':
        send_signal(k)
        print("Wireless Data Send: "+str(k))
        cy_status_wireless.append(k)
        v_s_wireless[v_id] = k        
        valvestopic = "device/" + deviceName + "/valvewireless"
        valvemessage='{ "rundatetime" :'+ str(round(time.time()*1000))+',"data" : { "S" : '+str(k) +'}}'        
        mqtt._publish(valvestopic,valvemessage)
        print("Wireless MQTT Publish Message : "+valvemessage)

    elif valve_name[0:2] =='AV' or valve_name[0:2] =='AC' or valve_name[0:2] =='WP' or valve_name[0:2] =='WV':
        status = k[2:]
        modbus_status(status)
        print("Modbus Data send :"+str(status))
        cy_status_wired.append(status)
        v_s_wired[v_id] = status        
        valvestopic = "device/" + deviceName + "/valvewired"
        valvemessage='{ "rundatetime" :'+ str(round(time.time()*1000))+', "data" : { "S" : '+str(status) +'}}'        
        mqtt._publish(valvestopic,valvemessage)
        print("Modebus MQTT Publish Message : "+valvemessage)
   else:
    print("Cycle Number: ",cy_number)    
    cyc_status =str(cy_number)    
    #cycletopic = "device/" + deviceName + "/cycle"
    cycletopic_wireless = "device/" + deviceName + "/cyclewireless"
    cycletopic_wired = "device/" + deviceName + "/cyclewired"
    str1 = ","
    cy_status_wireless.clear()
    cy_status_wired.clear()

    for thevalue in v_s_wireless.values():
       cy_status_wireless.append(thevalue)
       
    for thevalue in v_s_wired.values():
       cy_status_wired.append(thevalue)

    #cyclemessage='{ "rundatetime" :'+ str(round(time.time()*1000))+',"cycle":{"cycle":'+cyc_status+', "mode":'+ status+', "status": 0, "data":"'+str1.join(cy_status)+'"}}' 
    cm_wireless='{ "rundatetime" :'+ str(round(time.time()*1000))+',"cycle":{"cycle":'+cyc_status+', "mode":'+ status+', "status": 0, "data":"'+str1.join(cy_status_wireless)+'"}}' 
    cm_wired='{ "rundatetime" :'+ str(round(time.time()*1000))+',"cycle":{"cycle":'+cyc_status+', "mode":'+ status+', "status": 0, "data":"'+str1.join(cy_status_wired)+'"}}' 


    #mqtt._publish(cycletopic,cyclemessage)
    mqtt._publish(cycletopic_wireless,cm_wireless)
    mqtt._publish(cycletopic_wired,cm_wired)
    print("Cycle Publish Message : "+ cm_wireless)
    print("Cycle Publish Message : "+ cm_wired)

    cy_status_wireless.clear()
    cy_status_wired.clear()
    v_s_wireless.clear()
    v_s_wired.clear()
    
