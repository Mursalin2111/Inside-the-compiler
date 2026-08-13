"""
Token representation for the Lexical Analyzer.
"""

# Token Types enum constants
TokenType = {
    # Keywords
    "KEYWORD": "KEYWORD",         # int, float, if, else
    "IDENTIFIER": "IDENTIFIER",   # variable names (a, b, x, y)
    "NUMBER": "NUMBER",           # 10, 20.5
    
    # Operators
    "ASSIGNMENT": "ASSIGNMENT",   # =
    "PLUS": "PLUS",               # +
    "MINUS": "MINUS",             # -
    "MULTIPLY": "MULTIPLY",       # *
    "DIVIDE": "DIVIDE",           # /
    
    # Relational
    "GREATER": "GREATER",         # >
    "LESS": "LESS",               # <
    "GREATER_EQUAL": "GREATER_EQUAL", # >=
    "LESS_EQUAL": "LESS_EQUAL",   # <=
    "EQUAL": "EQUAL",             # ==
    "NOT_EQUAL": "NOT_EQUAL",     # !=
    
    # Delimiters
    "SEMICOLON": "SEMICOLON",     # ;
    "LPAREN": "LPAREN",           # (
    "RPAREN": "RPAREN",           # )
    "LBRACE": "LBRACE",           # {
    "RBRACE": "RBRACE",           # }
    
    # Special
    "EOF": "EOF"
}

TOKEN_EXPLANATIONS = {
    "KEYWORD": "A reserved word in the programming language with a fixed semantic meaning (e.g., data type or control flow).",
    "IDENTIFIER": "A user-defined name used to identify variables or storage locations in memory.",
    "NUMBER": "A numeric literal value (integer or floating point constant).",
    "ASSIGNMENT": "Assignment operator used to store the right-hand value into the left-hand variable.",
    "PLUS": "Arithmetic addition operator.",
    "MINUS": "Arithmetic subtraction operator.",
    "MULTIPLY": "Arithmetic multiplication operator.",
    "DIVIDE": "Arithmetic division operator.",
    "GREATER": "Relational operator checking if left value is strictly greater than right value.",
    "LESS": "Relational operator checking if left value is strictly less than right value.",
    "GREATER_EQUAL": "Relational operator checking if left value is greater than or equal to right value.",
    "LESS_EQUAL": "Relational operator checking if left value is less than or equal to right value.",
    "EQUAL": "Relational comparison operator checking for structural equality.",
    "NOT_EQUAL": "Relational comparison operator checking for inequality.",
    "SEMICOLON": "Statement terminator marking the end of a statement.",
    "LPAREN": "Opening parenthesis used for grouping expressions or specifying parameters.",
    "RPAREN": "Closing parenthesis.",
    "LBRACE": "Opening curly brace denoting the start of a code block.",
    "RBRACE": "Closing curly brace denoting the end of a code block.",
    "EOF": "End-Of-File token indicating the completion of lexical analysis."
}

class Token:
    def __init__(self, token_type, value, line, column, start_pos, end_pos):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.explanation = TOKEN_EXPLANATIONS.get(token_type, "Lexical token produced by the scanner.")

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', Line:{self.line}, Col:{self.column})"

    def to_dict(self):
        return {
            "type": self.type,
            "value": str(self.value),
            "line": self.line,
            "column": self.column,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos,
            "explanation": self.explanation
        }
