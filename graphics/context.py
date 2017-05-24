import pyglet
from pyglet.gl import *

from ui.geom import *


class Context(pyglet.graphics.OrderedGroup):
    def __init__(self, parent, offset=Vec(0, 0)):
        if parent:
            self.offset = Vec(parent.offset.x + offset.x, parent.offset.y - offset.y)
            self.index = parent.index = parent.index + 1
            self.batch = parent.batch
        else:
            self.index = 0
            self.offset = offset
            self.batch = pyglet.graphics.Batch()
        super().__init__(self.index, parent)

    def set_state(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def draw_rect(self, rect, color):
        x = self.offset.x
        y = self.offset.y
        vertexes = (x + rect.x, y + rect.y,
                    x + rect.x + rect.width, y + rect.y,
                    x + rect.x + rect.width, y + rect.y - rect.height,
                    x + rect.x, y + rect.y - rect.height)
        ctuple = color.tuple()
        colors = (*ctuple, *ctuple, *ctuple, *ctuple)
        self.batch.add(4, pyglet.gl.GL_QUADS, self, ('v2f', vertexes), ('c4B', colors))

    def draw(self):
        self.batch.draw()
