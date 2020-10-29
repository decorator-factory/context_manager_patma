from typing import Dict, Generic, TypeVar
from . import parse


class _MatchManager:
    def __init__(self, arg, debug: bool):
        self.arg = arg
        self.debug = debug

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            raise MatchFailed(self.arg)
        elif exc_type is _MatchSuccessful:
            return True
        else:
            return False

    def __call__(self, pattern: str):
        return Case(parse.parse(pattern), self.arg, self.debug)


def match(arg, debug: bool = False):
    return _MatchManager(arg, debug)


class _MatchSuccessful(Exception):
    pass


class MatchFailed(LookupError):
    pass


T = TypeVar("T")


class Match(Generic[T]):
    def __init__(self, data: Dict[str, T]):
        self._data = data

    def __getattr__(self, key: str) -> T:
        try:
            return self._data[key]
        except KeyError as e:
            raise AttributeError(key) from e

    def __repr__(self):
        return f"Match({self._data})"


class Case:
    def __init__(self, pattern: parse.Pattern, arg, debug: bool):
        self.pattern = pattern
        self.arg = arg
        self.debug = debug

    def __enter__(self):
        if (m := self.pattern.match(self.arg, self.debug)) is not None:
            return (Match(m),)
        else:
            return ()

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            raise _MatchSuccessful
        if exc_type is ValueError and "not enough values to unpack" in exc_value.args[0]:
            return True
        return False


register = parse.register_constructor
