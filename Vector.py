import math


class Vect:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def findCCWAngle(self, other):
        return math.degrees(math.asin((self.x * other.y - self.y * other.x)/(self.length()*other.length())))

    def length(self):
        return (self.x**2 + self.y**2)**0.5

    def transform2uvec(self):
        self.x /= self.length()
        self.y /= self.length()
