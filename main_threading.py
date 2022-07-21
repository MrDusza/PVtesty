import _thread
from machine import Pin
from time import sleep

led1 = Pin(4, Pin.OUT)
led2 = Pin(5, Pin.OUT)

lock1 = _thread.allocate_lock()
lock2 = _thread.allocate_lock()

def diode1():
    while True:
        lock1.acquire()
        led1.value(1)
        sleep(0.25)
        led1.value(0)
        sleep(0.25)
        lock1.release()
        #_thread.exit()
        
def diode2():
    while True:
        lock2.acquire()
        led2.value(1)
        sleep(1)
        led2.value(0)
        sleep(1)
        lock2.release()
        #_thread.exit()
        
#while True:
_thread.start_new_thread(diode1, ())
_thread.start_new_thread(diode2, ())
