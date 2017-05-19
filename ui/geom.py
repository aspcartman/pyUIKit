class Vec:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "x:{} y:{}".format(self.x, self.y)

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y


class Rect:
    def __init__(self, x=0, y=0, width=0, height=0, origin=None, size=None):
        if origin is not None:
            self.origin = origin
        else:
            self.origin = Vec(x, y)

        if size is not None:
            self.size = size
        else:
            self.size = Vec(width, height)

    @property
    def x(self):
        return self.origin.x

    @property
    def y(self):
        return self.origin.y

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    def __cmp__(self, other):
        return self.origin == other.origin and self.size == other.size

    def __str__(self):
        return "x:{} y:{} width:{} height:{}".format(self.x, self.y, self.width, self.height)
