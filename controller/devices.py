from serial import Serial
from serial.tools.list_ports import comports
import pygame
from array import array
from device_config import DEVICE_CONFIG

class Note(pygame.mixer.Sound):
    def __init__(self, frequency, volume=.33):
        self.frequency = frequency
        super().__init__(buffer=self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

class Devices():
    led_num = 57
    _buzzer_duration = 100
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    _channel_left = pygame.mixer.Channel(0)
    _channel_left.set_volume(1, 0)
    _channel_right = pygame.mixer.Channel(1)
    _channel_right.set_volume(0, 1)
    _beep = Note(440)
    _sound_duration = 50
    _lightbar = (None, None)
    _buzzer = (None, None)

    @classmethod
    def probe(cls):
        _, ser = cls._lightbar
        if ser:
            ser.close()
        cls._lightbar = (None, None)
        _, ser = cls._buzzer
        if ser:
            ser.close()
        cls._buzzer = (None, None)
        for p in comports():
            for d in DEVICE_CONFIG.values():
                if (p.vid, p.pid) == (d['vid'], d['pid']):
                    ser = None
                    try:
                        ser = Serial(p.device, baudrate=d['baud'], timeout=0.1)
                        ser.write(b'i\r\n')
                        ser.flush()
                        if d['echo']:
                            ser.read_until()
                        id_str = ser.read_until().strip()
                        if id_str.find(b'EMDR Lightbar') == 0:
                            cls._lightbar = (d, ser)
                        elif id_str.find(b'EMDR Buzzer') == 0:
                            cls._buzzer = (d, ser)
                        else:
                            ser.close()
                    except:
                        if ser:
                            ser.close()
                        pass

    @classmethod
    def lightbar_plugged_in(cls):
        return cls._lightbar != (None, None)

    @classmethod
    def buzzer_plugged_in(cls):
        return cls._buzzer != (None, None)

    @classmethod
    def write(cls, devser, cmd):
        (dev, ser) = devser
        if dev and ser:
            ser.write(cmd)
            ser.flush()
            if dev['echo']:
                ser.read_until().strip()


    @classmethod
    def set_led(cls, num):
        if num >= 0:
            cls.write(cls._lightbar, b'l %d\r\n' % num)
        else:
            cls.write(cls._lightbar, b't\r\n')

    @classmethod
    def set_color(cls, col):
        cls.write(cls._lightbar, b'c %d\r\n' % col)

    @classmethod
    def set_buzzer_duration(cls, duration):
        cls._buzzer_duration = duration

    @classmethod
    def do_buzzer(cls, left):
        cls.write(cls._buzzer, (b'l' if left else b'r') + b' %d\r\n' % cls._buzzer_duration)

    @classmethod
    def do_sound(cls, left):
        if left:
            cls._channel_left.play(cls._beep, cls._sound_duration)
        else:
            cls._channel_right.play(cls._beep, cls._sound_duration)

    @classmethod
    def set_tone(cls, frequency, duration, volume):
        cls._beep = Note(frequency)
        cls._sound_duration = duration
        cls._channel_left.set_volume(1 * volume, 0)
        cls._channel_right.set_volume(0, 1 * volume)
