import onewire, ds18x20
from machine import Pin

increment_button = Pin(14, Pin.IN, Pin.PULL_UP)
decrement_button = Pin(27, Pin.IN, Pin.PULL_UP)
ds_pin = Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))


def change_temp_factor(set_temperature):
    if increment_button.value() == 0:
        if set_temperature < 95:
            set_temperature += 1
    if decrement_button.value() == 0:
        if set_temperature > 0:
            set_temperature -= 1
      
    return set_temperature
        
def read_ds_sensor():
    roms = ds_sensor.scan()
    ds_sensor.convert_temp()
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        if isinstance(temp, float):
            temp = round(temp, 2)
            water_temperature  = temp
            
    return water_temperature

 
    