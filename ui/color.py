class Color:
	def __init__(self, value=None, hex=None, r=None, g=None, b=None, a=None):
		if hex is not None:
			value = int(hex, 16)
		if value is not None:
			self.red = (value >> 16) & 0xFF
			self.green = (value >> 8) & 0xFF
			self.blue = value & 0xFF
		else:
			self.red = r if r is not None else 0
			self.green = g if g is not None else 0
			self.blue = b if b is not None else 0

		self.alpha = a if a is not None else 255

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

	def tuple(self):
		return self.red, self.green, self.blue, self.alpha

	def with_alpha(self, alpha) -> 'Color':
		return Color(r=self.red, g=self.green, b=self.blue, a=alpha)
