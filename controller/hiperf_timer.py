from time import perf_counter, sleep
from _thread import start_new_thread

class HighPerfTimer():
    def __init__(self, delay, action):
        self.delay = delay
        self.action = action
        self.start_counter = perf_counter()
    def start(self):
        start_new_thread(self.wait, (()))
    def wait(self):
        # cpu friendly wait for more than 10 ms
        def elapsed():
            return perf_counter() - self.start_counter
        if self.delay - elapsed() > 10 / 1000:
            sleep(self.delay - elapsed())
        # cpu intensive sleep for less than 10 ms
        while self.delay - elapsed() > 0:
            sleep(0)
        # now call back
        self.action()
