import time

from .timer import Timer


def lerp(l, x, y):
    return x * (1 - l) + y * l


def linear_time_function(t):
    return t


def cubic_time_function(t):
    if t <= 0.5:
        return (t ** 2) * 2
    else:
        return 1 - (((t - 1) ** 2) * 2)


class Animation:
    def __init__(self, anim, duration=0.33, time_func=cubic_time_function):
        self._animFunc = anim
        self._duration = duration
        self._time_func = time_func
        self._first_tick = None
        self._timer = Timer(0, self._animate)

    def run(self):
        self._timer.schedule()

    def _animate(self):
        if not self._first_tick:
            self._first_tick = time.time()
        progress = (time.time() - self._first_tick) / self._duration
        if progress >= 1:
            self._animFunc(1)
            self.stop()
            return
        progress = self._time_func(progress)
        self._animFunc(progress)

    def stop(self):
        self._timer.unschedule()

    @classmethod
    def animate(cls, anim, duration=0.33, time_func=cubic_time_function):
        cls(anim, duration, time_func).run()

    @classmethod
    def animate_property(cls, obj, prop: property, end, start=None, duration=0.33, time_func=cubic_time_function):
        if not start:
            start = prop.fget(obj)

        def anim(t):
            obj.animating = True
            l = lerp(t, start, end)
            prop.fset(obj, l)
            obj.animating = False

        cls.animate(anim, duration, time_func)
