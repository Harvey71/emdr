from os import uname
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

NUMLED = 57
ID = 'EMDR Lightbar'

machine = uname().machine
pin_no = 0
if machine.startswith('Teensy 4.0'):
    pin_no = 'D1'
elif machine.startswith('ESP module'):
    pin_no = 5
elif machine.startswith('Raspberry Pi Pico'):
    pin_no = 16

np = NeoPixel(Pin(pin_no), NUMLED, bpp=3)

def clear():
    np.fill([0] * len(np))
    
def test():
    global np
    clear()
    np[0] = (0, 0x20, 0)
    np[-1] = (0x20, 0, 0)
    np.write()
    sleep_ms(500)
    clear()
    np.write()


def loop():
    global np
    col = (0x0f, 0, 0)
    while True:
        line = input()
        cmd, val, *_ = (line + ' ').split(' ')
        try:
            val = int(val)
        except:
            val = 0
        try:
            if cmd == 'c':
                # color cmd
                col = ((val >> 16) & 0xff, (val >> 8) & 0xff, val & 0xff)
            elif cmd == 'l':
                # led cmd
                clear()
                np[val - 1] = col
                np.write()
            elif cmd == 't':
                # test command
                clear()
                np[0] = col
                np[-1] = col
                np.write()
            elif cmd == 'i':
                # id command
                print(ID)
        except:
            print('error')

test()
loop()
            
            