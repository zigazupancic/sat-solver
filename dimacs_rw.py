""" Reads and writes files in DIMACS format. """

from boolean import *
import warnings


def dimacs_reader(file_name):
    """
    Reads a DIMACS file and returns a formula (constructed according to the file).
    :param file_name: path of the DIMACS file
    :return: formula in CNF
    """
    clauses = []
    num_var, num_clauses = 0, 0
    with open(file_name) as file:
        ln_cnt = 0
        for line in file:
            ln_cnt += 1
            line = line.strip()
            if line == "" or line[0].lower() == "c":
                continue
            elif line[0].lower() == "p":
                try:
                    p, cnf, num_var, num_clauses = line.split()
                    num_var, num_clauses = int(num_var), int(num_clauses)
                except ValueError:
                    print("Error in line {}. Line should be of the form: 'p cnf num_var num_clauses', where num_var"
                          " is the number of arguments and num_clauses is the number of clauses. \n"
                          "Actual line is '{}'.".format(ln_cnt, line))
                    raise
            else:
                try:
                    clause = [int(var) for var in line.split()][:-1]
                except ValueError:
                    print("Error in line {}. Line should be of the form: 'cl_1 cl_2 ... cl_n', where cl_i"
                          " is the name of a variable (an integer). \n"
                          "Actual line is '{}'.".format(ln_cnt, line))
                    raise
                clause = ["x{}".format(var) if var > 0 else Not("x{}".format(-var)) for var in clause]
                clauses.append(Or(*clause))
    if num_clauses != len(clauses):
        warnings.warn("Number of clauses is not {}, but {}!".format(num_clauses, len(clauses)))
    return And(*clauses)
