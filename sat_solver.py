from boolean import *
import dimacs_rw
import heapq
import sys


sys.setrecursionlimit(2000)


def get_variable_occurrences(phi):
    """
    Returns a heap of pairs (-occurrences, variable).
    :param phi: formula phi.
    :return: heap (according to occurrences) -- max at the top.
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
    occurrences_heap = []
    for key in occurrences.keys():
        occurrences_heap.append((-occurrences[key], key))
    heapq.heapify(occurrences_heap)
    return occurrences_heap


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


def SAT_solve(phi, valuation=set(), variable_occurrences=None):
    """
    Main function which takes a formula and computes a satisfying valuation or returns "False" if it is not satisfiable.
    :param phi: formula
    :param valuation: list of formulas (variables or nots)
    :param variable_occurrences: heap of pairs (-occurrences, variable)
    :return: satisfying valuation or "unsatisfiable"
    """
    if variable_occurrences is None:
        variable_occurrences = get_variable_occurrences(phi)
    while 1:
        if phi == T:
            return valuation
        elif phi == F:
            return "unsatisfiable"

        unit_clauses = find_unit_clauses(phi)
        if len(unit_clauses) > 0:
            phi = simplify_by_clauses(phi, unit_clauses)
            valuation.update(unit_clauses)
            if phi == T:
                return valuation
            elif phi == F:
                return "unsatisfiable"
            continue

        try:
            var = heapq.heappop(variable_occurrences)[1]  # We choose a literal var to simplify the formula by
        except IndexError:
            return valuation
        while var in valuation or Not(var).flatten() in valuation:
            try:
                var = heapq.heappop(variable_occurrences)[1]
            except IndexError:

                return valuation

        new_phi = simplify_by_clauses(phi, [var])
        new_valuation = valuation.copy()
        new_variable_occurrences = variable_occurrences[:]
        new_valuation = SAT_solve(new_phi, new_valuation, new_variable_occurrences)
        if new_valuation == "unsatisfiable":           # If simplifying by var fails
            var = Not(var).flatten()
            phi = simplify_by_clauses(phi, [var])
            valuation.add(var)
            valuation = SAT_solve(phi, valuation, variable_occurrences)
            if valuation == "unsatisfiable":       # If simplifying by Not(var) fails
                return "unsatisfiable"
        else:
            variable_occurrences = new_variable_occurrences
            valuation = new_valuation.copy()        # If we can simplify by var
            valuation.add(var)
            phi = new_phi
        phi.flatten().simplify()


if __name__ == "__main__":
    formula_phi = dimacs_rw.dimacs_read(sys.argv[1])
    solution = SAT_solve(formula_phi)
    if len(sys.argv) > 1:
        out_file_name = sys.argv[2]
    else:
        out_file_name = sys.argv[1] + "_output"
    dimacs_rw.dimacs_write(list(solution), out_file_name)
