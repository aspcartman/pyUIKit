import pyglet
import ui
from pyglet.gl import *

class MainController(ui.Controller):
    def load_view(self):
        return MyView()


class MyView(ui.View):
    def __init__(self, frame=ui.Rect()):
        super().__init__(frame)

        self.background_color = ui.Color.blue()
        subview = ui.View(ui.Rect(0, 0, 20, 20))
        subview.background_color = ui.Color.red()
        self._subview = subview
        self.add_subview(subview)

    def layout(self):
        self._subview.frame.origin = self.bounds.size - self._subview.bounds.size

window = ui.Window()
window.root_controller = ui.NavigationController(MainController())
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
pyglet.app.run()