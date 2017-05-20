from ui.geom import *
from typing import List


class Event:
    pass


class Touch:
    def __init__(self, view, location):
        self.view = view
        self.location = location

    def location_in_view(self, view):
        return self.view.convert_to(view, self.location)


class TouchEventType:
    MOVE = 0
    TOUCH = 1
    DRAG = 2
    RELEASE = 3


class TouchEvent(Event):
    def __init__(self, event_type: TouchEventType, touches: List[Touch]):
        super().__init__()
        self.type = event_type
        self.touches = touches
