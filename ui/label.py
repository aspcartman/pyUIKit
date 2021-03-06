import pyglet

from .color import Color
from .context import Context
from .geom import Rect, Vec
from .view import View


class Label(View):
    def __init__(self, text="", frame=Rect()):
        super().__init__(frame)
        self._pyglet_label = pyglet.text.Label(text=text, dpi=226, font_size=10)
        self._text = None
        self.text = text
        self._text_color = None
        self.text_color = Color.scheme.white()
        self.background_color = Color.clear()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value if value is not None else ""
        self._pyglet_label.text = self._text

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value

    def draw(self, ctx: Context):
        ctx.draw_text(self._text, 10)

    def preferred_size(self):
        if self._pyglet_label:
            return Vec(self._pyglet_label.content_width, self._pyglet_label.content_height / 2)
        else:
            return Vec(0, 0)
