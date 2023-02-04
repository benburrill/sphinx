from abc import ABC, abstractmethod
from expressions import Expression
from dataclasses import dataclass
from memory import MemoryFormat
import typing as ty


# Seems a bit weird to subclass "Expression" because directives are not
# really expressions.  They just play the same sort of game with get().
class Directive(Expression):
    @abstractmethod
    def __len__(self):
        pass


@dataclass
class FillDirective(Directive):
    fill_expr: Expression
    length_expr: Expression

    def get(self):
        return bytes([self.fill_expr.get()]) * self.length_expr.get()

    def __len__(self):
        return self.length_expr.get()


@dataclass
class AsciiDirective(Directive):
    bytestring: bytes

    def __len__(self):
        return len(self.bytestring)

    def get(self):
        return self.bytestring


@dataclass
class WordDirective(Directive):
    word_exprs: ty.Sequence[Expression]
    mf: MemoryFormat

    def __len__(self):
        return self.mf.word_size * len(self.word_exprs)

    def get(self):
        return bytes(self.mf.array_from_words([e.get() for e in self.word_exprs]))


@dataclass
class ByteDirective(Directive):
    byte_exprs: ty.Sequence[Expression]

    def __len__(self):
        return len(self.byte_exprs)

    def get(self):
        return bytes([e.get() for e in self.byte_exprs])



@dataclass
class InstructionDirective(Directive):
    name: str
    arg_exprs: ty.Sequence[Expression]

    def __len__(self):
        return 1

    def get(self):
        return (self.name, *[e.get() for e in self.arg_exprs])
