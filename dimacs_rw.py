""" Reads and writes files in DIMACS format. """

from boolean import *
import warnings
import os


def dimacs_read(file_name):
    """
    Reads a DIMACS file and returns a formula (constructed according to the file).
    :param file_name: name of the DIMACS file.
    :return: formula in CNF.
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


def dimacs_write(variables, filename="sat_output", tf_form=False):
    """
    Saves variable values in a file.
    :param variables: list of variables that are true if tf_form is False, otherwise pairs of (`var`, `var_value`),
                      where `var` is the name of the variable and `var_value` its boolean value.
    :param filename: name of the desired output file.
    :param tf_form: type of input variables.
    :return: name of the output file.
    """
    fn_num = 0
    while os.path.isfile(filename):
        fn_num += 1
        filename = filename + str(fn_num)
    output_variables = []
    if tf_form:
        for var, var_value in variables:
            output_variables.append(var[1:] if var_value else "-" + var[1:])
    else:
        for var in variables:
            output_variables.append("-" + var.x.x[1:] if isinstance(var, Not) else var[1:])
    with open(filename, "w") as file:
        file.write(" ".join(output_variables))
