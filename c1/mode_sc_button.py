import serial
from a_v import *
from mqtt_lib import MqttHandler


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttymxc2', 9600, timeout=1)
    ser.reset_input_buffer()
    l = 0
    mqtt=MqttHandler()
    mqtt
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8')
            if l != line[1]:
               l = line[1]
               m = int(line[1])
               a=Switcher()
               print("Manual switch Press (Mode): "+ str(m))
               a.numbers_to_modes(int(m),1,mqtt) 
            

