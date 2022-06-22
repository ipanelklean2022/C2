#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import serial
import pycrc
import time

s = serial.Serial("/dev/ttymxc5",9600)    
cmd = [0, 0, 0, 0, 0, 0, 0, 0]

cmd[0] = 0x01  #Device address
cmd[1] = 0x05  #command

def wiredsignal(signal):
        if signal[1]=='1':
                i = str(signal[0])
                cmd[2] = 0
                cmd[3] = int(i)
                cmd[4] = 0xFF
                cmd[5] = 0
                crc = pycrc.ModbusCRC(cmd[0:6])
                cmd[6] = crc & 0xFF
                cmd[7] = crc >> 8
                print(cmd)
                s.write(cmd)
                time.sleep(0.2)
        elif signal[1]=='0':
                i = str(signal[0])
                cmd[2] = 0
                cmd[3] = int(i)
                cmd[4] = 0
                cmd[5] = 0
                crc = pycrc.ModbusCRC(cmd[0:6])
                cmd[6] = crc & 0xFF
                cmd[7] = crc >> 8
                print(cmd)
                s.write(cmd)
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
    #time is in sec
    time.sleep(int(wait_duration))

while True:
        id1 = input(' Enter wireless device id: ')
        id2 = input(' Enter wired device id: ')
        send_signal(id1 + '1')
        wiredsignal(id2 + '1')
        print(id + ': On')
        wait(15)
        send_signal(id1 + '0')
        wiredsignal(id2 + '0')
        print(id + ': Off')
        wait(15)

