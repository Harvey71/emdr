from threading import Lock
import pickle

class Config():
    colors = [
        ('weiß', 255, 255, 255),
        ('rot', 255, 0, 0),
        ('grün', 0, 255, 0),
        ('blau', 0, 0, 255),
        ('gelb', 255, 255, 0),
    ]
    intensities = [
        20, 40, 60, 80, 100
    ]
    speeds = [
        10, 20, 30, 40, 50, 60, 80, 100, 120,
    ]
    durations = [
        100, 200, 300, 400, 500, 600, 800, 1000
    ]
    volumes = [
        20, 40, 60, 80, 100
    ]
    tones = [
        ('mittel/kurz', 440, 50),
        ('mittel/lang', 440, 100),
        ('hoch/kurz', 880, 100),
        ('hoch/lang', 880, 200),
        ('niedrig/kurz', 220, 25),
        ('niedrig/lang', 220, 50),
    ]
    data = {
        'general.speed': 10,
        'lightbar.on': True,
        'lightbar.intensity': 20,
        'lightbar.color': colors[0],
        'buzzer.on': True,
        'buzzer.duration': 100,
        'headphone.on': True,
        'headphone.volume': 0.5,
        'headphone.tone': tones[0],
    }

    @classmethod
    def load(cls):
        try:
            with open('emdr.config', 'rb') as f:
                cls.data = pickle.load(f)
        except:
            pass

    @classmethod
    def save(cls):
        with open('emdr.config', 'wb') as f:
            pickle.dump(cls.data, f)
