import pyglet


class Timer:
    def __init__(self, interval, func, repeat=True):
        self.interval = interval
        self.func = func
        self.repeat = repeat

    def schedule(self):
        if self.repeat:
            if not self.interval:
                pyglet.clock.schedule(self.execute)
            else:
                pyglet.clock.schedule_interval(self.execute, self.interval)
        else:
            pyglet.clock.schedule_once(self.execute, self.interval)

    def execute(self, wtf):
        self.func()

    def unschedule(self):
        pyglet.clock.unschedule(self.execute)
