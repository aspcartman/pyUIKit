from .color import Color
from .event import MouseEvent
from .geom import Rect, Vec
from .label import Label
from .view import View


class Button(View):
    def __init__(self, frame=None, origin=None, size=None, title='Button', action=None):
        super().__init__(frame, origin, size)
        label = Label()
        self.add_subview(label)
        self._label = label

        self.action = action
        self.title = title
        self.background_color = Color.scheme.warn()

    @property
    def title(self):
        return self._label.text

    @title.setter
    def title(self, value):
        self._label.text = value

    def preferred_size(self):
        return self._label.preferred_size() + Vec(20, 20)

    def layout(self):
        self._label.frame = Rect(size=self._label.preferred_size(), center=self.frame.size / 2)

    def mouse_enter(self, event: MouseEvent):
        self.background_color = Color.scheme.tint()
        if self.action:
            self.action()

    def mouse_leave(self, event: MouseEvent):
        self.background_color = Color.scheme.warn()

    def mouse_click(self, event: MouseEvent):
        self.background_color = Color.scheme.front()

    def mouse_release(self, event: MouseEvent):
        self.background_color = Color.scheme.tint()
