# DPLL SAT Solver

SAT solver using the Davis–Putnam–Logemann–Loveland algorithm implemented in Python 3. 

To run use an instances file as input to the program:
```
python3 dpll.py small_instances.txt
```

## File Syntax

### Instances:
Each clause is written in single line with literals from 0 to N that are negated with a prepending '-'.
```
2 -0 4 -3 -1
```
SAT problems are divided by a newline between the clauses.
```
-0 -1
0 1

-0 -1 3
0 -2 3
2 -1 0
```
### Assignments
Each line denotes the positive or negative assignments to the literals for the corresponding SAT problem in the instances file.
```
-0 1
0 -1 2 3
```




