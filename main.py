from machine import ADC, Pin, PWM
from time import sleep
from math import sqrt

adc = ADC(0)

increment_button = Pin(13, Pin.IN, Pin.PULL_UP)
decrement_button = Pin(12, Pin.IN, Pin.PULL_UP)

pwm = PWM(Pin(0))
pwm.freq(5000)

def change_of_fill_factor():
    global fill_value
   
    if increment_button.value() == 0:
        if fill_value < 100:
            fill_value = fill_value + 1
    if decrement_button.value() == 0:
        if fill_value > 1:
            fill_value = fill_value - 1
                        
    print('Współczynnik wypełnienia:', fill_value, '%')
    
def current_value():
    mA_per_bit = 31.03
    reference_adc_value = 811
    reference_adc_diff = reference_adc_value - kalman_filter(adc.read())
    
    n_factor = fill_value / 100
    
    average_current_value = mA_per_bit * reference_adc_diff
    max_current_value = average_current_value / n_factor
    effective_current_value = sqrt(n_factor) * max_current_value
    
    #average_voltage_value =  (average_current_value * resistance) / 1000
    #max_voltage_value = (max_current_value * resistance) / 1000
    #effective_voltage_value = (effective_current_value * resistance) / 1000
    
    return effective_current_value
    
    #print('Wartość średnia prądu:', average_current_value, 'mA')
    #print('Wartość maksymalna prądu', max_current_value, 'mA')
    #print('Wartość skuteczna prądu', effective_current_value, 'mA')
    #print('Wartość średnia napięcia', average_voltage_value, 'V')
    #print('Wartość masymalna napięcia', max_voltage_value, 'V')
    #print('Wartość skuteczna napięcia', effective_voltage_value, 'V')

    
def power_value():
    resistance = 6.8
    power_value = ((current_value() / 1000) ** 2) * resistance
    print('Moc', power_value, 'W')
    
    return power_value

def MPPT_algorithm():
    global fill_value
    
    fill_value_array = []
    power_value_array = []
    old_power_value = 0
    cell_number = 0
    
    for fill_value_counter in range(0, 10):
        fill_value_array.append(fill_value - 5 + fill_value_counter)
        
        if fill_value_array[fill_value_counter] < 2:
            fill_value_array[fill_value_counter] = 1
        elif fill_value_array[fill_value_counter] > 99:
            fill_value_array[fill_value_counter] = 100
        
    for power_value_counter in range(0, 10):
        fill_value = fill_value_array[power_value_counter]
        pwm.duty(fill_value * 10)
        for kalman_wait in range(0, 10000):
            if kalman_wait == 9999:
                power_value_array.append(power_value())
                
    for highest_value_counter in range(0, 10):
        current_power_value = power_value_array[highest_value_counter]
        
        if current_power_value > old_power_value:
            cell_number = highest_value_counter
            old_power_value = current_power_value
        else:
            old_power_value = current_power_value
            
    fill_value = fill_value_array[cell_number]
    pwm.duty(fill_value * 10)
    fill_value_array.clear()
    power_value_array.clear()
           
def kalman_filter(adc_value):
    global kalman_adc_old
    global P1
    global Q
    global R
    global Kg
    global P 
    
    NowData =  adc_value
    LastData = kalman_adc_old
    P = P1 + Q
    Kg = P / (P + R)
    kalman_adc = LastData + Kg * (NowData - kalman_adc_old)
    P1 = (1 - Kg) * P
    P = P1
    kalman_adc_old = kalman_adc
    
    return kalman_adc
     
fill_value = 50
#-------------------Kalman's settings
kalman_adc_old = 0
P1 = 0
Q = 1     #0.0003
R = 5
Kg = 0
P = 1
#-------------------

while True:
    MPPT_algorithm()
    print('adc read', adc.read())
    change_of_fill_factor()
    power_value()
    print(' ')
    #sleep(0.1)