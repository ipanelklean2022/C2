import time
import serial
import pycrc
import paho.mqtt.client as mqtt
import time
import json
import sys
import ssl
import time
import datetime
import logging, traceback


number_of_remote_valves=10
remote_valves_offset=100
number_of_air_valves = 10
air_valves_offset = 200
number_of_water_valves = 10
water_valves_offset = 290
number_of_water_pumps = 10
water_pumps_offset = 400
number_of_air_compressor = 10
air_compressor_offset = 500

valves = []
address = []
cy_status = []
v_s = {}

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

lookup_table = dict( zip(valves,address ))



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


def ch_status_valves(valve_name,status):
   #valve name = V1,V2... WP3, AC1 etc
   #status = ON or OFF S_D['ON'] S_D['OFF']
   if  valve_name[0] != 'E':
    S_D ={'ON':1, 'OFF':0}
    k = (str(lookup_table[valve_name])+str(S_D[status]))
    print("k value ",k, str(lookup_table[valve_name])) 
    v_id =  str(lookup_table[valve_name])

    send_signal(k)
    print(k)

def wait(wait_duration):
    #time is in sec
    time.sleep(int(wait_duration))
