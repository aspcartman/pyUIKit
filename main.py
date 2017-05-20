from pyglet.gl import *

import ui


class MainController(ui.Controller):
	def __init__(self):
		super().__init__(view_class=MyView, title="lol")


class MyView(ui.View):
	def __init__(self, frame=ui.Rect()):
		super().__init__(frame)

		scroll = ui.ScrollView(ui.Rect(0, 0, 300, 300))
		self.add_subview(scroll)
		self._scroll = scroll

		subview = ui.View(ui.Rect(100, 100, 20, 20))
		subview.background_color = ui.Color.scheme.tint()
		scroll.add_subview(subview)
		self._subview = subview

		for i in range(0, 10):
			scroll.add_subview(ui.Label(text="Testing this shit"))

	def layout(self):
		off = 0
		for l in self._scroll.content.subviews[1:]:
			l.frame = l.frame.modified(y=off, size=l.preferred_size())
			off += l.preferred_size().y


window = ui.Window()
window.root_controller = ui.NavigationController(MainController())
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
pyglet.app.run()
