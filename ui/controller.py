from ui.view import View
from typing import Type


class Controller:
    def __init__(self):
        self.supercontroller = None
        self.navigation_controller = None
        self._view = None
        self._subcontrollers = []

    @property
    def view(self) -> [View]:
        if self._view is None:
            view = self.load_view()
            self._view = view
            return view
        else:
            return self._view

    def load_view(self) -> View:
        return View()

    @property
    def is_view_loaded(self) -> bool:
        return self._view is not None

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
