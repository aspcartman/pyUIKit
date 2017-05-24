class Color:
    scheme = None

    def __init__(self, value=None, hex=None, r=None, g=None, b=None, a=None, tuple=None):
        self.alpha = 1.0

        if hex is not None:
            value = int(hex, 16)
        if value is not None:
            self.red = ((value >> 16) & 0xFF) / 0xFF
            self.green = ((value >> 8) & 0xFF) / 0xFF
            self.blue = (value & 0xFF) / 0xFF
        else:
            self.red = r if r is not None else 0
            self.green = g if g is not None else 0
            self.blue = b if b is not None else 0
        if tuple is not None:
            self.red, self.green, self.blue = tuple
            if len(tuple) > 3:
                self.alpha = tuple[3]
        if a is not None:
            self.alpha = a

    @staticmethod
    def white():
        return Color(value=0xffffff)

    @staticmethod
    def black():
        return Color(0x000000)

    @staticmethod
    def red():
        return Color(0xff0000)

    @staticmethod
    def green():
        return Color(0x00ff00)

    @staticmethod
    def blue():
        return Color(0x0000ff)

    @staticmethod
    def clear():
        return Color(a=0)

    def tuple(self):
        return self.red, self.green, self.blue, self.alpha

    def with_alpha(self, alpha) -> 'Color':
        return Color(r=self.red, g=self.green, b=self.blue, a=alpha)


class FlatRedScheme:
    @staticmethod
    def back():
        return Color(0x1C2021)

    @staticmethod
    def front():
        return Color(0x353C3E)

    @staticmethod
    def tint():
        return Color(0xE66A39)

    @staticmethod
    def warn():
        return Color(0xD04E33)

    @staticmethod
    def white():
        return Color(0xEEEEEE)


Color.scheme = FlatRedScheme
