from ui.geom import *


class TestVec:
	def test_comparing(self):
		assert Vec(1, 1) == Vec(1, 1)
		assert Vec(0, 0) == Vec(0, 0)
		assert Vec() == Vec()

	def test_math(self):
		assert Vec(1, 1) + Vec(-3, -4) == Vec(-2, -3)
		assert Vec(1, 2) - Vec(1, 2) == Vec(0, 0)

	def test_in(self):
		assert Vec(1, 1) in Vec(2, 2)
		assert Vec(2, 2) not in Vec(1, 1)
		assert Vec(-1, -1) not in Vec(1, 1)
		assert Vec(1, 2) not in Vec(1, 1)
		assert Vec(2, 1) not in Vec(1, 1)


class TestRect:
	def test_comparing(self):
		assert Rect() == Rect()
		assert Rect(1, 2, 3, 4) == Rect(1, 2, 3, 4)

	def test_in(self):
		assert Vec(0, 0) in Rect()
		assert Vec(1, 1) in Rect(0, 0, 1, 1)
		assert Vec(-1, -1) not in Rect(0, 0, 1, 1)
		assert Vec(2, 1) not in Rect(0, 0, 1, 1)
