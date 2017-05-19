import pyglet
from ui.geom import *
from ui.color import Color
from ui.graphics import Context
from typing import Iterable


class View:
    def __init__(self, frame=Rect()):
        self.background_color = Color.white()
        self._frame = frame
        self._bounds = Rect(size=frame.size)
        self._subviews = []
        self._superview = None
        self._needs_layout = True
        self._needs_draw = True

    # !- Frame & Bounds
    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value
        self.bounds = Rect(origin=self._bounds.origin, size=value.size)

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, value):
        if self._bounds.size != value.size:
            self.set_needs_layout()
        self._bounds = value

    # !- Subviews
    @property
    def subviews(self) -> Iterable['View']:
        return list(self._subviews)

    @property
    def superview(self) -> ['View']:
        return self._superview

    @superview.setter
    def superview(self, value):
        self._superview = value

    def add_subview(self, view):
        view.remove_from_superview()
        self._subviews.append(view)
        view.superview = self

    def insert_subview(self, i, view):
        view.remove_from_superview()
        self._subviews.insert(i, view)
        view.superview = self

    def remove_subview(self, view):
        self._subviews.remove(view)
        view.superview = None

    def remove_from_superview(self):
        if self.superview is not None:
            self.superview.remove_subview(self)

    def move_subview_to_back(self, subview):
        self._subviews.remove(subview)
        self._subviews.insert(0, subview)

    def move_subview_to_front(self, subview):
        self._subviews.remove(subview)
        self._subviews.append(subview)

    # !- Sizing
    def preferred_size(self):
        return Vec()

    # !- Layout
    def set_needs_layout(self):
        self._needs_layout = True
        if self.superview is not None:
            self.superview.set_needs_layout()

    def _layout(self):
        self._needs_layout = False
        self.layout()
        for sv in self.subviews:
            if sv._needs_layout:
                sv._layout()

    def layout(self):
        pass

    # !- Drawing
    def _draw(self, ctx: Context):
        ctx.draw_rect(self.bounds, self.background_color)
        self._needs_draw = False
        self.draw(ctx)
        for sv in self.subviews:
            sv_ctx = ctx.new_subcontext(sv.frame.origin)
            sv._draw(sv_ctx)

    def draw(self, ctx: Context):
        pass
