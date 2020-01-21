import usb
import pygame
from array import array
import os


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
    _lightbar = None
    _buzzer = None

    @classmethod
    def probe(cls):
        if cls._lightbar:
            cls._lightbar.finalize()
            cls._lightbar = None
        if cls._buzzer:
            cls._buzzer.finalize()
            cls._buzzer = None
        devs = usb.core.find(find_all=True, idVendor=0x16c0)
        for dev in devs:
            try:
                #print(repr(dev))
                if os.name != 'nt':
                    if dev.is_kernel_driver_active(0):
                        dev.detach_kernel_driver(0)
                dev.write(0x03, 'i\n')
                id_arr = dev.read(0x84, size_or_buffer=64, timeout=100)
                id_str = ''.join(chr(x) for x in id_arr).strip()
                #print(id_str)
                if id_str.find('EMDR Lightbar') == 0:
                    cls._lightbar = dev
                if id_str.find('EMDR Buzzer') == 0:
                    cls._buzzer = dev
            except:
                dev.finalize()
                pass

    @classmethod
    def lightbar_plugged_in(cls):
        return cls._lightbar is not None

    @classmethod
    def buzzer_plugged_in(cls):
        return cls._buzzer is not None

    @classmethod
    def set_led(cls, num):
        dev = cls._lightbar
        if dev:
            if num >= 0:
                dev.write(3, 'l%d\n' % num)
            else:
                dev.write(3, 't\n')

    @classmethod
    def set_color(cls, col):
        dev = cls._lightbar
        if dev:
            dev.write(3, 'c%d\n' % col)

    @classmethod
    def set_buzzer_duration(cls, duration):
        cls._buzzer_duration = duration

    @classmethod
    def do_buzzer(cls, left):
        dev = cls._buzzer
        if dev:
            dev.write(3, ('l' if left else 'r') + '%d\n' % cls._buzzer_duration)

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
