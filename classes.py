import math

class Point:
    __slots__ = ['x', 'y']

    def __init__(self, x, y=None):
        if y is None:
            self.x, self.y = x[0], x[1]
        else:
            self.x, self.y = x, y

    def __repr__(self):
        return 'Point(%r, %r)' % (self.x, self.y)

    def __str__(self):
        return '%G,%G' % (self.x, self.y)

    def __complex__(self):
        return complex(self.x, self.y)

    def __hash__(self):
        return hash(self.__complex__())

    def __bool__(self):
        return bool(self.x or self.y)

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            return Point(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            return Point(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        else:
            return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        else:
            return Point(self.x / other, self.y / other)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __len__(self):
        return math.hypot(self.x, self.y)

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except Exception:
            return False

    def __ne__(self, other):
        try:
            return self.x != other.x or self.y != other.y
        except Exception:
            return True

    add = __add__
    subtract = __sub__
    multiply = __mul__
    divide = __truediv__
    negate = __neg__
    getLength = __len__
    equals = __eq__

    def copy(self):
        return Point(self.x, self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def normalize(self, length=1):
        current = self.__len__()
        scale = length / current if current != 0 else 0
        return Point(self.x * scale, self.y * scale)

    def getDistance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)