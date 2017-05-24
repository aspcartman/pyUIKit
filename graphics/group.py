import pyglet


class FuckYouGroup(pyglet.graphics.OrderedGroup):
    def __init__(self, ctx, order, parent=None):
        super().__init__(order, parent)
        self._ctx = ctx

    def set_state(self):
        self._ctx.set_state()

    def unset_state(self):
        self._ctx.unset_state()
