import math

class Point:
    """Define point of space
        x : [0, 6999]
        y : [0, 2999]
    """
    def __init__(self, x : int, y : int):
        self.x = min(6999,max(0,x))
        self.y = min(2999,max(0,y))

    def __str__(self):
        return f"{self.x} {self.y}"

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __eq__(self, other) -> bool:
        return (abs(self.x - other.x) < 1 and abs(self.y - other.y) < 1)

    def distance(self, other) -> float:
        """Calcul the distance between two points"""
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2 )