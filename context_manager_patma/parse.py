import json
from typing import Any, Dict, Optional
from lark import v_args, Transformer, Lark


class Pattern:
    def match(self, value: Any, debug: bool) -> Optional[Dict[str, Any]]:
        raise NotImplementedError


class NamePattern(Pattern):
    def __init__(self, name):
        self.name = str(name)

    def match(self, value: Any, debug: bool) -> Optional[Dict[str, Any]]:
        return {self.name: value}


class IgnorePattern(Pattern):
    def __init__(self, token):
        self.line = token.line
        self.column = token.column
        self.name = str(token)

    def match(self, value: Any, debug: bool) -> Optional[Dict[str, Any]]:
        if debug:
            return {f"__anon({self.name}@{self.line}:{self.column})__": value}
        else:
            return {}


class ExactPattern(Pattern):
    def __init__(self, value):
        self.value = value

    def match(self, value: Any, debug: bool) -> Optional[Dict[str, Any]]:
        if value == self.value:
            if debug:
                return {f"__exact({self.value!r})__": value}
            else:
                return {}
        else:
            return None


class ConstructorPattern(Pattern):
    _constructors = {}

    @staticmethod
    def register(name: str):
        def _register(cls):
            ConstructorPattern._constructors[name] = cls
            return cls
        return _register

    def __init__(self, constructor, *subpatterns):
        self.constructor = str(constructor)
        self.subpatterns = subpatterns

    def match(self, value: Any, debug: bool) -> Optional[Dict[str, Any]]:
        cls = self._constructors[self.constructor]
        return cls.__match__(self.subpatterns, value, debug)


register_constructor = ConstructorPattern.register


@v_args(inline=True)
class PatternTransformer(Transformer):
    ignore_pattern = IgnorePattern
    name_pattern = NamePattern
    constructor_pattern = ConstructorPattern

    @staticmethod
    def string_pattern(token):
        return ExactPattern(json.loads(token.value))

    @staticmethod
    def integer_pattern(token):
        return ExactPattern(int(token.value))


parser = Lark.open(
    "grammar.lark",
    rel_to=__file__,
    parser="lalr",
    transformer=PatternTransformer(),
    propagate_positions=True,
)


def parse(source: str) -> Pattern:
    return parser.parse(source)  # type: ignore
