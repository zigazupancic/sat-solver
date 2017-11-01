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
                    simpl_phi.append(Or(temp_conj))
                else:
                    simpl_phi.append(temp_conj[0])
        elif conjunct == not_l:
            return F
        elif conjunct != l:
            simpl_phi.append(conjunct)
    if len(simpl_phi) == 0:
        return T
    return And(*simpl_phi)


def find_unit_clause(phi):
    """
    Finds the first unit clause in formula phi. If phi has no unit clauses it returns False.
    :param phi: formula
    :return: unit clause or False if there is no unit clause in the formula
    """
    i = 0   # Assuming phi.terms is not empty, otherwise returns False
    while i < len(phi.listing()):
        if isinstance(phi.listing()[i], Variable):
            return phi.listing()[i]
        else:
            i += 1
    return False


def choose_literal(phi):
    """
    This function chooses a literal in case the given formula has no unit clauses.
    :param phi: formula
    :return: a literal
    """
    if len(phi.listing()) > 0:
        if len(phi.listing()[0].listing()) > 0:
            return phi.listing()[0].listing()[0]        # Assuming phi.terms is not empty
        else:
            return phi.listing[0]
    else:
        return False


def SAT_solve(phi, val=[]):
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
        if len(phi.terms) == 0:
            return val
        l = find_unit_clause(newphi)
        if l != False:                  # If we have a unit clause in the formula
            newphi_= simplify_by_unit_clause(newphi, l)
            if newphi_ == F:            # There is an empty clause
                return "unsatisfiable"
            elif newphi_ == T:          # We have found a valuation
                valuation = valuation.append(l)
                return valuation
            else:
                valuation = valuation.append(l)
        else:                           # If there is no unit clause in the formula
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
                    valuation = valuation_.append(l)    # If we can simplify by Not(l)
            else:
                valuation = valuation_.append(l)        # If we can simplify by l
        newphi = newphi_


if __name__ == "__main__":
    phi = dimacs_rw.dimacs_read(sys.argv[1])
    solution = SAT_solve(phi)
