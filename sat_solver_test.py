import sat_solver as sats

phi = sats.And(sats.Or("p", "q"), sats.Or("q", sats.Not("p")))
print(phi)
sim_phi = sats.simplify_by_unit_clause(phi, 'p')
print(str(sim_phi.simplify()))
print(sats.simplify_by_unit_clause(sats.Not("p"), "p"))
