from .view import View
from .controller import Controller
from .window import Window
from .geom import Rect

class TestWindow:
    def test_event_handling(self):
        catch = None

        class MyView(View):
            def handle_event(self, event):
                global catch
                catch = event
                return True

        window = Window(real_window=False, root=Controller(view_class=MyView))
        window.frame = Rect(0,0,100,100)
        window.process_mouse_event(None, 10, 10, 0, 0, None, None)
        assert catch is not None
