import unittest
import sat_solver as sats
import dimacs_rw
import os


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

    def test_sat_solve(self):
        input_fn = os.path.join("examples", "sudoku_easy.txt")
        output = os.path.join("examples", "sudoku_easy_out.txt")
        phi = dimacs_rw.dimacs_read(input_fn)
        solution = sats.SAT_solve(phi)
        dimacs_rw.dimacs_write(list(solution), output)
        sol = dimacs_rw.dimacs_read_output(output)
        self.assertTrue(phi.evaluate(sol))


if __name__ == '__main__':
    unittest.main()
