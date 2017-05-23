import time

from .timer import Timer
from typing import List


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
    def __init__(self, duration, offset=0, time_func=cubic_time_function, completion=None):
        self.duration = duration
        self.animation_functions = list()
        self.time_function = time_func
        self.completion = completion
        self.first_tick = None


class Animator:
    def __init__(self):
        self._current: List[Animation] = list()
        self._pending: List[Animation] = list()
        self._active: List[Animation] = list()
        self._timer = Timer(0, self.tick)

    def in_animation(self):
        return len(self._current) != 0

    def begin(self, duration=0.33, time_func=cubic_time_function):
        self._current.append(Animation(duration=duration, time_func=time_func))

    def add(self, animation):
        if len(self._current) == 0:
            raise Exception('No current animation')
        self._current[-1].animation_functions.append(animation)

    def commit(self, completion=None):
        if len(self._current) == 0:
            raise Exception('No current animation')

        anim = self._current.pop()
        if completion:
            anim.completion = completion

        self._pending.append(anim)
        self._timer.schedule()

    def tick(self):
        for anim in self._pending:  # Need to check if anim is ready to start
            self._pending.remove(anim)
            self._active.append(anim)

        now = time.time()
        for anim in self._active:
            if not anim.first_tick:
                anim.first_tick = now

            progress = (now - anim.first_tick) / anim.duration
            finished = progress >= 1
            if finished:
                progress = 1

            progress = anim.time_function(progress)
            for func in anim.animation_functions:
                func(progress)

            if finished:
                if anim.completion:
                    anim.completion()
                self._active.remove(anim)

        if len(self._pending) == 0 and len(self._active) == 0:
            self._timer.unschedule()
