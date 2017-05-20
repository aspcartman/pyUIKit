# from ui.geom import *
from ui.view import *


class TestView:
	def test_hit_test(self):
		v1 = View(frame=Rect(10, 10, 100, 100))
		v1.bounds = Rect(10, 10, 100, 100)
		v2 = View(frame=Rect(10, 10, 100, 100))
		v1.add_subview(v2)
		v3 = View(frame=Rect(10, 10, 100, 100))
		v2.add_subview(v3)

		assert v1.hit_test(Vec(-1, -1)) is None
		assert v1.hit_test(Vec(0, 0)) == v1
		assert v1.hit_test(Vec(5, 5)) == v1
		assert v1.hit_test(Vec(10, 10)) == v2
		assert v1.hit_test(Vec(12, 12)) == v2
		assert v1.hit_test(Vec(22, 22)) == v3

	def test_view_superviews(self):
		v1 = View()
		v2 = View()
		v3 = View()

		v1.add_subview(v2)
		v2.add_subview(v3)

		assert list(v3.superviews()) == [v2, v1]
		assert list(v3.superviews(include_self=False)) == [v2, v1]
		assert list(v3.superviews(include_self=True)) == [v3, v2, v1]

	def test_common_superview(self):
		v1 = View()
		v2 = View()
		v3 = View()
		v4 = View()
		v5 = View()
		v6 = View()

		v1.add_subview(v2)
		v2.add_subview(v3)
		v2.add_subview(v4)
		v3.add_subview(v5)

		assert v1.first_common_superview(v2) == v1
		assert v1.first_common_superview(v3) == v1
		assert v1.first_common_superview(v4) == v1
		assert v1.first_common_superview(v5) == v1
		assert v1.first_common_superview(v6) is None
		assert v2.first_common_superview(v3) == v2
		assert v3.first_common_superview(v5) == v3
		assert v3.first_common_superview(v4) == v2

	def test_point_convertion(self):
		v1 = View(frame=Rect(0, 0, 100, 100))
		v2 = View(frame=Rect(10, 10, 100, 100))
		v3 = View(frame=Rect(10, 10, 100, 100))
		v3._bounds.origin = Vec(0, -100)

		v1.add_subview(v2)
		v2.add_subview(v3)

		assert v3.convert_to(v1, Vec(0, 100)) == Vec(20, 20)

	def test_next_responder(self):
		v1 = View()
		v2 = View()
		v1.add_subview(v2)

		assert v2.next_responder() == v1
