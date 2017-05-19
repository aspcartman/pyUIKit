import pyglet
from ui.geom import *
from ui.graphics import Context
from ui.controller import *
from ui.view import *


class Window(Controller, View):
    def __init__(self):
        Controller.__init__(self)
        View.__init__(self)

        self.background_color = Color.black()
        self._needs_update = False
        self._rootController: Controller = None
        window = pyglet.window.Window(resizable=True)
        window.set_handler('on_draw', self.on_draw)
        window.set_handler('on_resize', self._pyglet_did_resize)
        self._pygletWindow = window

    def on_draw(self):
        ctx = Context(Vec(y=self._frame.height))
        self._draw(ctx)

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

    # !- Update

    def set_needs_update(self):
        if not self._needs_update:
            self._needs_update = True
            pyglet.clock.schedule_once(self.update, 0)

    def update(self, dt):
        if self._needs_layout:
            self._layout()
        self._needs_update = False

    # !- Layout
    def set_needs_layout(self):
        super().set_needs_layout()
        self.set_needs_update()

    def layout(self):
        if self._rootController is not None:
            self._rootController.view.frame = self.bounds

    def _pyglet_did_resize(self, width, height):
        self.frame = Rect(0, 0, width, height)
