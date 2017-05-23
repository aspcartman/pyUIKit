from .color import Color
from .responder import Responder
from .view import View

class Controller(Responder):
    def __init__(self, view_class=View, title=None):
        super().__init__()
        self.supercontroller = None
        self.navigation_controller  = None
        self._navigation_title = None
        self.navigation_title = title
        self._view_class = view_class
        self._view = None
        self._subcontrollers = []

    #
    # !- View
    #
    @property
    def view(self):
        if self._view is None:
            view = self.load_view()
            view._controller = self
            self._view = view
            return view
        else:
            return self._view

    def load_view(self):
        view = self._view_class()
        view.background_color = Color.scheme.back()
        return view

    @property
    def is_view_loaded(self) -> bool:
        return self._view is not None

    #
    # !- SubControllers
    #
    @property
    def subcontrollers(self) -> ['Controller']:
        return list(self._subcontrollers)

    def remove_from_supercontroller(self):
        if self.supercontroller is not None:
            self.supercontroller.remove_subcontroller(self)

    def remove_subcontroller(self, controller):
        self._subcontrollers.remove(controller)

    def add_subcontroller(self, controller):
        controller.remove_from_supercontroller()
        self._subcontrollers.append(controller)
        controller.parentController = self

    #
    # !- Responder
    #
    def next_responder(self):
        return self.view.superview

    #
    # !- Navigation
    #
    @property
    def navigation_title(self):
        return self._navigation_title

    @navigation_title.setter
    def navigation_title(self, value):
        self._navigation_title = value
