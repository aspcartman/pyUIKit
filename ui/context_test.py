import pyglet

from .color import Color
from .context import Context
from .geom import Rect


class TestContext:
    def test_detach(self):
        batch = pyglet.graphics.Batch()
        root = Context(None)
        root.batch = batch
        root.set_parent_and_index(None, 0)
        root.draw_rect(Rect(), Color())

        assert len(root._vertex_lists) == 1
        assert len(batch.group_map) == 1

        root.detach()

        assert len(root._vertex_lists) == 0
        assert batch._draw_list_dirty

        batch._update_draw_list()
        assert len(batch.group_map) == 0

    def test_detach_label(self):
        batch = pyglet.graphics.Batch()
        root = Context(None)
        root.batch = batch
        root.set_parent_and_index(None, 0)
        root.draw_text('text', 10)

        assert len(root._vertex_lists) == 1
        assert len(batch.group_map) > 0

        root.detach()

        assert len(root._vertex_lists) == 0
        assert batch._draw_list_dirty

        batch._update_draw_list()
        assert len(batch.group_map) == 0

    def test_change_root(self):
        batch = pyglet.graphics.Batch()
        root = Context(None)
        root.batch = batch
        root.set_parent_and_index(None, 0)
        root.draw_rect(Rect(), Color())

        assert len(root._vertex_lists) == 1
        assert len(batch.group_map) == 1

        root.detach()

        assert len(root._vertex_lists) == 0
        assert batch._draw_list_dirty

        batch._update_draw_list()
        assert len(batch.group_map) == 0
