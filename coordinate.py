type Grid[T] = list[list[T]]

class Coordinate:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, "Coordinate"):
            return self.x == other.x and self.y == other.y
        raise Exception("Compare only coordinates with a coordinate")

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def wrapping_add[T](self, other: "Coordinate", grid: Grid[T]) -> "Coordinate":
        y = (self.y + other.y) % len(grid)
        x = (self.x + other.x) % len(grid[y])
        return Coordinate(x , y)

    def get_value_from_grid[T](self, grid: Grid[T]) -> T | None:
        if self.y < 0 or self.y >= len(grid) or self.x < 0 or self.x >= len(grid[self.y]):
            return None
        return grid[self.y][self.x]

    def set_value_in_grid[T](self, grid: Grid[T], value: T):
        if self.y < 0 or self.y >= len(grid) or self.x < 0 or self.x >= len(grid[0]):
            return None
        grid[self.y][self.x] = value

    def get_manh_dist(self, other: "Coordinate") -> int:
        return abs(self.x - other.x) + abs(self.y + other.y)

    @staticmethod
    def get_coord[T](grid: Grid[T], wanted_value: T) -> "Coordinate" | None:
        for (y, line) in enumerate(grid):
            for (x, value) in enumerate(line):
                if value == wanted_value:
                    return Coordinate(x, y)

class Direction(Coordinate):
    up: "Direction"
    down: "Direction"
    left: "Direction"
    right: "Direction"
    dirs: list["Direction"]

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        assert self.x == 0 and self.y in [-1, 1] or self.y == 0 and self.x in [-1, 1]

    def is_perpendicular(self, other: "Direction") -> bool:
        return self.x * other.x + self.y * other.y == 0

    def is_reversed(self, other: "Direction") -> bool:
        return self.x == -other.x and self.y == -other.y

    def turn_right(self) -> "Direction":
       if self.x == 0 and self.y == -1:  # up
           return Direction(1, 0)  # right
       elif self.x == 1 and self.y == 0:  # right
           return Direction(0, 1)  # down
       elif self.x == 0 and self.y == 1:  # down
           return Direction(-1, 0)  # left
       elif self.x == -1 and self.y == 0:  # left
           return Direction(0, -1)  # up
       else:
           raise Exception("Invalid direction")

    def turn_left(self) -> "Direction":
        if self.x == 0 and self.y == -1:  # up
            return Direction(-1, 0)  # left
        elif self.x == -1 and self.y == 0:  # left
            return Direction(0, 1)  # down
        elif self.x == 0 and self.y == 1:  # down
            return Direction(1, 0)  # right
        elif self.x == 1 and self.y == 0:  # right
            return Direction(0, -1)  # up
        else:
            raise Exception("Invalid direction")

Direction.up = Direction(0, -1)
Direction.down = Direction(0, 1)
Direction.left = Direction(-1, 0)
Direction.right = Direction(1, 0)
Direction.dirs = [Direction.up, Direction.down, Direction.left, Direction.right]
        
