"""
Three-Address Code (TAC) Intermediate Representation Generator.
Translates AST nodes into sequential TAC quadruples with full AST node ID and source code mapping.
"""

from backend.ast_nodes.nodes import (
    ProgramNode, VarDeclNode, AssignmentNode, 
    IfStatementNode, BlockNode, BinaryOpNode, LiteralNode, IdentifierNode
)

class TACInstruction:
    def __init__(self, step, op, arg1, arg2, result, ast_node_id=None, ast_node_type=None, line=1, column=1, explanation=None):
        self.step = step
        self.op = op             # '=', '+', '*', 'IF_FALSE', 'GOTO', 'LABEL'
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
        self.ast_node_id = ast_node_id
        self.ast_node_type = ast_node_type
        self.line = line
        self.column = column
        self.explanation = explanation or self.default_explanation()
        self.instruction_str = self.format_str()

    def format_str(self):
        if self.op == "LABEL":
            return f"{self.result}:"
        elif self.op == "GOTO":
            return f"goto {self.result}"
        elif self.op == "IF_FALSE":
            return f"ifFalse {self.arg1} goto {self.result}"
        elif self.op == "=":
            return f"{self.result} = {self.arg1}"
        else:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"

    def default_explanation(self):
        if self.op == "LABEL":
            return f"Define jump target location {self.result}."
        elif self.op == "GOTO":
            return f"Unconditional jump to label {self.result}."
        elif self.op == "IF_FALSE":
            return f"Conditional jump to label {self.result} if condition '{self.arg1}' evaluates to false (0)."
        elif self.op == "=":
            return f"Assign value of '{self.arg1}' into variable '{self.result}'."
        else:
            return f"Perform binary operation '{self.arg1} {self.op} {self.arg2}' and store result into temporary '{self.result}'."

    def to_dict(self):
        return {
            "step": self.step,
            "op": self.op,
            "arg1": str(self.arg1) if self.arg1 is not None else None,
            "arg2": str(self.arg2) if self.arg2 is not None else None,
            "result": str(self.result) if self.result is not None else None,
            "instruction": self.instruction_str,
            "ast_node_id": self.ast_node_id,
            "ast_node_type": self.ast_node_type,
            "line": self.line,
            "column": self.column,
            "explanation": self.explanation
        }


class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, op, arg1, arg2, result, ast_node=None, explanation=None):
        step = len(self.instructions) + 1
        inst = TACInstruction(
            step=step,
            op=op,
            arg1=arg1,
            arg2=arg2,
            result=result,
            ast_node_id=ast_node.id if ast_node else None,
            ast_node_type=ast_node.node_type if ast_node else None,
            line=ast_node.line if ast_node else 1,
            column=ast_node.column if ast_node else 1,
            explanation=explanation
        )
        self.instructions.append(inst)
        return inst

    def generate(self, ast_root):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0
        
        if ast_root:
            self.visit(ast_root)
            
        return [inst.to_dict() for inst in self.instructions]

    def visit(self, node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.visit(stmt)
            return None

        elif isinstance(node, VarDeclNode):
            if node.initializer:
                val = self.visit(node.initializer)
                self.emit("=", val, None, node.var_name, ast_node=node,
                          explanation=f"Initialize variable '{node.var_name}' with value of '{val}'.")
            else:
                # Default 0 initialization
                self.emit("=", 0, None, node.var_name, ast_node=node,
                          explanation=f"Declare variable '{node.var_name}' initialized to 0.")
            return node.var_name

        elif isinstance(node, AssignmentNode):
            val = self.visit(node.expression)
            self.emit("=", val, None, node.var_name, ast_node=node,
                      explanation=f"Assign expression result '{val}' to variable '{node.var_name}'.")
            return node.var_name

        elif isinstance(node, IfStatementNode):
            cond_val = self.visit(node.condition)
            else_label = self.new_label()
            end_label = self.new_label() if node.else_block else else_label

            # Jump to else/end if condition false
            self.emit("IF_FALSE", cond_val, None, else_label, ast_node=node,
                      explanation=f"If condition '{cond_val}' is false, jump to {else_label}.")
            
            # Then block
            self.visit(node.then_block)

            if node.else_block:
                self.emit("GOTO", None, None, end_label, ast_node=node,
                          explanation=f"Jump to end of if-else block ({end_label}).")
                self.emit("LABEL", None, None, else_label, ast_node=node,
                          explanation=f"Label {else_label}: Beginning of 'else' block.")
                self.visit(node.else_block)
                self.emit("LABEL", None, None, end_label, ast_node=node,
                          explanation=f"Label {end_label}: End of if statement.")
            else:
                self.emit("LABEL", None, None, else_label, ast_node=node,
                          explanation=f"Label {else_label}: End of if statement.")

            return None

        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self.visit(stmt)
            return None

        elif isinstance(node, BinaryOpNode):
            left_val = self.visit(node.left)
            right_val = self.visit(node.right)
            temp = self.new_temp()
            self.emit(node.operator, left_val, right_val, temp, ast_node=node,
                      explanation=f"Compute '{left_val} {node.operator} {right_val}' and assign to temporary '{temp}'.")
            return temp

        elif isinstance(node, LiteralNode):
            return node.value

        elif isinstance(node, IdentifierNode):
            return node.name

        return None
