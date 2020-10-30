from . import register, match, derive
from dataclasses import dataclass


#####################


@derive("Point", "x", "y")
@dataclass
class Point:
    x: int
    y: int


@register("Thing")
class Thing:
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f"Thing({self.x!r})"

    @classmethod
    def __match__(cls, subpatterns, value, debug):
        if len(subpatterns) != 1:
            raise ValueError("'Thing' expected 1 placeholder")

        [subp] = subpatterns

        if not isinstance(value, Thing):
            return None
        return subp.match(value.x, debug)


@register("Pair")
class Pair:
    @classmethod
    def __match__(cls, subpatterns, value, debug):
        if len(subpatterns) != 2:
            raise ValueError("'Pair' expected 2 placeholders")
        left, right = subpatterns
        if not isinstance(value, tuple) or len(value) != 2:
            return None

        lm = left.match(value[0], debug)
        if lm is None:
            return None

        rm = right.match(value[1], debug)
        if rm is None:
            return None

        return {**lm, **rm}


#####################


def what_is(arg, debug=False):
    with match(arg, debug=debug) as case:
        with case("Thing(x)") as [m]:
            r = m.x

        with case("Pair(Thing(x), Thing(_))") as [m]:
            r = m.x

        with case("Point(a, b)") as [m]:
            r = m.a + m.b

        with case("_") as [m]:
            r = 666

    return r


assert what_is(42) == 666
assert what_is(Thing(5)) == 5
assert what_is((1, 5)) == 666
assert what_is((Thing(1), Thing(2))) == 1
assert what_is(Point(5, 7)) == 12
