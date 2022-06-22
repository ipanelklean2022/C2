import time
import serial
import sys

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

#print(str( sys.argv[1]))
#send_signal( str(sys.argv[1])+'1')
#wait(13)
#send_signal( str(sys.argv[1])+'0')
#wait(13)

id = input('enter id')
print(id)
send_signal(id + '1')
wait(13)
send_signal(id + '0')
wait(13)

'''
print('400')
send_signal('4001')
wait(13)
send_signal('4000')
wait(13)

print('201')
send_signal('2011')
wait(13)
send_signal('2010')
wait(13)

print('300')
send_signal('3001')
wait(13)
send_signal('3000')
wait(13)

print('400')
send_signal('4001')
wait(13)
send_signal('4000')
wait(13)
'''
