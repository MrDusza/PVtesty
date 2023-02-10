import _thread, esp32
from display_handling import LCD_handling
from temp_api import read_ds_sensor, change_temp_factor
from time import sleep
from machine import Timer, Pin, freq

#========================================================================================================
freq(240000000)

but0 = Pin(14, Pin.IN, Pin.PULL_UP)
but1 = Pin(27, Pin.IN, Pin.PULL_UP)

global_time = 0
set_temperature = 50
water_temperature = 0.0

#=========================================================================================================
def global_time_inc(Timer):
    global global_time
    global_time += 1

global_timer = Timer(1)
global_timer.init(period=10, mode=Timer.PERIODIC, callback=global_time_inc)
#==========================================================================================================

result_temp = [set_temperature ,water_temperature]
     
while True:
    if global_time % 450 == 0:
        water_temperature = read_ds_sensor()
        
    if global_time % 100 == 0:
        set_temperature = change_temp_factor(set_temperature)
        if but0.value() == 0 or but1.value() == 0:
            LCD_handling("Maksymalna dozwolona","temperatura wody:","",str(set_temperature)+chr(223)+"C    ")
        else:
            LCD_handling("Status:"+" "+str(global_time), "Temp: "+str(water_temperature)+" "+ chr(223)+"C   ", set_temperature, "chleb")
            
    
            
    
