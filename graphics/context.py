import pyglet
from pyglet.gl import *

from ui.geom import *
from .shader import SimpleShader


class Context(pyglet.graphics.OrderedGroup):
    def __init__(self, parent, offset=Vec(0, 0)):
        if parent:
            self.offset = Vec(parent.offset.x + offset.x, parent.offset.y - offset.y)
            self.index = parent.index = parent.index + 1
            self.batch = parent.batch
            self.shader = parent.shader
            self.parent = parent
        else:
            self.index = 0
            self.offset = offset
            self.batch = pyglet.graphics.Batch()
            self.shader = SimpleShader()
            self.parent = None

        self._color = None
        super().__init__(self.index, parent)

    def set_state(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if not self.parent:
            self.shader.bind()
        self.shader.position = self.offset
        self.shader.color = self._color

    def draw_rect(self, rect, color):
        vertexes = (rect.x, rect.y,
                    rect.x + rect.width, rect.y,
                    rect.x + rect.width, rect.y - rect.height,
                    rect.x, rect.y - rect.height)
        self._color = color
        self.batch.add(4, pyglet.gl.GL_QUADS, self, ('v2f', vertexes))

    def draw(self):
        self.batch.draw()
