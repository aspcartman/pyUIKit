from pyglet.gl import *

import ui


class MainController(ui.Controller):
	def load_view(self):
		return MyView()


class MyView(ui.View):
	def __init__(self, frame=ui.Rect()):
		super().__init__(frame)
		self.background_color = ui.Color.blue()

		scroll = ui.ScrollView(ui.Rect(0, 0, 300, 300))
		scroll.background_color = ui.Color.green()
		self.add_subview(scroll)

		subview = ui.View(ui.Rect(100, 100, 20, 20))
		subview.background_color = ui.Color.red()
		scroll.add_subview(subview)
		self._subview = subview


window = ui.Window()
window.root_controller = ui.NavigationController(MainController())
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
pyglet.app.run()
