import math


def outbound(x, bound):
    if x > bound:
        return x - bound
    if x < 0:
        return x
    return 0


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

    def modified(self, x: float = None, y: float = None):
        return Vec(x if x else self._x, y if y else self._y)

    def miss(self, other):
        return Vec(outbound(self.x, other.x), outbound(self.y, other.y))

    def __add__(self, other):
        return Vec(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        return Vec(self._x - other._x, self._y - other._y)

    def __neg__(self):
        return Vec(-self._x, -self._y)

    def __mul__(self, other):
        if isinstance(other, Vec):
            return Vec(self._x * other._x, self._y * other._y)
        if isinstance(other, (int, float, complex)):
            return Vec(self._x * other, self._y * other)

    def __truediv__(self, other):
        if isinstance(other, Vec):
            return Vec(self._x / other._x, self._y / other._y)
        if isinstance(other, (int, float, complex)):
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

    def __init__(self, x: float = None, y: float = None, width: float = None, height: float = None, origin: Vec = None,
                 size: Vec = None, center: Vec = None):
        if origin:
            self._origin = origin
        else:
            self._origin = Vec(x if x else 0, y if y else 0)

        if size:
            self._size = size
        else:
            self._size = Vec(width if width else 0, height if height else 0)

        if center:
            self._origin = center - self.size / 2

    def modified(self, x: float = None, y: float = None, width: float = None, height: float = None, origin: Vec = None,
                 size: Vec = None, center: Vec = None):
        return Rect(origin=origin if origin else Vec(x, y) if x or y else self.origin,
                    size=size if size else Vec(width, height) if width or height else self.size, center=center)

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

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Rect(origin=self.origin * other, size=self.size * other)

    def __str__(self):
        return "{},{}".format(self.origin, self.size)

    def __repr__(self):
        return "{},{}".format(self.origin, self.size)
