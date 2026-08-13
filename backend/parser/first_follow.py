"""
Fixpoint algorithms for computing FIRST and FOLLOW sets.
"""

from .grammar import EPSILON, EOF_SYMBOL

def first_of_sequence(sequence, first_sets):
    """
    Computes FIRST(X1 X2 ... Xk) given a sequence of symbols.
    """
    if not sequence or sequence == [EPSILON]:
        return {EPSILON}

    result = set()
    all_have_epsilon = True

    for symbol in sequence:
        if symbol == EPSILON:
            continue
        
        symbol_first = first_sets.get(symbol, {symbol})
        result.update(symbol_first - {EPSILON})

        if EPSILON not in symbol_first:
            all_have_epsilon = False
            break

    if all_have_epsilon:
        result.add(EPSILON)

    return result


def calculate_first_sets(grammar):
    """
    Calculates FIRST sets for all non-terminals and terminals iteratively.
    """
    first_sets = {}

    # Initialize terminals
    for t in grammar.terminals:
        first_sets[t] = {t}
    first_sets[EOF_SYMBOL] = {EOF_SYMBOL}
    first_sets[EPSILON] = {EPSILON}

    # Initialize non-terminals
    for nt in grammar.non_terminals:
        first_sets[nt] = set()

    # Iterative fixpoint calculation
    changed = True
    while changed:
        changed = False

        for prod in grammar.productions:
            lhs = prod.lhs
            rhs = prod.rhs

            rhs_first = first_of_sequence(rhs, first_sets)
            old_size = len(first_sets[lhs])
            first_sets[lhs].update(rhs_first)

            if len(first_sets[lhs]) > old_size:
                changed = True

    return {k: sorted(list(v)) for k, v in first_sets.items()}


def calculate_follow_sets(grammar, first_sets_dict):
    """
    Calculates FOLLOW sets for all non-terminals iteratively.
    """
    # Convert first_sets_dict values back to sets for set operations
    first_sets = {k: set(v) for k, v in first_sets_dict.items()}
    follow_sets = {nt: set() for nt in grammar.non_terminals}

    # Rule 1: Place EOF_SYMBOL ($) in FOLLOW(StartSymbol)
    follow_sets[grammar.start_symbol].add(EOF_SYMBOL)

    # Iterative fixpoint calculation
    changed = True
    while changed:
        changed = False

        for prod in grammar.productions:
            lhs = prod.lhs
            rhs = prod.rhs

            for i, symbol in enumerate(rhs):
                if not grammar.is_non_terminal(symbol):
                    continue

                beta = rhs[i + 1:]
                beta_first = first_of_sequence(beta, first_sets)

                # Rule 2: Add FIRST(beta) - {ε} to FOLLOW(symbol)
                old_size = len(follow_sets[symbol])
                follow_sets[symbol].update(beta_first - {EPSILON})

                # Rule 3: If ε in FIRST(beta) or beta is empty, add FOLLOW(lhs) to FOLLOW(symbol)
                if EPSILON in beta_first or not beta:
                    follow_sets[symbol].update(follow_sets[lhs])

                if len(follow_sets[symbol]) > old_size:
                    changed = True

    return {k: sorted(list(v)) for k, v in follow_sets.items()}
