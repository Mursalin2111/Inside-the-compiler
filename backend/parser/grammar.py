"""
Formal LL(1) Grammar Representation.
Defines Non-Terminals, Terminals, Start Symbol, and Production Rules for the educational language.
"""

EPSILON = "ε"
EOF_SYMBOL = "$"

class Production:
    def __init__(self, prod_id, lhs, rhs, explanation=None):
        self.id = prod_id
        self.lhs = lhs          # Non-terminal string (e.g., 'Expression')
        self.rhs = rhs          # List of symbol strings (e.g., ['Term', 'ExpressionPrime'])
        self.explanation = explanation or f"{lhs} → {' '.join(rhs)}"

    @property
    def rhs_str(self):
        return ' '.join(self.rhs)

    def __repr__(self):
        return f"[{self.id}] {self.lhs} → {self.rhs_str}"

    def to_dict(self):
        return {
            "id": self.id,
            "lhs": self.lhs,
            "rhs": self.rhs,
            "rhs_str": self.rhs_str,
            "production_str": str(self),
            "explanation": self.explanation
        }


class Grammar:
    def __init__(self):
        self.start_symbol = "Program"
        
        self.non_terminals = [
            "Program", "StatementList", "Statement", 
            "Declaration", "Assignment", "Type", 
            "IfStatement", "ElseClause", "Condition", "RelOp", 
            "Expression", "ExpressionPrime", "Term", "TermPrime", "Factor"
        ]

        self.terminals = [
            "int", "float", "if", "else", 
            "ID", "NUMBER", "=", ";", 
            "(", ")", "{", "}", 
            "+", "-", "*", "/", 
            ">", "<", ">=", "<=", "==", "!="
        ]

        self.productions = []
        self._build_productions()

    def _build_productions(self):
        prods = [
            # Program
            (1, "Program", ["StatementList"], "Program derives a sequence of statements."),
            
            # StatementList
            (2, "StatementList", ["Statement", "StatementList"], "StatementList expands to a Statement followed by more statements."),
            (3, "StatementList", [EPSILON], "StatementList expands to empty string (ε) when no more statements remain."),
            
            # Statement
            (4, "Statement", ["Declaration"], "Statement derives a Variable Declaration."),
            (5, "Statement", ["Assignment"], "Statement derives an Assignment Statement."),
            (6, "Statement", ["IfStatement"], "Statement derives a Conditional If Statement."),
            
            # Declaration
            (7, "Declaration", ["Type", "ID", "=", "Expression", ";"], "Declaration declares a typed variable initialized with an expression."),
            
            # Assignment
            (8, "Assignment", ["ID", "=", "Expression", ";"], "Assignment assigns an expression result to an identifier."),
            
            # Type
            (9, "Type", ["int"], "Type resolves to integer type keyword."),
            (10, "Type", ["float"], "Type resolves to float type keyword."),
            
            # IfStatement & ElseClause
            (11, "IfStatement", ["if", "(", "Condition", ")", "{", "StatementList", "}", "ElseClause"], "IfStatement evaluates a condition and executes a block."),
            (12, "ElseClause", ["else", "{", "StatementList", "}"], "ElseClause provides an alternate block when condition is false."),
            (13, "ElseClause", [EPSILON], "ElseClause resolves to ε when no else block exists."),
            
            # Condition & RelOp
            (14, "Condition", ["Expression", "RelOp", "Expression"], "Condition compares two expressions using a relational operator."),
            (15, "RelOp", [">"], "Relational operator greater-than."),
            (16, "RelOp", ["<"], "Relational operator less-than."),
            (17, "RelOp", [">="], "Relational operator greater-than-or-equal."),
            (18, "RelOp", ["<="], "Relational operator less-than-or-equal."),
            (19, "RelOp", ["=="], "Relational operator equality."),
            (20, "RelOp", ["!="], "Relational operator inequality."),
            
            # Expression
            (21, "Expression", ["Term", "ExpressionPrime"], "Expression evaluates a Term followed by additive terms."),
            (22, "ExpressionPrime", ["+", "Term", "ExpressionPrime"], "ExpressionPrime adds another Term."),
            (23, "ExpressionPrime", ["-", "Term", "ExpressionPrime"], "ExpressionPrime subtracts another Term."),
            (24, "ExpressionPrime", [EPSILON], "ExpressionPrime terminates additive chain with ε."),
            
            # Term
            (25, "Term", ["Factor", "TermPrime"], "Term evaluates a Factor followed by multiplicative factors."),
            (26, "TermPrime", ["*", "Factor", "TermPrime"], "TermPrime multiplies another Factor."),
            (27, "TermPrime", ["/", "Factor", "TermPrime"], "TermPrime divides another Factor."),
            (28, "TermPrime", [EPSILON], "TermPrime terminates multiplicative chain with ε."),
            
            # Factor
            (29, "Factor", ["ID"], "Factor resolves to variable identifier."),
            (30, "Factor", ["NUMBER"], "Factor resolves to numeric literal constant."),
            (31, "Factor", ["(", "Expression", ")"], "Factor evaluates parenthesized expression.")
        ]

        for pid, lhs, rhs, exp in prods:
            self.productions.append(Production(pid, lhs, rhs, exp))

    def get_productions_for(self, non_terminal):
        return [p for p in self.productions if p.lhs == non_terminal]

    def is_terminal(self, symbol):
        return symbol in self.terminals or symbol == EOF_SYMBOL

    def is_non_terminal(self, symbol):
        return symbol in self.non_terminals

    def to_dict(self):
        return {
            "start_symbol": self.start_symbol,
            "non_terminals": self.non_terminals,
            "terminals": self.terminals,
            "productions": [p.to_dict() for p in self.productions]
        }
