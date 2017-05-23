import pyglet
import time


class Timer:
    def __init__(self, interval, func, repeat=True):
        self.interval = interval
        self.func = func
        self.repeat = repeat
        self.scheduled = False
        self.previous_call = None

    def schedule(self):
        if self.scheduled:
            return
        if self.repeat:
            if not self.interval:
                pyglet.clock.schedule(self.execute)
            else:
                pyglet.clock.schedule_interval(self.execute, self.interval)
        else:
            pyglet.clock.schedule_once(self.execute, self.interval)
        self.scheduled = True

    def execute(self, wtf):
        now = time.time()
        if not self.previous_call:
            self.previous_call = now
        self.func(now - self.previous_call)
        self.previous_call = now

    def unschedule(self):
        pyglet.clock.unschedule(self.execute)
        self.scheduled = False
