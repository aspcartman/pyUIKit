import math


class Vec:
	__slots__ = ['_x', '_y']

	def __init__(self, x: float = 0, y: float = 0):
		self._x = x if x else 0
		self._y = y if y else 0

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	def length(self):
		return math.sqrt(self._x * self._x + self._y * self._y)

	def __add__(self, other):
		return Vec(self._x + other._x, self._y + other._y)

	def __sub__(self, other):
		return Vec(self._x - other._x, self._y - other._y)

	def __truediv__(self, other):
		if isinstance(other, Vec):
			return Vec(self._x / other._x, self._y / other._y)
		if isinstance(other, (float, int)):
			return Vec(self._x / other, self._y / other)

	def __str__(self):
		return "({}, {})".format(self._x, self._y)

	def __repr__(self):
		return "({}, {})".format(self._x, self._y)

	def __eq__(self, other):
		return self._x == other._x and self._y == other._y

	def __contains__(self, other):
		return 0 <= self._x - other._x <= self._x and 0 <= self._y - other._y <= self._y


class Rect:
	__slots__ = ['_origin', '_size']

	def __init__(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0, origin: Vec = None, size: Vec = None, center: Vec = None):
		if origin:
			self._origin = origin
		else:
			self._origin = Vec(x, y)

		if size:
			self._size = size
		else:
			self._size = Vec(width, height)

		if center:
			self._origin = center - self.size / 2

	def modified(self, x: float = None, y: float = None, width: float = None, height: float = None, origin: Vec = None, size: Vec = None):
		return Rect(origin=origin if origin else Vec(x, y) if x or y else self.origin, size=size if size else Vec(width, height) if width or height else self.size)

	@property
	def origin(self) -> Vec:
		return self._origin

	@property
	def size(self) -> Vec:
		return self._size

	@property
	def center(self):
		return self.origin + self.size / 2

	@property
	def x(self):
		return self._origin.x

	@property
	def y(self):
		return self._origin.y

	@property
	def width(self):
		return self._size.x

	@property
	def height(self):
		return self._size.y

	def __contains__(self, item):
		if isinstance(item, Vec):
			return self._origin in item and item in self._origin + self._size

	def __eq__(self, other):
		return self._origin == other.origin and self._size == other.size

	def __add__(self, other):
		if isinstance(other, Rect):
			return Rect(origin=self.origin + other.origin, size=self.size + other.size)
		if isinstance(other, Vec):
			return Rect(origin=self.origin + other, size=self.size)

	def __sub__(self, other):
		if isinstance(other, Rect):
			return Rect(origin=self.origin - other.origin, size=self.size - other.size)
		if isinstance(other, Vec):
			return Rect(origin=self.origin - other, size=self.size)

	def __str__(self):
		return "{},{}".format(self.origin, self.size)

	def __repr__(self):
		return "{},{}".format(self.origin, self.size)
