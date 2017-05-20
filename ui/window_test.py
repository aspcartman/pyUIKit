from .controller import Controller
from .geom import Rect
from .view import View
from .window import Window


class TestWindow:
    def test_event_handling(self):
        class MyView(View):
            def handle_event(s, event):
                self.catch = True
                return True

        window = Window(real_window=False, root=Controller(view_class=MyView))
        window.frame = Rect(0, 0, 100, 100)
        window.process_mouse_event(None, 10, 10, 0, 0, None, None)
        assert self.catch is not None
