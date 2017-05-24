import pyglet
from pyglet.gl import *

from ui.color import Color
from ui.geom import *
from .shader import SimpleShader


class Context(pyglet.graphics.OrderedGroup):
    def __init__(self, parent, deep):
        if parent:
            self.index = deep
            self.batch = parent.batch
            self.shader = parent.shader
            self.parent = parent
        else:
            self.index = deep
            self.batch = pyglet.graphics.Batch()
            self.shader = SimpleShader()
            self.parent = None

        self._offset = Vec(0, 0)
        self._color = None
        self._vertex_lists = []
        super().__init__(self.index, parent)
        if not self.parent:
            self.shader.bind()

    @property
    def offset(self):
        if self.parent:
            return self.parent.offset + self._offset
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = Vec(value.x, - value.y)

    def set_state(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader.position = self.offset
        if self._color:
            self.shader.color = self._color
        else:
            self.shader.color = Color.clear()

    def draw_rect(self, rect, color):
        vertexes = (rect.x, rect.y,
                    rect.x + rect.width, rect.y,
                    rect.x + rect.width, rect.y - rect.height,
                    rect.x, rect.y - rect.height)
        self._color = color
        vl = self.batch.add(4, pyglet.gl.GL_QUADS, self, ('v2f', vertexes))
        self._vertex_lists.append(vl)

    def draw_text(self, text, size):
        label = pyglet.text.Label(text=text, dpi=226, font_size=size, batch=self.batch, group=self)
        label.y -= label.content_height / 2
        self._vertex_lists.append(label)

    def draw(self):
        self.batch.draw()

    def clear(self):
        for vl in self._vertex_lists:
            vl.delete()
        self._vertex_lists = []
