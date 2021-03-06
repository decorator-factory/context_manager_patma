# Usage example

```py
from context_manager_patma import match, register, derive


@register("Pair")
class Pair:
    @staticmethod
    def __match__(subpatterns, value, debug: bool):
        if len(subpatterns) != 2:
            raise ValueError(subpatterns)
        if not isinstance(value, tuple) or len(value) != 2:
            return None

        left_pattern, right_pattern = subpatterns
        left, right = value

        lx = left_pattern.match(left, debug)
        if lx is None:
            return None

        rx = right_pattern.match(right, debug)
        if rx is None:
            return None

        return {**lx, **rx}


@derive("Point", "x", "y")
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def f(x):
    with match(x) as case:
        with case("Pair(Pair(left, _), Pair(_, right))") as [m]:
            ret = (m.left, m.right)

        with case("Pair(left, right)") as [m]:
            ret = (m.left, m.right)

        with case("Point(1, y)") as [m]:
            ret = (1, m.y)

        with case("Point(x, _)") as [m]:
            ret = (2, m.x)

        with case("_"):
            ret = (None, None)
    return ret


assert f( (1, 2) ) == (1, 2)
assert f( ((1, 2), (3, 4)) ) == (1, 4)
assert f( 545345 ) == (None, None)
assert f( Point(1, 5) ) == (1, 5)
assert f( Point(32, 5) ) == (2, 32)
```
