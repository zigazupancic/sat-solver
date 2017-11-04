""" Reads and writes files in DIMACS format. """

from boolean import *
import warnings


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
                clause = [str(var) if var > 0 else Not(str(-var)) for var in clause]
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
    output_variables = []
    if tf_form:
        for var, var_value in variables:
            output_variables.append(var if var_value else "-" + var)
    else:
        for var in variables:
            output_variables.append("-" + var.x.x if isinstance(var, Not) else var.x)
    with open(filename, "w") as file:
        if len(variables) == 0:
            file.write("0")
        else:
            file.write(" ".join(output_variables))


def dimacs_read_output(input_file_name, output_file_name):
    """
    Reads a DIMACS output file and returns a dictionary of variables (constructed according to the file).
    :param input_file_name: name of the input DIMACS file.
    :param output_file_name: name of the DIMACS file.
    :return: dictionary, key = name of the variable, value = boolean value of the variable
    """
    variables = {}
    num_var = 0
    with open(input_file_name) as file:
        for line in file:
            line = line.strip()
            if line == "" or line[0].lower() == "c":
                continue
            elif line[0].lower() == "p":
                p, cnf, num_var, num_clauses = line.split()
                num_var, num_clauses = int(num_var), int(num_clauses)
    with open(output_file_name) as file:
        for line in file:
            line = line.strip()
            if line == "" or line[0].lower() == "c":
                continue
            else:
                read_vars = [int(var) for var in line.split()]
                for i in range(1, num_var+1):
                    if i not in read_vars and -i not in read_vars:
                        read_vars.append(i)
                for var in read_vars:
                    if var > 0:
                        variables[str(var)] = True
                    else:
                        variables[str(-var)] = False
    return variables
