from .event import MouseEvent
from .geom import Rect, Vec
from .timer import Timer
from .view import View


class ScrollView(View):
    def __init__(self, frame=Rect(), pos=None):
        super().__init__(frame, pos)
        content_view = View()
        super().add_subview(content_view)
        self._content_view = content_view
        self._timer = Timer(0, self.get_over_here)

    @property
    def content(self):
        return self._content_view

    @View.bounds.getter
    def bounds(self):
        return self._content_view.frame

    @property
    def content_size(self):
        return self._content_view.frame.size

    @content_size.setter
    def content_size(self, value):
        self._content_view.frame = self._content_view.frame.modified(size=value)

    def add_subview(self, view):
        self._content_view.add_subview(view)

    def mouse_scroll(self, event: MouseEvent):
        self._content_view.frame += Vec(event.delta.x, -event.delta.y)
        if (self.frame - self._content_view.frame).size < self.frame.size:
            self._timer.schedule()

    def get_over_here(self, dt):
        allowed = self.frame.size - self._content_view.frame.size
        allowed._x, allowed._y = min(0, allowed._x), min(0, allowed._y)
        origin = self._content_view.frame.origin
        miss = origin.outbound(allowed)
        if miss < Vec(0.5, 0.5):
            self._timer.unschedule()
        miss *= dt * 10
        self._content_view.frame = self._content_view.frame - miss
