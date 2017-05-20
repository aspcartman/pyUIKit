from ui.geom import *
import pyglet


class Context:
    def __init__(self, offset=Vec()):
        self.offset = offset

    def draw_rect(self, rect, color):
        x = self.offset.x
        y = self.offset.y
        vertexes = (x + rect.x, y + rect.y,
                    x + rect.x + rect.width, y + rect.y,
                    x + rect.x + rect.width, y + rect.y - rect.height,
                    x + rect.x, y + rect.y - rect.height)
        ctuple = color.tuple()
        colors = (*ctuple, *ctuple, *ctuple, *ctuple)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', vertexes), ('c4B', colors))

    def new_subcontext(self, offset):
        return Context(Vec(self.offset.x + offset.x, self.offset.y - offset.y))
