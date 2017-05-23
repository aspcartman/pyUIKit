from ui.color import Color
from ui.controller import Controller
from ui.geom import *
from ui.view import View
from .label import Label


class NavigationController(Controller):
    def __init__(self, root=None):
        super().__init__(view_class=NavigationView)
        self._root = None
        if root is not None:
            self.root = root

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value: [Controller]):
        for c in self.subcontrollers:
            self.remove_subcontroller(c)
        self.add_subcontroller(value)
        self.push(value, animated=False)

    def add_subcontroller(self, controller):
        super().add_subcontroller(controller)
        controller.navigation_controller = self

    def remove_subcontroller(self, controller):
        super().remove_subcontroller(controller)
        controller.navigation_controller = None

    def push(self, controller, animated=True):
        self.add_subcontroller(controller)
        self.view.push_to(controller.view, animated)

    def pop(self, animated=True):
        self.remove_subcontroller(self._subcontrollers[-1])
        self.view.pop_to(self.subcontrollers[-1].view, animated)

    @property
    def view(self) -> 'NavigationView':
        return super().view


class NavigationView(View):
    def __init__(self, frame=Rect()):
        super().__init__(frame)
        self._back_view = None
        self._front_view = None
        self._right_view = None

        bar = NavigationBar()
        bar.title_label.text = "Testing"
        self.add_subview(bar)
        self.bar = bar

    def layout(self):
        super().layout()
        if self._back_view is not None:
            self.move_subview_to_front(self._back_view)
            self._back_view.frame = self.bounds.modified(x=-self.bounds.width / 6)
        if self._front_view is not None:
            self.move_subview_to_front(self._front_view)
            self._front_view.frame = self.bounds
        if self._right_view is not None:
            self.move_subview_to_front(self._right_view)
            self._right_view.frame = self.bounds.modified(x=self.bounds.width)
        self.move_subview_to_front(self.bar)
        self.bar.frame = Rect(size=Vec(self.frame.width, self.bar.preferred_size().y))

    def push_to(self, view, animated):
        self.add_subview(view)
        self._right_view = view
        if animated:
            self.layout()
            View.animator.begin()

        self._back_view, self._front_view, self._right_view = self._front_view, self._right_view, None
        self.layout()

        if animated:
            View.animator.commit(self.finished)
        else:
            self.finished()

    def pop_to(self, view, animated):
        self.add_subview(view)
        self._back_view = view
        if animated:
            self.layout()
            View.animator.begin()

        self._back_view, self._front_view, self._right_view = None, self._back_view, self._front_view
        self.layout()

        if animated:
            View.animator.commit(self.finished)
        else:
            self.finished()

    def finished(self):
        if self._back_view:
            self.remove_subview(self._back_view)
            self._back_view = None
        if self._right_view:
            self.remove_subview(self._right_view)
            self._right_view = None

    @property
    def title(self):
        return self.bar.title_label.text

    @title.setter
    def title(self, text):
        self.bar.title_label.text = text


class NavigationBar(View):
    def __init__(self, frame=Rect()):
        super().__init__(frame)
        self.background_color = Color.scheme.warn().with_alpha(200)
        self.title_label = Label()
        self.add_subview(self.title_label)

    def preferred_size(self):
        return Vec(-1, 60)

    def layout(self):
        self.title_label.frame = Rect(size=self.title_label.preferred_size(), center=self.frame.size / 2)
