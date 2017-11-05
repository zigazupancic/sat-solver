# SAT Solver
Project for Logic in CS course.

### Authors:
* Živa Urbančič
* Žiga Zupančič

## Basic instructions:
To run our SAT solver one should type

``` python sat_solver.py input_file_name.txt output_file_name.txt```

in command-line. Here `input_file_name.txt` is the name of the file containing the formula, which we want to find valuation for, in Dimacs format, and `output_file_name.txt` is the name of the output file. We added an example of input file: **ne_obstaja_se.txt** in folder **examples**. Therefore, to run SAT solver on this file one would type

``` python sat_solver.py examples/ne_obstaja_se.txt examples/ne_obstaja_se_out.txt```.

Your final source code should reside on your repository, which should contain instructions for running your code in a file README.md. Include in this file the command-line command needed to execute your code on an input file.

## Enivronment:
Since we worked with propositional formulas, we introduced a new class `Formula` in **boolean.py**. We took this file from the [repository of our course](https://github.com/jaanos/LVR)(folder 'satsolver'). It contains three subclasses `Variable`, `Not` and `Multi` -- class `Multi` is further divided into subclasses `And` and `Or` -- and basic properties and functions we needed for further use.

## Working with files:
SAT solver will take input from a file ([cnf formula](https://en.wikipedia.org/wiki/Conjunctive_normal_form) in [Dimacs format](http://www.satcompetition.org/2009/format-benchmarks2009.html)) and will save output in a file. Functions we use for working with input and output files in Dimacs format are contained in **dimacs_rw.py**. These functions are:
* **dimacs_read(file_name)**: the function takes the name of the input file with a formula in Dimacs format as input and returns an object of type *Formula* from *boolean.py*.
* **dimacs_write(variables, filename, tf_form = False)**: parameter tf_form indicates how are other parameters given. If tf_form is True, variables is a list of pairs (`var`, `var_value`), where `var` is the name of the variable and `var_value` its boolean value. If tf_form is False, variables is a list of variables that are true. The function saves variable values in a file named *filename*.
* **dimacs_read_output(input_file_name, output_file_name)**: This function reads a Dimacs output file and returns a dictionary of variables (constructed according to the file). In case output file does not contain all variables the function also reads the number of variables from original input file.

## SAT solver:
The main program is **sat_solver.py**. It consists of four functions, namely:
* **def select_next_variable(phi)**: We needed this function when we were choosing which variable we will assume to hold next. It is given a formula phi as a parameter and it returns the most frequent variable in phi.
* **def simplify_by_clauses(phi, literals)**: This function takes a formula `phi` and a list of literals as a parameter and it simplifies phi accordigly. (I.e. it assumes all formulas `l` in `literals` hold. It removes the clauses containing such formulas `l` and it removes all negations `Not(l)`from the remaining clauses.)
* **def find_unit_clauses(phi)**: Given a formula `phi`it returns a set of unit clauses in `phi`.
* **def SAT_solve(phi)**: Main function which takes a formula `phi` and computes a satisfying valuation or returns `False` if it is not satisfiable. It is based on [DPLL algorithm](https://en.wikipedia.org/wiki/DPLL_algorithm).

We also added **`__main__`** function so that our sat solver can be easily used.
    


