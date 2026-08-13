"""
Abstract Syntax Tree (AST) Node definitions.
Each node carries a unique ID, node type name, structural properties, and source mapping.
"""

_node_counter = 0

def get_next_node_id():
    global _node_counter
    _node_counter += 1
    return f"node_{_node_counter}"

def reset_node_counter():
    global _node_counter
    _node_counter = 0

class ASTNode:
    def __init__(self, node_type, line=1, column=1, start_pos=0, end_pos=0):
        self.id = get_next_node_id()
        self.node_type = node_type
        self.line = line
        self.column = column
        self.start_pos = start_pos
        self.end_pos = end_pos

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.node_type,
            "line": self.line,
            "column": self.column,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos
        }

class ProgramNode(ASTNode):
    def __init__(self, statements, line=1, column=1, start_pos=0, end_pos=0):
        super().__init__("Program", line, column, start_pos, end_pos)
        self.statements = statements or []

    def to_dict(self):
        data = super().to_dict()
        data["label"] = "Program"
        data["statements"] = [stmt.to_dict() for stmt in self.statements]
        data["children"] = [stmt.to_dict() for stmt in self.statements]
        return data

class VarDeclNode(ASTNode):
    def __init__(self, data_type, var_name, initializer=None, line=1, column=1, start_pos=0, end_pos=0):
        super().__init__("VarDecl", line, column, start_pos, end_pos)
        self.data_type = data_type   # 'int' or 'float'
        self.var_name = var_name     # identifier string
        self.initializer = initializer # ASTNode (expression) or None

    def to_dict(self):
        data = super().to_dict()
        data["label"] = f"VarDecl: {self.data_type} {self.var_name}"
        data["data_type"] = self.data_type
        data["var_name"] = self.var_name
        data["initializer"] = self.initializer.to_dict() if self.initializer else None
        data["children"] = [self.initializer.to_dict()] if self.initializer else []
        return data

class AssignmentNode(ASTNode):
    def __init__(self, var_name, expression, line=1, column=1, start_pos=0, end_pos=0):
        super().__init__("Assignment", line, column, start_pos, end_pos)
        self.var_name = var_name
        self.expression = expression

    def to_dict(self):
        data = super().to_dict()
        data["label"] = f"Assign: {self.var_name} ="
        data["var_name"] = self.var_name
        data["expression"] = self.expression.to_dict()
        data["children"] = [self.expression.to_dict()]
        return data

class IfStatementNode(ASTNode):
    def __init__(self, condition, then_block, else_block=None, line=1, column=1, start_pos=0, end_pos=0):
        super().__init__("IfStatement", line, column, start_pos, end_pos)
        self.condition = condition     # expression
        self.then_block = then_block   # BlockNode
        self.else_block = else_block   # BlockNode or None

    def to_dict(self):
        data = super().to_dict()
        data["label"] = "If Statement"
        data["condition"] = self.condition.to_dict()
        data["then_block"] = self.then_block.to_dict()
        data["else_block"] = self.else_block.to_dict() if self.else_block else None
        
        children = [self.condition.to_dict(), self.then_block.to_dict()]
        if self.else_block:
            children.append(self.else_block.to_dict())
        data["children"] = children
        return data

class BlockNode(ASTNode):
    def __init__(self, statements, line=1, column=1, start_pos=0, end_pos=0):
        super().__init__("Block", line, column, start_pos, end_pos)
        self.statements = statements or []

    def to_dict(self):
        data = super().to_dict()
        data["label"] = "Block ({...})"
        data["statements"] = [stmt.to_dict() for stmt in self.statements]
        data["children"] = [stmt.to_dict() for stmt in self.statements]
        return data

class BinaryOpNode(ASTNode):
    def __init__(self, operator, left, right, line=1, column=1, start_pos=0, end_pos=0):
        super().__init__("BinaryOp", line, column, start_pos, end_pos)
        self.operator = operator   # '+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!='
        self.left = left
        self.right = right

    def to_dict(self):
        data = super().to_dict()
        data["label"] = f"BinaryOp ({self.operator})"
        data["operator"] = self.operator
        data["left"] = self.left.to_dict()
        data["right"] = self.right.to_dict()
        data["children"] = [self.left.to_dict(), self.right.to_dict()]
        return data

class LiteralNode(ASTNode):
    def __init__(self, value, data_type, line=1, column=1, start_pos=0, end_pos=0):
        super().__init__("Literal", line, column, start_pos, end_pos)
        self.value = value        # int or float value
        self.data_type = data_type # 'int' or 'float'

    def to_dict(self):
        data = super().to_dict()
        data["label"] = f"Literal ({self.value})"
        data["value"] = self.value
        data["data_type"] = self.data_type
        data["children"] = []
        return data

class IdentifierNode(ASTNode):
    def __init__(self, name, line=1, column=1, start_pos=0, end_pos=0):
        super().__init__("Identifier", line, column, start_pos, end_pos)
        self.name = name

    def to_dict(self):
        data = super().to_dict()
        data["label"] = f"Identifier ({self.name})"
        data["name"] = self.name
        data["children"] = []
        return data
