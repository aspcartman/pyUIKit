from unittest.mock import MagicMock

from .controller import Controller
from .event import MouseEvent
from .geom import Rect, Vec
from .window import Window


class TestWindow:
	def test_event_handling(self):
		vc = Controller()
		v = vc.view
		v.mouse_click = MagicMock()
		window = Window(real_window=False, root=vc)
		window.frame = Rect(0, 0, 100, 100)
		window.process_mouse_event(MouseEvent.TOUCH, Vec(10, 10))
		v.mouse_click.assert_called()
