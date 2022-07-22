 from uts import *

'''
    V1-wire1== V100 #present
    V2-wire1== V101 #present
    V3-wire1== V200 #present
    V4-wire1== V701 #present
    V5-wire1== V901 #present
    V6-wire1== V904 #present
    WV1 == WV201    #Present
    WV3 == WV203    #present
    WV4 == WV204    #present
    WP == WP207     #Present
    AC == AC206     #present
    AV1 == AV205    #Present
    AV2 == AV206    #Present
   this is Source Address:/home/inoviea/phalguni/Ruggedboard_inoviea cd /home/in
'''

def twoc_twop(cy_num,mqtt):
    valve_list1 =["V100","V101","V200","V701","V901","V904"]

    ch_status_valves('AV205','ON',cy_num,mqtt) #2.c
    wait(13)
    wait(10)#for air to travel to first valve

    for x in valve_list1:
        ch_status_valves(x,'ON',cy_num,mqtt)
        wait(13)
        ch_status_valves(x,'OFF',cy_num,mqtt) #2.e 2.f
        wait(13)
        wait(150)
    ch_status_valves('AV205','OFF',cy_num,mqtt)
    wait(13)

def Manual_Air_Mode(cy_num,mqtt):
    print("Manual Air_mode Start MODE 1")
    ch_status_valves('AC206','ON',cy_num,mqtt) #2.a
    wait(150)
    twoc_twop(cy_num,mqtt)
    ch_status_valves('AC206','OFF',cy_num,mqtt) #2.c
    wait(13)
    ch_status_valves('E','1',cy_num,mqtt)
    return

def Auto_Air_Mode(c, mqtt):
    print("Auto Air_Mode Start MODE 2")
    Manual_Air_Mode(c, mqtt)
    '''
    # if rain_sens is False:
    #     # if rain_flag=1 and rain_stop_time count start
    #     # if rain_stop_time>1800 & rain_time > 120
    #     #Manual_Air_Mode()
    #     # rain_flag=1
    # else:
    #     rain_flag=1
    #     #rain_time count start
    '''

def Super_Wash_Mode(cyc,mqtt):
    print("Super Wash_Mode Start MODE 3")
    valve_list =["V100","V101","V200","V701","V901","V904"]

    ch_status_valves('AC206','ON',cyc,mqtt) #4.b
    wait(150)
    twoc_twop(cyc,mqtt)
    ch_status_valves('WV201','ON',cyc,mqtt) #4.c
    wait(15)

    ch_status_valves('WP207','ON',cyc,mqtt) #4.d
    wait(120)#pumptorecharge water pump on

    for x in valve_list:
        ch_status_valves('WV204','ON',cyc,mqtt) #4.e
        wait(13)
        wait(40)#watertransfer
        ch_status_valves(x,'ON',cyc,mqtt)
        wait(13)
        wait(60)#watercleaning

        ch_status_valves('WV201','OFF',cyc,mqtt) #4.e.ii
        wait(13)
        ch_status_valves('WV202','ON',cyc,mqtt)#soap realease
        ch_status_valves('WV203','ON',cyc,mqtt)#soap release
        wait(13)
        wait(20) #soap release time
        ch_status_valves('WV202','OFF',cyc,mqtt)  #4.e.iii soap off
        ch_status_valves('WV203','OFF',cyc,mqtt)# soap off
        wait(13)
        ch_status_valves('AV205','ON',cyc,mqtt)
        wait(13)
        wait(5)#Air release time

        ch_status_valves(x,'OFF',cyc,mqtt) #4.e.v stop air wash1
        ch_status_valves('AV205','OFF',cyc,mqtt)
        wait(13)
        wait(150) #wait 3min for air comp to charge

        ch_status_valves('AV205','ON',cyc,mqtt)   #4.e.vi air wash2 start
        wait(13)
        ch_status_valves(x,'ON',cyc,mqtt)
        wait(13)
        wait(5) #Air blow time

        ch_status_valves(x,'OFF',cyc,mqtt) #4.e.vii stop air wash2
        ch_status_valves('AV205','OFF',cyc,mqtt)
        wait(13)
        wait(150) #wait 3min for air comp to charge

        ch_status_valves('AV205','ON',cyc,mqtt)  #4.e.viii
        wait(13)
        ch_status_valves(x,'ON',cyc,mqtt)
        wait(13)
        wait(5) #Air blow time

        ch_status_valves(x,'OFF',cyc,mqtt)  #4.e.ix stop air wash3
        ch_status_valves('AV205','OFF',cyc,mqtt)
        wait(13)
    wait(150) #wait 3min                     #4.k
    ch_status_valves('AV205','ON',cyc,mqtt)  #blow through entire system
    ch_status_valves('V100','ON',cyc,mqtt)
    ch_status_valves('V101','ON',cyc,mqtt)
    ch_status_valves('V200','ON',cyc,mqtt)
    ch_status_valves('V701','ON',cyc,mqtt)
    ch_status_valves('V901','ON',cyc,mqtt)
    ch_status_valves('V904','ON',cyc,mqtt)
    wait(20)

    ch_status_valves('AV205','OFF',cyc,mqtt)  #4.l shut entire system
    ch_status_valves('V100','OFF',cyc,mqtt) #shut entire system
    ch_status_valves('V101','OFF',cyc,mqtt)
    ch_status_valves('V200','OFF',cyc,mqtt)
    ch_status_valves('V701','OFF',cyc,mqtt)
    ch_status_valves('V901','OFF',cyc,mqtt)
    ch_status_valves('V904','OFF',cyc,mqtt)
    wait(20)

    wait(200)                              #4.m
    twoc_twop(cyc,mqtt) #repeat air wash
    ch_status_valves('WP207','OFF',cyc,mqtt)
    ch_status_valves('AC206','OFF',cyc,mqtt) #4.n  Switch off compressor

    ch_status_valves('E','3',cyc,mqtt)

def Manual_Testing_Air_Mode(cy_num,mqtt):
  #5.a
    print("Mannual Testing_Air_Mode MODE 4")
    ch_status_valves('AC206','ON',cy_num,mqtt) #2.a
    wait(150)
    ch_status_valves('AV205','ON',cy_num,mqtt)
    wait(13)
    wait (10) #for air to travel to first valve
    ch_status_valves('V100','ON',cy_num,mqtt)
    wait(13)
    ch_status_valves('V100','OFF',cy_num,mqtt) #2.e
    wait(13)
  #5.b
    ch_status_valves('AV205','OFF',cy_num,mqtt) #2.p
    ch_status_valves('AC206','OFF',cy_num,mqtt) #2.q
    wait(15)

def Manual_Testing_Super_Wash_Mode(cyc,mqtt):
    print("Mannual Testing_Super_Wash_Mode MODE 5")
    valve_list =["V100"]

    ch_status_valves('AC206','ON',cyc,mqtt) #4.b
    wait(150)
    twoc_twop(cyc,mqtt)

    ch_status_valves('WV201','ON',cyc,mqtt) #4.c
    wait(15)

    ch_status_valves('WP207','ON',cyc,mqtt) #4.d
    wait(120)#pumptorecharge

    for x in valve_list:
        ch_status_valves('WV204','ON',cyc,mqtt) #4.e
        wait(13)
        wait(40)#watertransfer
        ch_status_valves(x,'ON',cyc,mqtt)
        wait(13)
        wait(60)#watercleaning

        ch_status_valves('WV201','OFF',cyc,mqtt) #4.e.ii
        wait(13)
        ch_status_valves('WV202','ON',cyc,mqtt)#soap release
        ch_status_valves('WV203','ON',cyc,mqtt)#soap release
        wait(13)
        wait(20)#soap release time

        ch_status_valves('WV202','OFF',cyc,mqtt)  #4.e.iii soap off
        ch_status_valves('WV203','OFF',cyc,mqtt)# soap off
        wait(13)
        ch_status_valves('WV201','ON',cyc,mqtt) #plain water release
        wait(13)
        wait(40)#water release time

        ch_status_valves('WV204','OFF',cyc,mqtt)  #4.e.iv water shut down
        ch_status_valves('WV201','OFF',cyc,mqtt)
        wait(13)
        ch_status_valves('AV205','ON',cyc,mqtt) #air wash1 start (residue water
        wait(13)
        wait(13)#Air release time

        ch_status_valves(x,'OFF',cyc,mqtt) #4.e.v stop air wash1
        ch_status_valves('AV205','OFF',cyc,mqtt)
        wait(13)
         wait(150) #wait 4min for air comp to charge

        ch_status_valves('AV205','ON',cyc,mqtt)   #4.e.vi air wash2 start
        wait(13)
        ch_status_valves(x,'ON',cyc,mqtt)
        wait(13)
        wait(13) #Air blow time

        ch_status_valves(x,'OFF',cyc,mqtt) #4.e.vii stop air wash2
        ch_status_valves('AV205','OFF',cyc,mqtt)
        wait(13)
        wait(150) #wait 4min for compr recharge

        ch_status_valves('AV205','ON',cyc,mqtt)  #4.e.viii start air wash3
        wait(13)
        ch_status_valves(x,'ON',cyc,mqtt)
        wait(13)


        ch_status_valves(x,'OFF',cyc,mqtt)  #4.e.ix stop air wash3
        ch_status_valves('AV205','OFF',cyc,mqtt)
        wait(13)
    wait(150) #4.k wait 3min
    ch_status_valves('AV205','ON',cyc,mqtt)# blow through entire system
    ch_status_valves('V100','ON',cyc,mqtt)
    ch_status_valves('V101','ON',cyc,mqtt)
    ch_status_valves('V200','ON',cyc,mqtt)
    ch_status_valves('V701','ON',cyc,mqtt)
    ch_status_valves('V901','ON',cyc,mqtt)
    ch_status_valves('V904','ON',cyc,mqtt)
    wait(20)

    ch_status_valves('AV205','OFF',cyc,mqtt)  #4.l
    ch_status_valves('V100','OFF',cyc,mqtt)# shut entire system
    ch_status_valves('V101','OFF',cyc,mqtt)
    ch_status_valves('V200','OFF',cyc,mqtt)
    ch_status_valves('V701','OFF',cyc,mqtt)
    ch_status_valves('V901','OFF',cyc,mqtt)
    ch_status_valves('V904','OFF',cyc,mqtt)
    wait(20)

    wait(200)                              #4.m
    twoc_twop(cyc,mqtt) #repeat air wash
    ch_status_valves('WP207','OFF',cyc,mqtt)
    ch_status_valves('AC206','OFF',cyc,mqtt) #4.n Switch off compressor

    #Blue Light on  #4.O







