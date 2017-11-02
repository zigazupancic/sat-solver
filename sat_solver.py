from boolean import *
import dimacs_rw
import sys


def simplify_by_unit_clause(phi, l):
    """
    :param phi: formula
    :param l: unit clause
    :return: simplified formula phi by l
    """
    not_l = Not(l).simplify()
    simpl_phi = []
    for conjunct in phi.terms:
        temp_conj = []
        if isinstance(conjunct, Or):
            for clause in conjunct.terms:
                if clause == l:
                    temp_conj = T
                    break
                elif clause != not_l:
                    temp_conj.append(clause)
            if temp_conj != T:
                if len(temp_conj) > 1:
                    simpl_phi.append(Or(*temp_conj))
                else:
                    simpl_phi.append(temp_conj[0])
        elif conjunct == not_l:
            return F
        elif conjunct != l:
            simpl_phi.append(conjunct)
    if len(simpl_phi) == 0:
        return T
    return And(*simpl_phi)


def find_unit_clauses(phi):
    """
    Finds unit clauses in formula phi. If phi has no unit clauses it returns False.
    :param phi: formula
    :return: list of unit clauses or False if there is no unit clause in the formula
    """
    unit_clauses = []
    phi = phi.flatten()
    for clause in phi.terms:
        clause = clause.flatten()
        if (isinstance(clause, Variable) or isinstance(clause, Not)) and clause not in unit_clauses:
            unit_clauses.append(clause)
    return unit_clauses


def choose_literal(phi):
    """
    This function chooses a literal in case the given formula has no unit clauses.
    :param phi: formula
    :return: a literal
    """
    phi = phi.flatten()
    if isinstance(phi, Multi):
        x = next(iter(phi.terms))
        x = x.flatten()
        if isinstance(x, Multi):
            x = next(iter(x.terms))
        return x
    return phi


def SAT_solve(phi, val=set()):
    """
    Main function which takes a formula and computes a satisfying valuation or returns "False" if it is not satisfiable.
    :param phi: formula
    :param val: list of formulas (variables or nots)
    :return: satisfying valuation or "unsatisfiable"
    """
    valuation = val                     # List with valuations
    rep = True                          # Variable rep will later contain stopping condition for while loop
    newphi = phi
    while rep:
        if newphi == T:
            return val
        if newphi == F:
            return "unsatisfiable"
        unit_clauses = find_unit_clauses(newphi)
        for l in unit_clauses:                 # If we have a unit clause in the formula
            newphi_= simplify_by_unit_clause(newphi, l)
            if newphi_ == F:            # There is an empty clause
                return "unsatisfiable"
            elif newphi_ == T:          # We have found a valuation
                valuation.add(l)
                return valuation
            else:
                valuation.add(l)
            newphi = newphi_
        l = choose_literal(newphi)  # We choose a literal l to simplify the formula by
        newphi_ = simplify_by_unit_clause(newphi, l)
        valuation_ = SAT_solve(newphi_, valuation)
        if valuation_ == "unsatisfiable":           # If simplifying by l fails
            l = Not(l).simplify()
            newphi_ = simplify_by_unit_clause(newphi, l)
            valuation_ = SAT_solve(newphi_, valuation)
            if valuation_ == "unsatisfiable":       # If simplifying by Not(l) fails
                return "unsatisfiable"
            else:
                valuation_.add(l)    # If we can simplify by Not(l)
                valuation = valuation_
        else:
            valuation_.add(l)        # If we can simplify by l
            valuation = valuation_
        newphi = newphi_


if __name__ == "__main__":
    phi = dimacs_rw.dimacs_read(sys.argv[1])
    solution = SAT_solve(phi)
    if len(sys.argv) > 1:
        out_file_name = sys.argv[2]
    else:
        out_file_name = sys.argv[1] + "_output"
    dimacs_rw.dimacs_write(list(solution), out_file_name)
