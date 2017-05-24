from typing import List

from graphics import Context
from .animation import Animator, lerp
from .color import Color
from .geom import Rect, Vec
from .responder import Responder


class View(Responder):
    def __init__(self, frame=None, origin=None, size=None, controller=None):
        super().__init__()
        self._background_color = Color.scheme.front()
        if origin or size:
            self._frame = Rect(origin=origin, size=size)
        else:
            self._frame = frame if frame else Rect()
        self._subviews = []
        self._superview = None
        self._needs_layout = True
        self._needs_draw = True
        self._controller = None
        self._ctx = None

    def __str__(self):
        return '{} {}'.format(self.__class__.__name__, self._frame)

    #
    # !- Animations
    #
    animator = Animator()

    # noinspection PyPep8Naming
    class animatable:
        def __init__(self, prop):
            self.prop = prop

        def generate_animated_setter(self, getter, setter):
            def set_animated(self, new):
                if View.animator.in_animation():
                    old = getter(self)
                    if old != new:
                        def animate(t):
                            setter(self, lerp(t, old, new))

                        View.animator.add(animate)
                    else:
                        setter(self, new)
                else:
                    setter(self, new)

            return set_animated

        def setter(self, f) -> property:
            return self.prop.setter(self.generate_animated_setter(self.prop.fget, f))

    #
    # !- Frame
    #
    @animatable
    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        old = self._frame
        self._frame = value
        if old.size != value.size:
            self.set_needs_layout()

    @property
    def bounds(self):
        return Rect(size=self._frame.size)

    #
    # !- Hierarchy
    #
    @property
    def subviews(self) -> List['View']:
        return list(self._subviews)

    @property
    def superview(self) -> ['View']:
        return self._superview

    @superview.setter
    def superview(self, value):
        self._superview = value

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = value
        self.set_needs_redraw()

    def superviews(self, include_self=False):
        current = self if include_self else self.superview
        while current is not None:
            yield current
            current = current.superview

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
        if view._ctx:
            view._ctx.clear()

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
        if not view:
            return None
        mine = set(self.superviews(include_self=True))
        for sv in view.superviews(include_self=True):
            if sv in mine:
                return sv
        return None

    #
    # !- Sizing
    #
    def preferred_size(self):
        return Vec(0, 0)

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
    def set_needs_redraw(self):
        self._needs_draw = True

    def _draw(self, ctx: Context, deep):
        if not self._ctx or self._ctx.parent is not ctx or self._ctx.index != deep:
            if not self._ctx:
                self._ctx = Context(ctx, deep)
            self._needs_draw = True
        print(self, self._ctx)
        self._ctx.offset = self.frame.origin
        if self._needs_draw:
            self._ctx.clear()
            self.draw(self._ctx)
            self._needs_draw = False
        for sv in self.subviews:
            deep += 1
            sv._draw(self._ctx, deep)

    def draw(self, ctx: Context):
        ctx.draw_rect(Rect(size=self.frame.size), self.background_color)
        pass

    #
    # !- Hit Test
    #
    def hit_test(self, point: Vec) -> ['View']:
        if not self.point_inside(point):
            return None
        for sv in reversed(self._subviews):
            v = sv.hit_test(point - sv.frame.origin)
            if v is not None:
                return v
        return self

    def point_inside(self, point) -> bool:
        return point in self.frame.size

    def convert_from(self, view, point):
        return view.convert_to(self, point)

    def convert_to(self, view, point):
        super_view = self.first_common_superview(view)
        if super_view is None:
            return None
        for sv in self.superviews(include_self=True):
            point += sv.frame.origin
            if sv == super_view:
                break
        for sv in view.superviews(include_self=True):
            point -= sv.frame.origin
            if sv == super_view:
                break
        return point

    #
    # !- Responder Chain
    #
    def next_responder(self):
        if self._controller is not None:
            return self._controller
        return self.superview
