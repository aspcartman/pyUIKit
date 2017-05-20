from ui.color import Color
from ui.controller import Controller
from ui.geom import *
from ui.view import View
from .label import Label


class NavigationController(Controller):
	def __init__(self, root=None):
		super().__init__()
		self._root = None
		if root is not None:
			self.root = root

	@property
	def root(self):
		return self._root

	@root.setter
	def root(self, value: [Controller]):
		for c in self.subcontrollers:
			self.remove_subcontroller(c)
		self.add_subcontroller(value)
		self.view.content_view = value.view

	@property
	def view(self) -> 'NavigationView':
		return super().view

	def load_view(self):
		return NavigationView()


class NavigationView(View):
	def __init__(self, frame=Rect()):
		super().__init__(frame)
		self._content_view = None

		bar = NavigationBar()
		bar.title_label.text = "Testing"
		self.add_subview(bar)
		self.bar = bar

	def layout(self):
		super().layout()
		if self._content_view is not None:
			self._content_view.frame = Rect(size=self.frame.size)
		self.bar.frame = Rect(size=Vec(self.frame.width, self.bar.preferred_size().y))

	@property
	def content_view(self) -> View:
		return self._content_view

	@content_view.setter
	def content_view(self, value):
		if self._content_view is not None:
			self.remove_subview(self._content_view)
		self.insert_subview(0, value)
		self._content_view = value
		self.set_needs_layout()


class NavigationBar(View):
	def __init__(self, frame=Rect()):
		super().__init__(frame)
		self.background_color = Color.scheme.warn().with_alpha(250)
		self.title_label = Label()
		self.add_subview(self.title_label)

	def preferred_size(self):
		return Vec(-1, 60)

	def layout(self):
		self.title_label.frame = Rect(size=self.title_label.preferred_size(), center=self.frame.size / 2)
