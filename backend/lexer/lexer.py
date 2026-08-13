"""
Real Lexical Analyzer (Scanner).
Scans source code character by character and generates a list of tokens.
"""

from .token import Token, TokenType
from backend.errors.compiler_errors import LexicalError

KEYWORDS = {"int", "float", "if", "else"}

class Lexer:
    def __init__(self, source_code):
        self.source = source_code or ""
        self.pos = 0
        self.length = len(self.source)
        self.line = 1
        self.column = 1

    def peek(self, offset=0):
        target_pos = self.pos + offset
        if target_pos < self.length:
            return self.source[target_pos]
        return None

    def advance(self):
        ch = self.peek()
        if ch is not None:
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        return ch

    def tokenize(self):
        tokens = []

        while self.pos < self.length:
            ch = self.peek()

            # Skip whitespace
            if ch in ' \t\r\n':
                self.advance()
                continue

            # Skip comments (// single line or /* multi line */)
            if ch == '/' and self.peek(1) == '/':
                while self.pos < self.length and self.peek() != '\n':
                    self.advance()
                continue

            if ch == '/' and self.peek(1) == '*':
                start_line = self.line
                start_col = self.column
                self.advance() # /
                self.advance() # *
                while self.pos < self.length:
                    if self.peek() == '*' and self.peek(1) == '/':
                        self.advance() # *
                        self.advance() # /
                        break
                    self.advance()
                else:
                    raise LexicalError(
                        "Unterminated block comment",
                        line=start_line,
                        column=start_col,
                        found="/*"
                    )
                continue

            start_pos = self.pos
            start_line = self.line
            start_col = self.column

            # Identifiers and Keywords
            if ch.isalpha() or ch == '_':
                lexeme = ""
                while self.pos < self.length and (self.peek().isalnum() or self.peek() == '_'):
                    lexeme += self.advance()
                
                t_type = TokenType["KEYWORD"] if lexeme in KEYWORDS else TokenType["IDENTIFIER"]
                tokens.append(Token(t_type, lexeme, start_line, start_col, start_pos, self.pos))
                continue

            # Numbers (int or float)
            if ch.isdigit():
                lexeme = ""
                has_decimal = False
                while self.pos < self.length:
                    curr = self.peek()
                    if curr.isdigit():
                        lexeme += self.advance()
                    elif curr == '.' and not has_decimal and self.peek(1) and self.peek(1).isdigit():
                        has_decimal = True
                        lexeme += self.advance()
                    else:
                        break
                
                tokens.append(Token(TokenType["NUMBER"], lexeme, start_line, start_col, start_pos, self.pos))
                continue

            # Two-character operators
            two_ch = ch + (self.peek(1) or '')
            if two_ch == '==':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType["EQUAL"], "==", start_line, start_col, start_pos, self.pos))
                continue
            if two_ch == '!=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType["NOT_EQUAL"], "!=", start_line, start_col, start_pos, self.pos))
                continue
            if two_ch == '>=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType["GREATER_EQUAL"], ">=", start_line, start_col, start_pos, self.pos))
                continue
            if two_ch == '<=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType["LESS_EQUAL"], "<=", start_line, start_col, start_pos, self.pos))
                continue

            # Single-character operators and delimiters
            if ch == '=':
                self.advance()
                tokens.append(Token(TokenType["ASSIGNMENT"], "=", start_line, start_col, start_pos, self.pos))
                continue
            if ch == '+':
                self.advance()
                tokens.append(Token(TokenType["PLUS"], "+", start_line, start_col, start_pos, self.pos))
                continue
            if ch == '-':
                self.advance()
                tokens.append(Token(TokenType["MINUS"], "-", start_line, start_col, start_pos, self.pos))
                continue
            if ch == '*':
                self.advance()
                tokens.append(Token(TokenType["MULTIPLY"], "*", start_line, start_col, start_pos, self.pos))
                continue
            if ch == '/':
                self.advance()
                tokens.append(Token(TokenType["DIVIDE"], "/", start_line, start_col, start_pos, self.pos))
                continue
            if ch == '>':
                self.advance()
                tokens.append(Token(TokenType["GREATER"], ">", start_line, start_col, start_pos, self.pos))
                continue
            if ch == '<':
                self.advance()
                tokens.append(Token(TokenType["LESS"], "<", start_line, start_col, start_pos, self.pos))
                continue
            if ch == ';':
                self.advance()
                tokens.append(Token(TokenType["SEMICOLON"], ";", start_line, start_col, start_pos, self.pos))
                continue
            if ch == '(':
                self.advance()
                tokens.append(Token(TokenType["LPAREN"], "(", start_line, start_col, start_pos, self.pos))
                continue
            if ch == ')':
                self.advance()
                tokens.append(Token(TokenType["RPAREN"], ")", start_line, start_col, start_pos, self.pos))
                continue
            if ch == '{':
                self.advance()
                tokens.append(Token(TokenType["LBRACE"], "{", start_line, start_col, start_pos, self.pos))
                continue
            if ch == '}':
                self.advance()
                tokens.append(Token(TokenType["RBRACE"], "}", start_line, start_col, start_pos, self.pos))
                continue

            # Invalid Character error
            err_char = self.advance()
            raise LexicalError(
                f"Unrecognized or invalid character '{err_char}'",
                line=start_line,
                column=start_col,
                start_pos=start_pos,
                end_pos=self.pos,
                found=err_char,
                hint="Remove or replace invalid character."
            )

        # Append EOF token
        tokens.append(Token(TokenType["EOF"], "", self.line, self.column, self.pos, self.pos))
        return tokens
