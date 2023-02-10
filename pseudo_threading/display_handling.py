from machine import Pin, SoftI2C,
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

I2C_ADDR = 0x27
totalRows = 4
totalColumns = 20

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

prstr0 = ""

def LCD_handling(row0, row1, row2, row3):
    
    global prstr0 
    
    if len(str(row0)) != len(str(prstr0)):
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr(str(row0))
        lcd.move_to(0,1)
        lcd.putstr(str(row1))
        lcd.move_to(0,2)
        lcd.putstr(str(row2))
        lcd.move_to(0,3)
        lcd.putstr(str(row3))
        
    else:
        lcd.move_to(0,0)
        lcd.putstr(str(row0))
        lcd.move_to(0,1)
        lcd.putstr(str(row1))
        lcd.move_to(0,2)
        lcd.putstr(str(row2))
        lcd.move_to(0,3)
        lcd.putstr(str(row3))
    
    prstr0 = row0

