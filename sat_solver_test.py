import unittest
import sat_solver as sats


class TestSatSolver(unittest.TestCase):

    def test_simplify_by_unit_clause(self):
        phi = sats.And(sats.Or("p", "q"), sats.Or("q", sats.Not("p")))
        sim_phi = sats.simplify_by_unit_clause(phi, "p")
        self.assertEqual(sim_phi.flatten(), "q")

        phi = sats.And(sats.Or("p", sats.Not("q")))
        sim_phi = sats.simplify_by_unit_clause(phi, "p")
        self.assertEqual(sim_phi.flatten(), sats.T)

        phi = sats.And(sats.Or("p", sats.Not("q")))
        sim_phi = sats.simplify_by_unit_clause(phi, sats.Not("q"))
        self.assertEqual(sim_phi.flatten(), sats.T)

        phi = sats.And(sats.Or("p", sats.Not("q")))
        sim_phi = sats.simplify_by_unit_clause(phi, sats.Not("p"))
        self.assertEqual(sim_phi.flatten(), sats.Not("q"))

        phi = sats.And("p", "q")
        sim_phi = sats.simplify_by_unit_clause(phi, sats.Not("p"))
        self.assertEqual(sim_phi.flatten(), sats.F)

        phi = sats.And(sats.Or("p"), sats.Not("q"))
        sim_phi = sats.simplify_by_unit_clause(phi, "p")
        self.assertEqual(sim_phi.flatten(), sats.Not("q"))

        phi = sats.And(sats.Or("p"), sats.Not("q"))
        sim_phi = sats.SAT_solve(phi)
        self.assertEqual(sim_phi, [sats.Variable("p"), sats.Not("q")])



if __name__ == '__main__':
    unittest.main()
