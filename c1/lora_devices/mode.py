from uts import *

def Manual_Air_Mode():
    #ch_status_valves('WP400','ON',cy_num,mqtt)
    #wait(30)
    #ch_status_valves('WP400','OFF',cy_num,mqtt)
    #wait(30)

    ch_status_valves(sys.argv[1], sys.argv[2])
    wait(15)
    return
def device_loop():
    for x in range(1,10):
       print("mode.py send>>", sys.argv[1]+str(x),sys.argv[2])
       ch_status_valves(sys.argv[1]+str(x), sys.argv[2])
       wait(15)


Manual_Air_Mode()
#device_loop()

