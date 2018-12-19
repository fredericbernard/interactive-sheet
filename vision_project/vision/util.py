import math
import numpy as np


class PixelCoordinate:

    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def north(self):
        return PixelCoordinate(self.x, self.y - 1)

    def south(self):
        return PixelCoordinate(self.x, self.y + 1)

    def __add__(self, other: 'PixelCoordinate') -> 'PixelCoordinate':
        return PixelCoordinate(self.x + other.x, self.y + other.y)

    def __gt__(self, other):
        return self.x > other.x

    def __lt__(self, other):
        return self.x < other.x

    def __eq__(self, other: "PixelCoordinate") -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * self.x + 59 * self.y

    def __sub__(self, other):
        return PixelCoordinate(self.x - other.x, self.y - other.y)

    def isclose(self, other: "PixelCoordinate", delta=10):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 <= delta ** 2

    def euclidean_length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return f"PixelCoordinate: ({self.x}, {self.y})"

    def rotate(self, angle_rad: float) -> "SubPixelCoordinate":
        return SubPixelCoordinate(
            math.cos(angle_rad) * self.x - math.sin(angle_rad) * self.y,
            math.sin(angle_rad) * self.x + math.cos(angle_rad) * self.y
        )


class SubPixelCoordinate(object):

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def normalize(self) -> "SubPixelCoordinate":
        return SubPixelCoordinate(
            self.x / self.euclidean_length(),
            self.y / self.euclidean_length()
        )

    def rotate(self, angle_rad: float) -> "SubPixelCoordinate":
        return SubPixelCoordinate(
            math.cos(angle_rad) * self.x - math.sin(angle_rad) * self.y,
            math.sin(angle_rad) * self.x + math.cos(angle_rad) * self.y
        )

    def euclidean_length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __mul__(self, other: float) -> "SubPixelCoordinate":
        return SubPixelCoordinate(self.x * other, self.y * other)

    def __add__(self, other) -> "SubPixelCoordinate":
        return SubPixelCoordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "SubPixelCoordinate":
        return SubPixelCoordinate(self.x - other.x, self.y - other.y)


class CameraCoordinate(PixelCoordinate):
    pass


class ProjectorCoordinate(PixelCoordinate):
    pass


class WorldCoordinate(object):

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other: 'WorldCoordinate') -> 'WorldCoordinate':
        return WorldCoordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'WorldCoordinate') -> 'WorldDelta':
        return WorldDelta(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __eq__(self, other) -> bool:
        if not isinstance(other, WorldCoordinate):
            return False
        return self.is_close(other)

    def is_close(self, other: "WorldCoordinate", delta=0.02) -> bool:
        return math.isclose(self.x, other.x, abs_tol=delta) and math.isclose(self.y, other.y, abs_tol=delta)

    def euclidean_length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)


class RelativeWorldCoordinate(WorldCoordinate):
    pass


class WorldDelta(object):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angle_radians(self) -> float:
        return math.atan2(self.x, -self.y) + 2 * math.pi


class OrientedWorldCoordinate:

    def __init__(self, coordinate: WorldCoordinate, angle: int):
        self.coordinate = coordinate
        self.angle = angle


class OrientedPixelCoordinate:

    def __init__(self, coordinate: PixelCoordinate, angle: int):
        self.coordinate = coordinate
        self.angle = angle


class Mask:

    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix

    def __add__(self, other):
        return Mask(self.matrix + other.matrix)

    def __sub__(self, other):
        return Mask(self.matrix - other.matrix)


class HsvColour:

    def __init__(self, hue: int, sat: int, val: int):
        self.colour = [hue, sat, val]
