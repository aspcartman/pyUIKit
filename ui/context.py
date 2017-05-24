import pyglet
from pyglet.gl import *

from .color import Color
from .geom import Vec
from .group import FuckYouGroup
from .shader import SimpleShader


class Context:
    def __init__(self, view):
        super().__init__()
        self._view = view
        self._offset = Vec(0, 0)
        self._shader = None
        self._batch = None
        self._color = None
        self._parent: 'Context' = None
        self._parent_group = None
        self._vertex_lists = []
        self._child_contexts = []
        self._group = None
        self.empty = True

    @property
    def parent(self):
        return self._parent

    @property
    def index(self):
        if self._group:
            return self._group.order
        raise Exception('No index!')

    def set_parent_and_index(self, parent: Context, index):
        if self._parent is parent and self._parent_group == parent._group if parent else None and self._group and self._group.order == index:
            return

        if self._parent:
            self.detach()
        if parent:
            print('Attaching', self._view)
            self._parent = parent
            self._batch = parent._batch
            self._parent_group = parent._group
            parent._child_contexts.append(self)
        self._group = FuckYouGroup(self, index, parent._group if parent else None)

    @property
    def offset(self):
        return self._parent.offset + self._offset if self._parent else self._offset

    @offset.setter
    def offset(self, value):
        self._offset = Vec(value.x, - value.y)

    @property
    def batch(self):
        return self._batch

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
        try:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            self.shader.position = self.offset
            self.shader.color = self._color if self._color else Color.clear()
        except (Exception) as e:
            print('It blow up again')
            pass

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

    def detach(self):
        print('Detaching', self._view)
        self.clear()
        self._group = None
        self._parent = None
        self._parent_group = None
        if self._batch:
            self._batch.invalidate()
        self._batch = None
        for c in self._child_contexts:
            c.detach()
        self._child_contexts = []

    def clear(self):
        for vl in self._vertex_lists:
            vl.delete()
        self._vertex_lists = []
        self.empty = True


class WindowContext(Context):
    def __init__(self, view):
        super().__init__(view)
        self._index = 0
        self._batch = pyglet.graphics.Batch()
        self._shader = SimpleShader()

    def draw(self):
        self._shader.bind()
        self._batch.draw()
