from abc import ABC, abstractmethod
import itertools as it

from errors import *


class Expression(ABC):
    # get returns a concrete value or raises a ExpressionError if a
    # value is not available
    @abstractmethod
    def get(self):
        pass


class Pretty(ABC):
    def __repr__(self):
        return f'<{type(self).__name__} {self}>'

    @abstractmethod
    def __str__(self):
        pass


class Value(Expression, Pretty):
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def __str__(self):
        return repr(self.value)


# This is kinda dumb, but I don't want to have to worry about whether
# I've figured out what word size the user wants when parsing.
class WordScaled(Expression, Pretty):
    def __init__(self, expr, mf):
        self.expr = expr
        self.mf = mf

    def get(self):
        return self.expr.get() * self.mf.word_size

    def __str__(self):
        return f'{self.expr}w'


class MaybeCyclical(Expression, Pretty):
    def __init__(self):
        self.trying_to_find_out = False

    def get(self):
        if self.trying_to_find_out:
            self.trying_to_find_out = False
            raise CyclicDependencyError(
                f'The expression {self.name} is cyclical and cannot'
                ' be resolved',
                self.origin
            )

        try:
            self.trying_to_find_out = True
            return self.unsafe_get()
        finally:
            self.trying_to_find_out = False

    @abstractmethod
    def unsafe_get(self):
        pass


class Variable(MaybeCyclical):
    def __init__(self, origin, namespace, name):
        super().__init__()
        self.origin = origin
        self.name = name
        self.namespace = namespace

    def unsafe_get(self):
        if self.name in self.namespace:
            return self.namespace[self.name].get()

        raise ExpressionError(
            f'{self.name} is not defined in this namespace',
            self.origin
        )

    def __str__(self):
        return self.name


class Label(MaybeCyclical):
    def __init__(self, origin, name, section, idx):
        super().__init__()
        self.origin = origin
        self.value = None
        self.name = name
        self.section = section
        self.idx = idx

    def unsafe_get(self):
        if self.value is not None:
            return self.value

        try:
            self.value = sum(map(len, it.islice(self.section, self.idx)))
            return self.value
        except ExpressionError as err:
            raise LabelError(
                f'The label {self.name} did not have a concrete address'
                ' when it was referenced',
                self.origin
            ) from err

    def __str__(self):
        return f'{self.name}:'


# Interesting idea if I want to get clever:
# in get, if func is operator.sub and deps directly or indirectly refer
# to labels that have the same section, then compute relative offset.
class Operation(Expression, Pretty):
    def __init__(self, origin, func_name, func, deps):
        self.value = None
        self.origin = origin
        self.func_name = func_name
        self.func = func
        self.deps = deps

    def get(self):
        try:
            self.value = self.func(*[dep.get() for dep in self.deps])
            return self.value
        except ExpressionError:
            raise
        except Exception as err:
            raise EvaluationError(
                f'Encountered an error evaluating {self.func_name}',
                self.origin
            ) from err

    def __str__(self):
        return f'{self.func_name}({", ".join(map(str, self.deps))})'


# Tagged is for instruction directives, for which many arguments need to
# be tagged with some information, eg [5] => ('sv', 5)
class Tagged(Expression):
    def __init__(self, tag, expr):
        self.tag = tag
        self.expr = expr

    def get(self):
        return (self.tag, self.expr.get())

    def __repr__(self):
        return f'<{self.tag} {self.expr}>'
