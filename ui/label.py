import pyglet

from graphics import Context
from .color import Color
from .geom import Rect, Vec
from .view import View


class Label(View):
    def __init__(self, text="", frame=Rect()):
        super().__init__(frame)
        self._pyglet_label = pyglet.text.Label(dpi=226)
        self._pyglet_label.font_size = 10
        self.text = text
        self.text_color = Color.scheme.white()
        self.background_color = Color.clear()

    @property
    def text(self):
        return self._pyglet_label.text

    @text.setter
    def text(self, value):
        self._pyglet_label.text = value if value is not None else ""
        self.set_needs_layout()

    @property
    def text_color(self):
        return Color(tuple=self._pyglet_label.color)

    @text_color.setter
    def text_color(self, value):
        self._pyglet_label.color = value.tuple()

    def draw(self, ctx: Context):
        self._pyglet_label.x = ctx.offset.x
        self._pyglet_label.y = ctx.offset.y - self._pyglet_label.content_height + 5
        self._pyglet_label.draw()

    def preferred_size(self):
        return Vec(self._pyglet_label.content_width, self._pyglet_label.content_height)
