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


def SAT_solve(phi):
    """
    Main function which takes a formula and computes a satisfying valuation or returns "False" if it is not satisfiable.
    :param phi: formula
    :return: satisfying valuation or False
    """
    valuation = {}                      # Slovar z valuacijami
    if len(phi.terms) = 0:
        return True                     # Kaj narediti v tem primeru?
    rep = True                          # V spremenljivki rep se bo kasneje skrival pogoj za
    phis = [phi]                        # Seznam s spremembami formule
    newphi = phi
    while rep:
        l = find_unit_clause(newphi)
        if l != False:                  # Če imamo unit clause
            newphi_= simplify_by_unit_clause(newphi, l)
            if newphi_ == F:            # Nek clause se poenostavi v F
                #reset valuation
            elif newphi_ == T:          # Našli smo valuacijo
                if isinstance(l, Not):
                    valuation[Not(l).simplify()] = F
                else:
                    valuation[l] = T
                return valuation
            else:
                if isinstance(l, Not):
                    valuation[Not(l).simplify()] = F
                else:
                    valuation[l] = T
                newphi = newphi_          # Za zadnjo poenostavljeno formulo vzamemo newphi_
                phis.append(newphi)
                continue
        else:                           # Če nimamo unit clausa
            l = choose_literal(newphi)  # Izberemo neko spremenljivko
            newphi_ = simplify_by_unit_clause(newphi, l)
            if newphi_ == F:            # Če poenostavljanje z l vrne fail
                newphi_ = simplify_by_unit_clause(newphi, Not(l))       # Poskusimo z not(l)
                if newphi_ == F:        # Če tudi to vrne fail
                    # reset valuation
                elif newphi_ == T:      # Če dobimo valuacijo
                    #if isinstance(l, Not):
                    #    valuation[Not(l).simplify()] = F
                    #else:
                    valuation[l] = T
                    return valuation
                else:                   # Sicer
                    #if isinstance(l, Not):
                    #    valuation[Not(l).simplify()] = F
                    #else:
                    valuation[l] = T
                    newphi = newphi_
                    phis.append(newphi)
                    continue            # V zapiskih piše, da mora na tem mestu vrniti unsatisfiable?

# Ideja: popravke v valuation označujemo z spremenljivko, ki smo jo na zadnje izbrali v koraku 4. Hkrati izbire na tem
# koraku shranjujemo v nek list, da vedno lahko najdemo zadnjo izbiro.