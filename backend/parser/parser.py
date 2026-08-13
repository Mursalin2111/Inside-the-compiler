"""
Parser Interface Wrapper.
Delegates syntax analysis to the table-driven LL(1) Parser.
"""

from .ll1_parser import LL1Parser
from .grammar import Grammar
from .first_follow import calculate_first_sets, calculate_follow_sets
from .ll1_table import build_ll1_table

class Parser:
    def __init__(self, tokens):
        self.ll1_parser = LL1Parser(tokens)

    def parse(self):
        res = self.ll1_parser.parse()
        self.parse_steps = res["steps"]
        self.cst = res["cst_root"]
        self.grammar = res["grammar"]
        self.first_sets = res["first"]
        self.follow_sets = res["follow"]
        self.parse_table = res["parse_table"]
        self.conflicts = res["conflicts"]
        return res["ast_root"]
