from sources.tools.line import Line
from sources.tools.point import Point

border_left = [Point(3500,2999), Point(0, 2999)]
border_right = [Point(6999, 2999), Point(3500, 2999)]


class Surface:
    """Define the shape of the surface
        lands : [Point]
    """
    def __init__(self, lands=[]):
        self.lands = lands
        self.find_landing_site()
        self.find_distance_maximum()
        self.border = [
            Line(border_left[0], border_left[1]),
            Line(border_right[1], lands[0]),
            Line(lands[-1], border_right[0]),
            Line(border_right[0], border_right[1])
        ]

    def __iter__(self):
        return iter(self.lands)
    
    def __next__(self):
        return next(self)
    
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __eq__(self, other) -> bool:
        for point_self, point_other in zip(self, other):
            if not point_self == point_other:
                return False
        return True

    def lines(self):
        """Generator of lines"""
        point_a = self.lands[0]
        for point_b in self.lands[1:]:
            yield Line(point_a, point_b)
            point_a = point_b
    
    def find_distance_maximum(self):
        """Find the maximal distance by walk of the landing"""
        distance = 0
        for line in self.lines():
            if line == self.landing_site:
                distance_left = distance
                distance = 0
            else:
                distance += line.lenght()
        self.distance_maximum = max(distance_left, distance)

    def find_landing_site(self) -> None:
        """Find the landing site, the only flat ground of the surface"""
        for line in self.lines():
            if line.point_a.y == line.point_b.y:
                self.landing_site = line
                return None
        raise EnvironmentError()

    def collision(self, point_a : Point, point_b : Point) -> bool:
        """Find out if there was a collision when the lander went from point_a to point_b"""

        for line in self.lines():
            if line.collision(point_a, point_b):
                self.collision_line = line
                return True
        
        for line in self.border:
            if line.collision(point_a, point_b):
                self.collision_line = line
                return True
        
        return False
