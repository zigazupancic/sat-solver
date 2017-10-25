from boolean import *


def simplify_by_unit_clause(phi, l):
    """
    :param phi: formula
    :param l: unit clause
    :return: simplified formula phi
    """
    simpl_phi = phi.simplify()
    if not isinstance(simpl_phi, Multi):
        if simpl_phi == l:
            return "T"
        elif simpl_phi == Not(l):
            return "F"
        else:
            return simpl_phi
    else:
        temp_clauses = []
        for clause in simpl_phi.terms:
            sbuc = simplify_by_unit_clause(clause, l)
            temp_clauses.append(simplify_by_unit_clause(clause, l))
        return phi.getClass()(*temp_clauses).simplify()
