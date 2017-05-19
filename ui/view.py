import pyglet
from ui.geom import *
from ui.color import Color
from ui.graphics import Context
from typing import List, Iterator, TypeVar


class View:
    def __init__(self, frame=Rect()):
        self.background_color = Color.white()
        self._frame = frame
        self._bounds = Rect(size=frame.size)
        self._subviews: List[View] = []
        self._superview = None
        self._needs_layout = True
        self._needs_draw = True

    def __str__(self):
        return '{} {}'.format(self.__class__.__name__, self._frame)

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

    #
    # !- Hierarchy
    #
    @property
    def subviews(self) -> List['View']:
        return list(self._subviews)

    @property
    def superview(self) -> ['View']:
        return self._superview

    def superviews(self) -> Iterator['View']:
        current = self.superview
        while current is not None:
            yield current
            current = current.superview

    def traverse_view_chain(self):
        current = self
        while current is not None:
            yield current
            current = current.superview

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

    def first_common_superview(self, view) -> ['View']:  # Needs optimizations
        mine = set(self.traverse_view_chain())
        for sv in view.traverse_view_chain():
            if sv in mine:
                return sv
        return None

    #
    # !- Sizing
    #
    def preferred_size(self):
        return Vec()

    #
    # !- Layout
    #
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

    #
    # !- Drawing
    #
    def _draw(self, ctx: Context):
        ctx.draw_rect(self.bounds, self.background_color)
        self._needs_draw = False
        self.draw(ctx)
        for sv in self.subviews:
            sv_ctx = ctx.new_subcontext(sv.frame.origin)
            sv._draw(sv_ctx)

    def draw(self, ctx: Context):
        pass

    #
    # !- Events
    #
    def hit_test(self, point: Vec) -> ['View']:
        if not self.point_inside(point):
            return None
        for sv in reversed(self._subviews):
            v = sv.hit_test(point - sv.frame.origin - sv.bounds.origin)
            if v is not None:
                return v
        return self

    def point_inside(self, point) -> bool:
        return self.bounds.origin + point in self.bounds

    def convert_from(self, view, point):
        return view.convert_to(self, point)

    def convert_to(self, view, point):
        super_view = self.first_common_superview(view)
        if super_view is None:
            return None
        for sv in self.traverse_view_chain():
            point += sv.bounds.origin + sv.frame.origin
            if sv == super_view:
                break
        for sv in view.traverse_view_chain():
            point -= sv.bounds.origin + sv.frame.origin
            if sv == super_view:
                break
        return point

    #
    # !- Responder Chain
    #
    def become_first_responder(self):
        pass

    def resign_first_responder(self):
        pass
