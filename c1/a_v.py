from datetime import datetime
from uts import *     #uts contains all the necessary definations and parameters 
from mode import *    # mode contains the mode definations 

  
class Switcher(object):
    def numbers_to_modes(self, argument, cyc,mqtt):
        method_name = 'mode_' + str(argument)                               # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid mode")         # Call the method as we return it
        return method(cyc,mqtt)
 
    def mode_1(self,cyc,mqtt):        
        print("In mode_1 file: a_v.py")
        Manual_Air_Mode(cyc,mqtt)
        return 

    def mode_2(self,cyc,mqtt):
        for i in range(1,int(cyc)+1):          
          Auto_Air_Mode(i,mqtt)
        return 

    def mode_3(self,cyc,mqtt):        
        Super_Wash_Mode(cyc,mqtt)
        return 
 
    def mode_4(self,cyc,mqtt):        
        Manual_Testing_Air_Mode(cyc,mqtt)
        return 
        
    def mode_5(self,cyc,mqtt):       
        Manual_Testing_Super_Wash_Mode(cyc,mqtt)
        return 