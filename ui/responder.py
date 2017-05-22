from .event import MouseEvent


class Responder:
	def __init__(self):
		super().__init__()
		self._is_first_responder = False

	@property
	def window(self):
		responder = self
		while responder is not None and responder.__class__.__name__ != 'Window':
			responder = responder.next_responder()
		return responder

	def next_responder(self) -> ['Responder']:
		return None

	def can_become_first_responder(self) -> bool:
		return False

	def become_first_responder(self):
		if self._is_first_responder:
			return True

		if not self.can_become_first_responder():
			return False

		window = self.window
		if window is None:
			return False

		if window.first_responder is not None:
			if not window.first_responder.resign_first_responder():
				return False

		window.first_responder = self

	def resign_first_responder(self):
		if not self._is_first_responder:
			return True

		window = self.window
		if window is None:
			return True

		self.window.first_responder = None
		return True

	def mouse_enter(self, event: MouseEvent):
		return self.next_responder()

	def mouse_leave(self, event: MouseEvent):
		return self.next_responder()

	def mouse_click(self, event: MouseEvent):
		return self.next_responder()

	def mouse_release(self, event: MouseEvent):
		return self.next_responder()

	def mouse_drag(self, event: MouseEvent):
		return self.next_responder()

	def mouse_move(self, event: MouseEvent):
		return self.next_responder()

	def mouse_scroll(self, event: MouseEvent):
		return self.next_responder()
