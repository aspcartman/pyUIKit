from ui.controller import *
from ui.view import *
from ui.event import *


class Window(Controller, View):
    def __init__(self):
        Controller.__init__(self)
        View.__init__(self)

        self.background_color = Color.black()
        self._needs_update = False
        self._rootController: Controller = None
        window = pyglet.window.Window(resizable=True)
        window.set_handler('on_draw', self._pyglet_on_draw)
        window.set_handler('on_resize', self._pyglet_did_resize)
        window.set_handler('on_mouse_motion', self._pyglet_on_mouse_motion)
        window.set_handler('on_mouse_press', self._pyglet_on_mouse_press)
        window.set_handler('on_mouse_release', self._pyglet_on_mouse_release)
        window.set_handler('on_mouse_drag', self._pyglet_on_mouse_drag)
        window.set_handler('on_mouse_enter', self._pyglet_on_mouse_enter)
        window.set_handler('on_mouse_leave', self._pyglet_on_mouse_leave)
        window.set_handler('on_mouse_scroll', self._pyglet_on_mouse_scroll)
        self._pygletWindow = window

    #
    # !- Pyglet Events
    #
    def _pyglet_on_draw(self):
        ctx = Context(Vec(y=self._frame.height))  # Reverting coordinate system
        self._draw(ctx)

    def _pyglet_did_resize(self, width, height):
        self.frame = Rect(0, 0, width, height)

    def _pyglet_on_mouse_motion(self, x, y, dx, dy):
        self.process_mouse_event(TouchEventType.MOVE, x, self.frame.height - y, dx, dy, None, None)

    def _pyglet_on_mouse_press(self, x, y, button, modifiers):
        self.process_mouse_event(TouchEventType.TOUCH, x, self.frame.height - y, 0, 0, button, modifiers)

    def _pyglet_on_mouse_release(self, x, y, button, modifiers):
        self.process_mouse_event(TouchEventType.RELEASE, x, self.frame.height - y, 0, 0, button, modifiers)

    def _pyglet_on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.process_mouse_event(TouchEventType.DRAG, x, self.frame.height - y, dx, dy, buttons, modifiers)

    def _pyglet_on_mouse_enter(self, x, y):
        pass

    def _pyglet_on_mouse_leave(self, x, y):
        pass

    def _pyglet_on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    @property
    def root_controller(self):
        return self._rootController

    @root_controller.setter
    def root_controller(self, value: Controller):
        if self._rootController is not None:
            self.remove_subcontroller(self._rootController)
        self.add_subcontroller(value)
        self._rootController = value

        self.add_subview(value.view)

    @property
    def view(self) -> View:
        return self

    #
    # !- Update
    #
    def set_needs_update(self):
        if not self._needs_update:
            self._needs_update = True
            pyglet.clock.schedule_once(self.update, 0)

    def update(self, dt):
        if self._needs_layout:
            self._layout()
        self._needs_update = False

    #
    # !- Layout
    #
    def set_needs_layout(self):
        super().set_needs_layout()
        self.set_needs_update()

    def layout(self):
        if self._rootController is not None:
            self._rootController.view.frame = self.bounds

    #
    # !- Events
    #
    def process_mouse_event(self, type, x, y, dx, dy, buttons, modifiers):
        view = self.hit_test(Vec(x, y))
        event = TouchEvent(type, [Touch(view, Vec(x, y))])
        self.process_event(event)

    def process_event(self, event):
        pass

    def handle_event(self, event):
        pass