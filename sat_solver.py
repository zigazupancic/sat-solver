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
