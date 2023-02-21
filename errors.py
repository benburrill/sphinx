from dataclasses import dataclass

@dataclass
class Origin:
    file: str
    line: int
    column: int

class AssemblerError(Exception):
    def __init__(self, message, origin):
        super().__init__(message)
        self.origin = origin

class AssemblerSyntaxError(AssemblerError):
    @classmethod
    def unhelpful(cls, origin):
        return cls('Invalid syntax', origin)

class NameConflictError(AssemblerError):
    pass

class ExpressionError(AssemblerError):
    pass

class LabelError(ExpressionError):
    pass

class CyclicDependencyError(ExpressionError):
    pass

class EvaluationError(ExpressionError):
    pass
