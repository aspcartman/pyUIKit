from .geom import Vec


class Event:
    pass


class MouseEvent(Event):
    MOVE = 0
    TOUCH = 1
    DRAG = 2
    RELEASE = 3
    SCROLL = 4

    def __init__(self, event_type, view, location, delta=Vec(), buttons=None, modifiers=None):
        super().__init__()
        self.type = event_type
        self.view = view
        self.location = location
        self.delta = delta
        self.buttons = buttons
        self.modifiers = modifiers

    def location_in_view(self, view):
        return self.view.convert_to(view, self.location)
