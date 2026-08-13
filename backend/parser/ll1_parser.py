"""
Table-Driven Stack-Based LL(1) Parser.
Simulates pushdown automaton execution steps, constructs Concrete Parse Tree (CST),
and transforms CST into an Abstract Syntax Tree (AST).
"""

from .grammar import Grammar, EPSILON, EOF_SYMBOL
from .first_follow import calculate_first_sets, calculate_follow_sets
from .ll1_table import build_ll1_table
from backend.lexer.token import TokenType
from backend.ast_nodes.nodes import (
    ProgramNode, VarDeclNode, AssignmentNode, 
    IfStatementNode, BlockNode, BinaryOpNode, LiteralNode, 
    IdentifierNode, reset_node_counter
)
from backend.errors.compiler_errors import SyntaxError

_cst_counter = 0

def get_next_cst_id():
    global _cst_counter
    _cst_counter += 1
    return f"cst_node_{_cst_counter}"


class ParseTreeNode:
    def __init__(self, symbol, is_terminal=False, token=None):
        self.id = get_next_cst_id()
        self.symbol = symbol
        self.is_terminal = is_terminal
        self.token = token
        self.children = []
        self.line = token.line if token else 1
        self.column = token.column if token else 1
        self.start_pos = token.start_pos if token else 0
        self.end_pos = token.end_pos if token else 0

    def add_child(self, child):
        self.children.append(child)
        if child.line and child.line > 1:
            self.line = child.line
            self.column = child.column

    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "label": f"{self.symbol}: {self.token.value}" if (self.is_terminal and self.token and self.token.value) else self.symbol,
            "is_terminal": self.is_terminal,
            "lexeme": self.token.value if self.token else None,
            "line": self.line,
            "column": self.column,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos,
            "children": [c.to_dict() for c in self.children]
        }


def token_to_terminal(token):
    """
    Maps a Lexer Token object to its corresponding LL(1) Grammar terminal symbol.
    """
    if not token or token.type == TokenType["EOF"]:
        return EOF_SYMBOL
    
    if token.type == TokenType["KEYWORD"]:
        return token.value  # 'int', 'float', 'if', 'else'
    elif token.type == TokenType["IDENTIFIER"]:
        return "ID"
    elif token.type == TokenType["NUMBER"]:
        return "NUMBER"
    else:
        # +, -, *, /, =, ;, (, ), {, }, >, <, >=, <=, ==, !=
        return token.value


class LL1Parser:
    def __init__(self, tokens):
        global _cst_counter
        _cst_counter = 0
        reset_node_counter()

        self.tokens = [t for t in (tokens or []) if t.type != TokenType["EOF"]]
        self.grammar = Grammar()
        self.first_sets = calculate_first_sets(self.grammar)
        self.follow_sets = calculate_follow_sets(self.grammar, self.first_sets)
        
        table_result = build_ll1_table(self.grammar, self.first_sets, self.follow_sets)
        self.table = table_result["table"]
        self.conflicts = table_result["conflicts"]

    def parse(self):
        steps = []
        input_stream = list(self.tokens)
        
        # Append EOF Token
        last_tok = self.tokens[-1] if self.tokens else None
        eof_token = type('EOFToken', (), {
            'type': TokenType["EOF"],
            'value': '$',
            'line': last_tok.line if last_tok else 1,
            'column': (last_tok.column + len(last_tok.value)) if last_tok else 1,
            'start_pos': last_tok.end_pos if last_tok else 0,
            'end_pos': last_tok.end_pos if last_tok else 0
        })()
        input_stream.append(eof_token)

        input_index = 0
        cst_root = ParseTreeNode(self.grammar.start_symbol)
        
        # Stack entries hold tuple (symbol_name_or_node, is_node)
        # We push node objects directly to build derivation tree
        stack = ["$", cst_root]

        step_counter = 0
        max_steps = 2000

        while len(stack) > 0 and step_counter < max_steps:
            step_counter += 1
            top = stack[-1]
            curr_token = input_stream[input_index] if input_index < len(input_stream) else eof_token
            lookahead_terminal = token_to_terminal(curr_token)

            # Format current stack representation
            stack_repr = [item.symbol if isinstance(item, ParseTreeNode) else str(item) for item in reversed(stack)]
            input_repr = [t.value if t.type != TokenType["EOF"] else "$" for t in input_stream[input_index:]]

            # 1. Check EOF match
            if top == "$":
                if lookahead_terminal == EOF_SYMBOL:
                    steps.append({
                        "step": step_counter,
                        "stack": stack_repr,
                        "input": input_repr,
                        "lookahead": "$",
                        "action": "Accept (Parsing Completed)",
                        "production": None,
                        "table_row": None,
                        "table_column": None,
                        "explanation": "Stack bottom '$' matches Input '$'. Program parsed successfully!"
                    })
                    stack.pop()
                    break
                else:
                    raise SyntaxError(
                        f"Unexpected input remaining after parsing completed.",
                        line=curr_token.line, column=curr_token.column,
                        found=curr_token.value
                    )

            top_node = top
            top_symbol = top_node.symbol if isinstance(top_node, ParseTreeNode) else str(top_node)

            # 2. Top is Terminal
            if self.grammar.is_terminal(top_symbol):
                if top_symbol == lookahead_terminal:
                    steps.append({
                        "step": step_counter,
                        "stack": stack_repr,
                        "input": input_repr,
                        "lookahead": lookahead_terminal,
                        "action": f"Match '{curr_token.value}'",
                        "production": None,
                        "table_row": None,
                        "table_column": None,
                        "explanation": f"Matched terminal '{top_symbol}' with input lexeme '{curr_token.value}'."
                    })
                    if isinstance(top_node, ParseTreeNode):
                        top_node.is_terminal = True
                        top_node.token = curr_token
                        top_node.line = curr_token.line
                        top_node.column = curr_token.column
                        top_node.start_pos = curr_token.start_pos
                        top_node.end_pos = curr_token.end_pos
                    
                    stack.pop()
                    input_index += 1
                else:
                    raise SyntaxError(
                        f"Syntax Error: Expected terminal '{top_symbol}', found '{curr_token.value}'",
                        line=curr_token.line, column=curr_token.column,
                        expected=top_symbol, found=curr_token.value,
                        hint=f"Ensure expected symbol '{top_symbol}' is provided."
                    )

            # 3. Top is Non-Terminal
            elif self.grammar.is_non_terminal(top_symbol):
                prod_dict = self.table.get(top_symbol, {}).get(lookahead_terminal)

                if prod_dict:
                    prod_rhs = prod_dict["rhs"]
                    prod_str = prod_dict["production_str"]

                    steps.append({
                        "step": step_counter,
                        "stack": stack_repr,
                        "input": input_repr,
                        "lookahead": lookahead_terminal,
                        "action": f"Expand {prod_str}",
                        "production": prod_str,
                        "table_row": top_symbol,
                        "table_column": lookahead_terminal,
                        "explanation": f"Lookahead '{lookahead_terminal}' selects rule M[{top_symbol}, {lookahead_terminal}] = {prod_str}."
                    })

                    stack.pop()

                    # Create CST children
                    child_nodes = []
                    if prod_rhs == [EPSILON]:
                        eps_node = ParseTreeNode(EPSILON, is_terminal=True)
                        top_node.add_child(eps_node)
                    else:
                        for sym in prod_rhs:
                            child = ParseTreeNode(sym, is_terminal=self.grammar.is_terminal(sym))
                            top_node.add_child(child)
                            child_nodes.append(child)

                        # Push onto stack in REVERSE order
                        for child in reversed(child_nodes):
                            stack.append(child)
                else:
                    # Parse Table cell is empty
                    valid_lookaheads = [t for t, p in self.table.get(top_symbol, {}).items() if p is not None]
                    raise SyntaxError(
                        f"Syntax Error: M[{top_symbol}, {lookahead_terminal}] is EMPTY. Unexpected token '{curr_token.value}'.",
                        line=curr_token.line, column=curr_token.column,
                        expected=", ".join(valid_lookaheads), found=curr_token.value,
                        hint=f"No valid LL(1) rule exists to expand non-terminal '{top_symbol}' when seeing lookahead '{lookahead_terminal}'."
                    )

        # Convert Concrete Parse Tree to AST
        ast_root = self.convert_cst_to_ast(cst_root)

        return {
            "cst_root": cst_root,
            "ast_root": ast_root,
            "steps": steps,
            "grammar": self.grammar.to_dict(),
            "first": self.first_sets,
            "follow": self.follow_sets,
            "parse_table": self.table,
            "conflicts": self.conflicts
        }

    def convert_cst_to_ast(self, cst_node):
        """
        Transforms Concrete Parse Tree (CST) into a clean Abstract Syntax Tree (AST).
        """
        if not cst_node:
            return None

        # Program -> StatementList
        if cst_node.symbol == "Program":
            stmts = []
            if cst_node.children:
                stmts = self._collect_statements(cst_node.children[0])
            first_child = stmts[0] if stmts else None
            return ProgramNode(
                statements=stmts,
                line=first_child.line if first_child else 1,
                column=first_child.column if first_child else 1
            )

        return None

    def _collect_statements(self, stmt_list_node):
        stmts = []
        curr = stmt_list_node
        while curr and curr.symbol == "StatementList" and curr.children:
            if len(curr.children) >= 2:
                stmt_node = curr.children[0]
                ast_stmt = self._parse_statement_cst(stmt_node)
                if ast_stmt:
                    stmts.append(ast_stmt)
                curr = curr.children[1]
            else:
                break
        return stmts

    def _parse_statement_cst(self, stmt_node):
        if not stmt_node or not stmt_node.children:
            return None

        child = stmt_node.children[0]

        # Declaration -> Type ID = Expression ;
        if child.symbol == "Declaration":
            type_node = child.children[0]
            id_node = child.children[1]
            expr_node = child.children[3]
            semi_node = child.children[4]

            type_str = type_node.children[0].symbol if type_node.children else "int"
            var_name = id_node.token.value if id_node.token else "x"
            init_expr = self._parse_expression_cst(expr_node)

            return VarDeclNode(
                data_type=type_str,
                var_name=var_name,
                initializer=init_expr,
                line=id_node.line, column=id_node.column,
                start_pos=id_node.start_pos, end_pos=semi_node.end_pos
            )

        # Assignment -> ID = Expression ;
        elif child.symbol == "Assignment":
            id_node = child.children[0]
            expr_node = child.children[2]
            semi_node = child.children[3]

            var_name = id_node.token.value if id_node.token else "x"
            expr = self._parse_expression_cst(expr_node)

            return AssignmentNode(
                var_name=var_name,
                expression=expr,
                line=id_node.line, column=id_node.column,
                start_pos=id_node.start_pos, end_pos=semi_node.end_pos
            )

        # IfStatement -> if ( Condition ) { StatementList } ElseClause
        elif child.symbol == "IfStatement":
            if_tok = child.children[0]
            cond_node = child.children[2]
            stmt_list = child.children[5]
            else_clause = child.children[7] if len(child.children) > 7 else None

            cond_expr = self._parse_condition_cst(cond_node)
            then_stmts = self._collect_statements(stmt_list)
            then_block = BlockNode(then_stmts, line=if_tok.line, column=if_tok.column)

            else_block = None
            if else_clause and len(else_clause.children) >= 4:
                else_stmts = self._collect_statements(else_clause.children[2])
                else_block = BlockNode(else_stmts, line=else_clause.line, column=else_clause.column)

            return IfStatementNode(
                condition=cond_expr,
                then_block=then_block,
                else_block=else_block,
                line=if_tok.line, column=if_tok.column,
                start_pos=if_tok.start_pos, end_pos=if_tok.end_pos
            )

        return None

    def _parse_condition_cst(self, cond_node):
        # Condition -> Expression RelOp Expression
        left_expr = self._parse_expression_cst(cond_node.children[0])
        rel_op = cond_node.children[1].children[0].symbol
        right_expr = self._parse_expression_cst(cond_node.children[2])

        return BinaryOpNode(
            operator=rel_op,
            left=left_expr,
            right=right_expr,
            line=left_expr.line, column=left_expr.column
        )

    def _parse_expression_cst(self, expr_node):
        # Expression -> Term ExpressionPrime
        term_node = expr_node.children[0]
        expr_prime = expr_node.children[1]

        left = self._parse_term_cst(term_node)
        return self._parse_expression_prime_cst(left, expr_prime)

    def _parse_expression_prime_cst(self, left, expr_prime_node):
        # ExpressionPrime -> + Term ExpressionPrime | - Term ExpressionPrime | ε
        if not expr_prime_node or not expr_prime_node.children or expr_prime_node.children[0].symbol == EPSILON:
            return left

        op_sym = expr_prime_node.children[0].symbol
        term_node = expr_prime_node.children[1]
        next_prime = expr_prime_node.children[2]

        right = self._parse_term_cst(term_node)
        bin_op = BinaryOpNode(
            operator=op_sym,
            left=left,
            right=right,
            line=left.line, column=left.column
        )
        return self._parse_expression_prime_cst(bin_op, next_prime)

    def _parse_term_cst(self, term_node):
        # Term -> Factor TermPrime
        factor_node = term_node.children[0]
        term_prime = term_node.children[1]

        left = self._parse_factor_cst(factor_node)
        return self._parse_term_prime_cst(left, term_prime)

    def _parse_term_prime_cst(self, left, term_prime_node):
        # TermPrime -> * Factor TermPrime | / Factor TermPrime | ε
        if not term_prime_node or not term_prime_node.children or term_prime_node.children[0].symbol == EPSILON:
            return left

        op_sym = term_prime_node.children[0].symbol
        factor_node = term_prime_node.children[1]
        next_prime = term_prime_node.children[2]

        right = self._parse_factor_cst(factor_node)
        bin_op = BinaryOpNode(
            operator=op_sym,
            left=left,
            right=right,
            line=left.line, column=left.column
        )
        return self._parse_term_prime_cst(bin_op, next_prime)

    def _parse_factor_cst(self, factor_node):
        # Factor -> ID | NUMBER | ( Expression )
        child = factor_node.children[0]
        if child.symbol == "ID":
            tok = child.token
            return IdentifierNode(
                name=tok.value if tok else "x",
                line=tok.line if tok else 1, column=tok.column if tok else 1,
                start_pos=tok.start_pos if tok else 0, end_pos=tok.end_pos if tok else 0
            )
        elif child.symbol == "NUMBER":
            tok = child.token
            val_str = tok.value if tok else "0"
            val = float(val_str) if '.' in val_str else int(val_str)
            dt = "float" if '.' in val_str else "int"
            return LiteralNode(
                value=val, data_type=dt,
                line=tok.line if tok else 1, column=tok.column if tok else 1,
                start_pos=tok.start_pos if tok else 0, end_pos=tok.end_pos if tok else 0
            )
        elif child.symbol == "(":
            expr_node = factor_node.children[1]
            return self._parse_expression_cst(expr_node)

        return LiteralNode(0, "int")
