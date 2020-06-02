from Vector import Vector2d
import random

class windforce:
    def __init__(self, max):
        self.max = int(max * 100)
        self.force = Vector2d(0.0, 0.0)
        self.newWind()

    def newWind(self):
        if self.max == 0:
            self.force = Vector2d(0.0, 0.0)
        else:
            self.force = Vector2d(float(random.randint(-self.max, self.max))/100.0, 0.0)
