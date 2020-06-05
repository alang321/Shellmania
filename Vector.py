import numpy as np

class Vector2d:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # create addNumbers static method
    @staticmethod
    def getvectorfrompoints(origin, target):
        return Vector2d(target[0] - origin[0], target[1] - origin[1])

    # angle from 0 to 2pi between two vectors
    def find360CCWAngle(self, vec2):
        angles = np.arctan2((self.x, vec2.x), (self.y, vec2.y))
        angle = angles[0] - angles[1]
        if angle < 0:
            angle = 2.0 * np.pi + angle
        return angle

    #return new vecto rotated by angle vec over angle in radians
    def getrotatedvect(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return Vector2d(self.x*c-self.y*s, self.x*s+self.y*c)

    #get the reflection of a vector over a normal vector
    def getreflectionvect(self, normal):
        temp = 2.0 * self.dotprod(self, normal)
        tempvec = Vector2d(temp * normal.x, temp * normal.y)
        return Vector2d(self.x - tempvec.x, self.y - tempvec.y)

    def length(self):
        return (self.x**2 + self.y**2)**0.5

    #skips taking the root, faster for cases where you need the square anyway
    def lengthsquared(self):
        return self.x**2 + self.y**2

    @staticmethod
    def dotprod(vec1, vec2):
        return vec1.x * vec2.x + vec1.y * vec2.y

    def getuvec(self):
        length = self.length()
        if length == 0:
            return Vector2d(0.0, 0.0)
        else:
            return Vector2d(self.x/length, self.y/length)

    def getnormalvec(self):
        return Vector2d(self.y, -self.x)

    def copy(self):
        return Vector2d(self.x, self.y)

    #operator definitions
    def __mul__(self, other):
        return Vector2d(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vector2d(self.x * other, self.y * other)

    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        return

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        if key == 1:
            self.y = value

    def __len__(self):
        return 2