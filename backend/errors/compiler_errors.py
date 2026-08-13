"""
Compiler Error Classes
Provides structured error reporting across all compiler phases.
"""

class CompilerError(Exception):
    def __init__(self, phase, message, line=1, column=1, start_pos=0, end_pos=0, expected=None, found=None, hint=None):
        super().__init__(message)
        self.phase = phase            # 'lexer', 'parser', 'semantic', 'runtime'
        self.message = message
        self.line = line
        self.column = column
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.expected = expected
        self.found = found
        self.hint = hint

    def to_dict(self):
        return {
            "phase": self.phase,
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos,
            "expected": self.expected,
            "found": self.found,
            "hint": self.hint
        }

class LexicalError(CompilerError):
    def __init__(self, message, line=1, column=1, start_pos=0, end_pos=0, found=None, hint=None):
        super().__init__(
            phase="lexer",
            message=message,
            line=line,
            column=column,
            start_pos=start_pos,
            end_pos=end_pos,
            expected="Valid Token",
            found=found,
            hint=hint or "Check for unsupported characters or unrecognized tokens."
        )

class SyntaxError(CompilerError):
    def __init__(self, message, line=1, column=1, start_pos=0, end_pos=0, expected=None, found=None, hint=None):
        super().__init__(
            phase="parser",
            message=message,
            line=line,
            column=column,
            start_pos=start_pos,
            end_pos=end_pos,
            expected=expected,
            found=found,
            hint=hint or "Ensure your statement follows C-like grammar rules (e.g. semicolons, matching braces)."
        )

class SemanticError(CompilerError):
    def __init__(self, message, line=1, column=1, start_pos=0, end_pos=0, hint=None):
        super().__init__(
            phase="semantic",
            message=message,
            line=line,
            column=column,
            start_pos=start_pos,
            end_pos=end_pos,
            hint=hint or "Ensure all variables are declared before use and types are compatible."
        )

class RuntimeError(CompilerError):
    def __init__(self, message, line=1, column=1, hint=None):
        super().__init__(
            phase="runtime",
            message=message,
            line=line,
            column=column,
            hint=hint or "Check arithmetic operations (e.g. division by zero) or variable values."
        )
