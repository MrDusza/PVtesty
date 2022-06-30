import onewire, ds18x20
from machine import Pin, SoftI2C, Timer
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

ds_pin = Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

def display(Timer):
    lcd.move_to(0,0)
    lcd.putstr("Moc: " + str(power) + " W     ")
    lcd.move_to(0,1)
    lcd.putstr("Temp: " + str(temp) + " " + chr(223) + "C")
    
def display_clear(Timer):
    lcd.clear()

def read_ds_sensor(Timer):
    global temp
    roms = ds_sensor.scan()
    ds_sensor.convert_temp()
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        if isinstance(temp, float):
            temp = round(temp, 1)

tim1 = Timer(0)
tim1.init(period = 5000, mode = Timer.PERIODIC, callback = display)

tim2 = Timer(1)
tim2.init(period = 4500, mode = Timer.ONE_SHOT, callback = display_clear)

tim3 = Timer(2)
tim3.init(period = 10000, mode = Timer.PERIODIC, callback = read_ds_sensor)

power = 0

lcd.putstr("MPPT driver v0.1")
lcd.move_to(0,1)
lcd.putstr("INICJALIZACJA...")

global temp
temp = 0
power = 0

while True:
    power = power + 1
    sleep(1)
    