"""
Semantic Analyzer and Symbol Table Manager.
Performs declaration checking, scope management, and basic type validation on the AST.
"""

from backend.ast_nodes.nodes import (
    ProgramNode, VarDeclNode, AssignmentNode, 
    IfStatementNode, BlockNode, BinaryOpNode, LiteralNode, IdentifierNode
)
from backend.errors.compiler_errors import SemanticError

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, data_type, line=1, column=1):
        if name in self.symbols:
            raise SemanticError(
                f"Redeclaration error: Variable '{name}' is already declared.",
                line=line, column=column,
                hint=f"Variable '{name}' was previously declared in this scope."
            )
        self.symbols[name] = {
            "name": name,
            "type": data_type,
            "line": line,
            "column": column
        }

    def lookup(self, name, line=1, column=1):
        if name not in self.symbols:
            raise SemanticError(
                f"Variable '{name}' is not defined.",
                line=line, column=column,
                hint=f"Declare variable '{name}' before using it (e.g. int {name} = 0;)."
            )
        return self.symbols[name]

    def to_list(self):
        return list(self.symbols.values())


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, ast_root):
        if not ast_root:
            return self.symbol_table.to_list()
        
        self.visit(ast_root)
        return self.symbol_table.to_list()

    def visit(self, node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, VarDeclNode):
            if node.initializer:
                self.visit(node.initializer)
            self.symbol_table.declare(node.var_name, node.data_type, node.line, node.column)
        elif isinstance(node, AssignmentNode):
            # Verify variable is declared before assignment
            self.symbol_table.lookup(node.var_name, node.line, node.column)
            self.visit(node.expression)
        elif isinstance(node, IfStatementNode):
            self.visit(node.condition)
            self.visit(node.then_block)
            if node.else_block:
                self.visit(node.else_block)
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, BinaryOpNode):
            self.visit(node.left)
            self.visit(node.right)
        elif isinstance(node, IdentifierNode):
            self.symbol_table.lookup(node.name, node.line, node.column)
        elif isinstance(node, LiteralNode):
            pass
        return True
