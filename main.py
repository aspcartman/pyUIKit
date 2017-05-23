import random

from pyglet.gl import *

import ui


class MainController(ui.Controller):
    def __init__(self):
        super().__init__(view_class=MyView, title="lol")
        self.toggle = False

    def push(self, btn):
        self.navigation_controller.push(MainController())

    def pop(self, btn):
        self.navigation_controller.pop()


class MyView(ui.View):
    def __init__(self, frame=ui.Rect()):
        super().__init__(frame)

        scroll = ui.ScrollView(ui.Rect(0, 0, 300, 300))
        self.add_subview(scroll)
        self._scroll = scroll

        button = ui.Button(title="Push")
        button.action = lambda x: self._controller.push(x)
        self.add_subview(button)
        self.push = button

        button = ui.Button(title="Pop")
        button.action = lambda x: self._controller.pop(x)
        self.add_subview(button)
        self.pop = button

    def layout(self):
        self.push.frame = ui.Rect(origin=ui.Vec(50, 300), size=self.push.preferred_size())
        self.pop.frame = ui.Rect(origin=ui.Vec(300, 300), size=self.pop.preferred_size())


window = ui.Window()
window.root_controller = ui.NavigationController(MainController())
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
pyglet.app.run()
