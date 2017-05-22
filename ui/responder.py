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
        resp = self.next_responder()
        if resp:
            resp.mouse_enter(event)

    def mouse_leave(self, event: MouseEvent):
        resp = self.next_responder()
        if resp:
            resp.mouse_leave(event)

    def mouse_click(self, event: MouseEvent):
        resp = self.next_responder()
        if resp:
            resp.mouse_click(event)

    def mouse_release(self, event: MouseEvent):
        resp = self.next_responder()
        if resp:
            resp.mouse_release(event)

    def mouse_drag(self, event: MouseEvent):
        resp = self.next_responder()
        if resp:
            resp.mouse_drag(event)

    def mouse_move(self, event: MouseEvent):
        resp = self.next_responder()
        if resp:
            resp.mouse_move(event)

    def mouse_scroll(self, event: MouseEvent):
        resp = self.next_responder()
        if resp:
            resp.mouse_scroll(event)
