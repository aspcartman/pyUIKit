import pyglet
from pyglet.gl import *

from ui.color import Color
from ui.geom import *
from .group import FuckYouGroup
from .shader import SimpleShader


class Context:
    def __init__(self):
        super().__init__()
        self._offset = Vec(0, 0)
        self._vertex_lists = []
        self._shader = None
        self._batch = None
        self._color = None
        self._parent: 'Context' = None
        self._child_contexts = []
        self._group = None
        self.empty = True

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new: 'Context'):
        self._parent = new

    @property
    def index(self):
        if self._group:
            return self._group.order
        raise Exception('No index!')

    @index.setter
    def index(self, new):
        if self._group and self._group.order == new:
            return
        if self._group:
            self.clear()
            self.batch.invalidate()
        self._group = FuckYouGroup(self, new, self._parent._group if self._parent else None)

    @property
    def offset(self):
        return self._parent.offset + self._offset if self._parent else self._offset

    @offset.setter
    def offset(self, value):
        self._offset = Vec(value.x, - value.y)

    @property
    def batch(self):
        return self._batch if self._batch else self._parent.batch if self._parent else None

    @batch.setter
    def batch(self, value):
        self._batch = value

    @property
    def shader(self):
        return self._shader if self._shader else self._parent.shader if self._parent else None

    @shader.setter
    def shader(self, value):
        self._shader = value

    def set_state(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader.position = self.offset
        self.shader.color = self._color if self._color else Color.clear()

    def unset_state(self):
        pass

    def draw_rect(self, rect, color):
        vertexes = (rect.x, rect.y,
                    rect.x + rect.width, rect.y,
                    rect.x + rect.width, rect.y - rect.height,
                    rect.x, rect.y - rect.height)
        self._color = color
        vl = self.batch.add(4, pyglet.gl.GL_QUADS, self._group, ('v2f', vertexes))
        self._vertex_lists.append(vl)

    def draw_text(self, text, size):
        label = pyglet.text.Label(text=text, dpi=226, font_size=size, batch=self.batch, group=self._group)
        label.y -= label.content_height / 2
        self._vertex_lists.append(label)

    def clear(self):
        print('Clear', self)
        # for vl in self._vertex_lists:
        #     vl.delete()
        # self._vertex_lists = []
        # self.empty = True


class WindowContext(Context):
    def __init__(self):
        super().__init__()
        self._index = 0
        self._batch = pyglet.graphics.Batch()
        self._shader = SimpleShader()
        self._shader.bind()

    def draw(self):
        self._shader.bind()
        self._batch.draw()
