from boolean import *
import dimacs_rw
import sys


sys.setrecursionlimit(2000)


def select_next_variable(phi):
    """
    Returns the most frequent variable in phi.
    :param phi: formula phi.
    :return: variable.
    """
    occurrences = {}
    for or_term in phi.terms:
        for variable in or_term.terms:
            if isinstance(variable, Not):
                variable = Not(variable).flatten()
            if variable in occurrences.keys():
                occurrences[variable] += 1
            else:
                occurrences[variable] = 1
    max = (0, "")
    for key in occurrences.keys():
        if occurrences[key] > max[0]:
            max = (occurrences[key], key)
    return max[1]


def simplify_by_clauses(phi, clauses):
    """
    :param phi: formula.
    :param clauses: list of clauses.
    :return: simplified formula phi by clauses.
    """
    n_clauses = set([Not(clause).simplify() for clause in clauses])
    remaining_terms = []
    for term in phi.terms:
        remaining_variables = []
        for variable in term.terms:
            if variable in clauses:
                remaining_variables = T
                break
            elif variable not in n_clauses:
                remaining_variables.append(variable)
        if remaining_variables != T and len(remaining_variables) >= 1:
            remaining_terms.append(Or(*remaining_variables))
        elif remaining_variables != T and len(remaining_variables) == 0:
            return F
    if len(remaining_terms) == 0:
        return T
    else:
        return And(*remaining_terms)


def find_unit_clauses(phi):
    """
    Finds unit clauses in formula phi.
    :param phi: formula
    :return: set of unit clauses.
    """
    unit_clauses = set()
    for clause in phi.terms:
        clause = clause.flatten()
        if isinstance(clause, Variable) or isinstance(clause, Not):
            unit_clauses.add(clause)
    return unit_clauses


def SAT_solve(phi):
    """
    Main function which takes a formula and computes a satisfying valuation or returns "False" if it is not satisfiable.
    :param phi: formula
    :return: satisfying valuation or False
    """
    valuation = set()
    if phi == T:
        return valuation
    elif phi == F:
        return False

    unit_clauses = find_unit_clauses(phi)
    if len(unit_clauses) > 0:
        phi = simplify_by_clauses(phi, unit_clauses)
        valuation.update(unit_clauses)
        if phi == T:
            return valuation
        elif phi == F:
            return False
        new_valuation = SAT_solve(phi)
        if new_valuation is False:
            return False
        valuation.update(new_valuation)
        return valuation

    var = select_next_variable(phi)

    new_phi = simplify_by_clauses(phi, {var})
    new_valuation = SAT_solve(new_phi)
    if new_valuation is False:           # If simplifying by var fails
        var = Not(var).flatten()
        phi = simplify_by_clauses(phi, {var})
        new_valuation = SAT_solve(phi)
        if new_valuation is False:
            return False
    new_valuation.add(var)
    return new_valuation


if __name__ == "__main__":
    formula_phi = dimacs_rw.dimacs_read(sys.argv[1])
    solution = SAT_solve(formula_phi)
    if len(sys.argv) > 1:
        out_file_name = sys.argv[2]
    else:
        out_file_name = sys.argv[1] + "_output"
    dimacs_rw.dimacs_write(list(solution), out_file_name)
