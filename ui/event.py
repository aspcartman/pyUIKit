from .geom import Vec


class Event:
	pass


class MouseEventType:
	MOVE = 0
	TOUCH = 1
	DRAG = 2
	RELEASE = 3
	SCROLL = 4


class MouseEvent(Event):
	def __init__(self, event_type, view, location, delta=Vec()):
		super().__init__()
		self.type = event_type
		self.view = view
		self.location = location

	def location_in_view(self, view):
		return self.view.convert_to(view, self.location)
