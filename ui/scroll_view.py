from .color import Color
from .event import MouseEvent
from .geom import Rect, Vec
from .view import View


class ScrollView(View):
	def __init__(self, frame=Rect()):
		super().__init__(frame)
		content_view = View()
		content_view.background_color = Color.clear()
		super().add_subview(content_view)
		self._content_view = content_view

	@property
	def content(self):
		return self._content_view

	def add_subview(self, view):
		self._content_view.add_subview(view)

	def layout(self):
		self._content_view.frame = self._content_view.frame.modified(size=self.frame.size)

	def handle_event(self, event):
		if isinstance(event, MouseEvent):
			if event.type == MouseEvent.SCROLL:
				self._content_view.frame += Vec(event.delta.x, -event.delta.y)