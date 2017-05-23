import random

from pyglet.gl import *

import ui


class MainController(ui.Controller):
    def __init__(self):
        super().__init__(view_class=MyView, title="lol")
        self.toggle = False

    def btn(self, btn):
        ui.View.animator.begin()
        if self.toggle:
            self.view.layout()
        else:
            btn.frame = ui.Rect(0, 0, 500, 500)
        ui.View.animator.commit()
        self.toggle = not self.toggle


class MyView(ui.View):
    def __init__(self, frame=ui.Rect()):
        super().__init__(frame)

        scroll = ui.ScrollView(ui.Rect(0, 0, 300, 300))
        self.add_subview(scroll)
        self._scroll = scroll

        button = ui.Button(title="I'm the button, bitches!", origin=ui.Vec(200, 200))
        button.action = lambda x: self._controller.btn(x)
        self.add_subview(button)
        self._button = button

        for i in range(0, 10):
            scroll.add_subview(ui.Label(text="Testing this shit"))

    def layout(self):
        off = 0
        for l in self._scroll.content.subviews[1:]:
            l.frame = l.frame.modified(y=off, size=l.preferred_size())
            off += l.preferred_size().y
        size = self._button.preferred_size()
        origin = ui.Vec(self.frame.center.x, self.frame.height - size.y - 30)
        self._button.frame = self._button.frame.modified(center=origin, size=size)


window = ui.Window()
window.root_controller = ui.NavigationController(MainController())
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
pyglet.app.run()
