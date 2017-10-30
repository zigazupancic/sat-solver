from boolean import *


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
    i = 0   # Predpostavljam, da phi.terms ni prazen seznam!
    while i <= len(phi.terms):
        if isinstance(phi.terms[i], Variable):
            return phi.terms[i]
        else:
            i += 1
    return False


def choose_literal(phi):
    """
    This function chooses a literal in case the given formula has no unit clauses.
    :param phi: formula
    :return: a literal
    """
    return phi.terms[0].terms[0]


def SAT_solve(phi, val=[]):
    """
    Main function which takes a formula and computes a satisfying valuation or returns "False" if it is not satisfiable.
    :param phi: formula
    :param val: list of formulas (variables or nots)
    :return: satisfying valuation or "unsatisfiable"
    """
    valuation = val                     # Seznam z valuacijami
    rep = True                          # V spremenljivki rep se bo kasneje skrival pogoj za
    newphi=phi
    while rep:
        if len(phi.terms) == 0:
            return val
        l = find_unit_clause(newphi)
        if l != False:                  # Če imamo unit clause
            newphi_= simplify_by_unit_clause(newphi, l)
            if newphi_ == F:            # Nek clause se poenostavi v F
                return "unsatisfiable"
            elif newphi_ == T:          # Našli smo valuacijo
                valuation = valuation.append(l)
                return valuation
            else:
                valuation = valuation.append(l)
        else:                           # Če nimamo unit clausa
            l = choose_literal(newphi)  # Izberemo neko spremenljivko
            newphi_ = simplify_by_unit_clause(newphi, l)
            variables_ = SAT_solve(newphi_, variables)
            if variables_ == "unsatisfiable":
                l = Not(l).simplify()
                newphi_ = simplify_by_unit_clause(newphi, l)
                variables_=SAT_solve(newphi_, variables)
                if variables_ == "unsatisfiable":
                    return "unsatisfiable"
                else:
                    variables = variables_.append(l)
            else:
                variables = variables_.append(l)
        newphi = newphi_

