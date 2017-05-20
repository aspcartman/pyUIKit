import pyglet

from graphics import Context
from .color import Color
from .controller import Controller
from .event import MouseEvent
from .geom import Rect, Vec
from .view import View


class Window(Controller, View):
	def __init__(self, root: Controller = None, real_window=True):
		Controller.__init__(self)
		View.__init__(self)

		self.first_responder = None
		self.background_color = Color.black()
		self._needs_update = False
		self._root_controller = None
		self._view = self
		if root is not None:
			self.root_controller = root
		if real_window:
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
			self._pyglet_window = window
		else:
			self._pyglet_window = None

	#
	# !- Pyglet Events
	#
	def _pyglet_on_draw(self):
		ctx = Context(Vec(y=self._frame.height))  # Reverting coordinate system
		self._draw(ctx)

	def _pyglet_did_resize(self, width, height):
		self.frame = Rect(0, 0, width, height)

	def _pyglet_on_mouse_motion(self, x, y, dx, dy):
		self.process_mouse_event(MouseEvent.MOVE, Vec(x, self.frame.height - y), delta=Vec(dx, dy))

	def _pyglet_on_mouse_press(self, x, y, button, modifiers):
		self.process_mouse_event(MouseEvent.TOUCH, Vec(x, self.frame.height - y), buttons=[button], modifiers=modifiers)

	def _pyglet_on_mouse_release(self, x, y, button, modifiers):
		self.process_mouse_event(MouseEvent.RELEASE, Vec(x, self.frame.height - y), buttons=[button], modifiers=modifiers)

	def _pyglet_on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.process_mouse_event(MouseEvent.DRAG, Vec(x, self.frame.height - y), delta=Vec(dx, dy), buttons=buttons, modifiers=modifiers)

	def _pyglet_on_mouse_enter(self, x, y):
		pass

	def _pyglet_on_mouse_leave(self, x, y):
		pass

	def _pyglet_on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		self.process_mouse_event(MouseEvent.SCROLL, Vec(x, self.frame.height - y), delta=Vec(scroll_x, scroll_y))
		pass

	@property
	def root_controller(self):
		return self._root_controller

	@root_controller.setter
	def root_controller(self, value: Controller):
		if self._root_controller is not None:
			self.remove_subcontroller(self._root_controller)
		self.add_subcontroller(value)
		self._root_controller = value

		self.add_subview(value.view)

	#
	# !- Update
	#
	def set_needs_update(self):
		if self._pyglet_window is None:
			self.update(0)
			return
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
		if self._root_controller is not None:
			self._root_controller.view.frame = Rect(size=self.frame.size)

	#
	# !- Events
	#
	def process_mouse_event(self, type, location, delta=None, buttons=None, modifiers=None):
		view = self.hit_test(location)
		if view is None:
			return
		event = MouseEvent(type, view, self.convert_to(view, location), delta=delta)
		while view is not None and not view.handle_event(event):
			view = view.next_responder()

	def process_event(self, event):
		pass

	def handle_event(self, event):
		pass

	# print('Unhandled event', event)

	#
	# !- Responder
	#
	def next_responder(self):
		return None
