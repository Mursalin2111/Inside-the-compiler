"""
LL(1) Parsing Table Construction & Conflict Detector.
"""

from .grammar import EPSILON, EOF_SYMBOL
from .first_follow import first_of_sequence

def build_ll1_table(grammar, first_sets_dict, follow_sets_dict):
    """
    Constructs the 2D LL(1) Parsing Table M[NonTerminal, Terminal] and detects conflicts.
    """
    first_sets = {k: set(v) for k, v in first_sets_dict.items()}
    follow_sets = {k: set(v) for k, v in follow_sets_dict.items()}

    terminals_with_eof = list(grammar.terminals) + [EOF_SYMBOL]
    
    # Initialize empty 2D table structure
    table = {nt: {t: None for t in terminals_with_eof} for nt in grammar.non_terminals}
    conflicts = []

    for prod in grammar.productions:
        lhs = prod.lhs
        rhs = prod.rhs
        rhs_first = first_of_sequence(rhs, first_sets)

        # Rule 1: For each terminal a in FIRST(rhs) - {ε}, add prod to M[lhs, a]
        for a in rhs_first - {EPSILON}:
            if a in terminals_with_eof:
                existing = table[lhs][a]
                if existing is not None and existing["id"] != prod.id:
                    conflicts.append({
                        "non_terminal": lhs,
                        "terminal": a,
                        "existing_production": existing["production_str"],
                        "conflicting_production": prod.to_dict()["production_str"],
                        "message": f"LL(1) Conflict at M[{lhs}, {a}]: Multi-entry rule conflict between '{existing['production_str']}' and '{prod.to_dict()['production_str']}'."
                    })
                else:
                    table[lhs][a] = prod.to_dict()

        # Rule 2: If ε in FIRST(rhs), for each terminal b in FOLLOW(lhs), add prod to M[lhs, b]
        if EPSILON in rhs_first:
            for b in follow_sets[lhs]:
                if b in terminals_with_eof:
                    existing = table[lhs][b]
                    if existing is not None and existing["id"] != prod.id:
                        conflicts.append({
                            "non_terminal": lhs,
                            "terminal": b,
                            "existing_production": existing["production_str"],
                            "conflicting_production": prod.to_dict()["production_str"],
                            "message": f"LL(1) Conflict at M[{lhs}, {b}]: Multi-entry rule conflict involving ε-production."
                        })
                    else:
                        table[lhs][b] = prod.to_dict()

    return {
        "terminals": terminals_with_eof,
        "non_terminals": grammar.non_terminals,
        "table": table,
        "conflicts": conflicts
    }
