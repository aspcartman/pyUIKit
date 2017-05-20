from pyglet.gl import *

import ui


class MainController(ui.Controller):
    def load_view(self):
        return MyView()


class MyView(ui.View):
    def __init__(self, frame=ui.Rect()):
        super().__init__(frame)

        self.background_color = ui.Color.blue()
        subview = ui.View(ui.Rect(100, 100, 20, 20))
        subview.background_color = ui.Color.red()
        self._subview = subview
        self.add_subview(subview)

    def handle_event(self, event):
        if isinstance(event, ui.MouseEvent):
            self._subview.frame.origin = event.location_in_view(self)
        return True


window = ui.Window()
window.root_controller = ui.NavigationController(MainController())
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
pyglet.app.run()
