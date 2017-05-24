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

        scroll = ui.ScrollView(ui.Rect(100, 100, 300, 300))
        scroll.content_size = ui.Vec(300, 10000)
        scroll._content_view.background_color = ui.Color.scheme.back().with_alpha(0.5)
        self.add_subview(scroll)
        self._scroll = scroll

        button = ui.Button(title="Push")
        button.action = lambda x: self._controller.push(x)
        scroll.add_subview(button)
        self.push = button

        button = ui.Button(title="Pop")
        button.action = lambda x: self._controller.pop(x)
        scroll.add_subview(button)
        self.pop = button

    def layout(self):
        self.pop.frame = ui.Rect(origin=ui.Vec(50, 100), size=self.pop.preferred_size())
        self.push.frame = ui.Rect(origin=ui.Vec(150, 100), size=self.push.preferred_size())


window = ui.Window()
window.root_controller = ui.NavigationController(MainController())
pyglet.app.run()
