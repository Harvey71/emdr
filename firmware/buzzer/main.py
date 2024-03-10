from os import uname
from machine import Pin
from time import sleep_ms

ID = 'EMDR Buzzer'

machine = uname().machine
pin_no = 0
if machine.startswith('Teensy 4.0'):
    pin_no_left = 'D23'
    pin_no_right = 'D22'
elif machine.startswith('ESP module'):
    pin_no_left = 12  
    pin_no_right = 14
elif machine.startswith('Raspberry Pi Pico'):
    pin_no_left = 19
    pin_no_right = 18
    
pin_left = Pin(pin_no_left, Pin.OUT)
pin_right = Pin(pin_no_right, Pin.OUT)

def buzz(pin, duration_ms):
    pin.on()
    sleep_ms(duration_ms)
    pin.off()
    
def test():
    buzz(pin_left, 50)
    sleep_ms(1000)
    buzz(pin_right, 50)
    
def loop():
    global np
    while True:
        line = input()
        cmd, val, *_ = (line + ' ').split(' ')
        try:
            val = int(val)
        except:
            val = 0
        try:
            if cmd == 'l':
                # buzz left
                buzz(pin_left, val)
            elif cmd == 'r':
                # buzz right
                buzz(pin_right, val)
            elif cmd == 'i':
                # id command
                print(ID)
        except:
            print('error')

test()
loop()
