# SAT Solver using the DPLL algorithm

import random
import sys
import time
import copy
from collections import OrderedDict


# Clause consists of a set of symbols, each of which is negated or not. 
class Clause:
    def __init__(self):
        pass

    def from_str(self, s):
        s = s.split()
        self.symbols = {}
        for token in s:
            if token[0] == "-":
                sign = -1
                symbol = token[1:]
            else:
                sign = 1
                symbol = token
            self.symbols[symbol] = sign

    def __str__(self):
        tokens = []
        for symbol,sign in self.symbols.items():
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            tokens.append(token)
        return " ".join(tokens)

# SAT instance consists of a set of CNF clauses. All clauses
# must be satisfied in order for the SAT instance to be satisfied.
class SatInstance:
    def __init__(self):
        pass

    def from_str(self, s):
        self.symbols = set()
        self.clauses = []
        for line in s.splitlines():
            clause = Clause()
            clause.from_str(line)
            self.clauses.append(clause)
            for symbol in clause.symbols:
                self.symbols.add(symbol)
        self.symbols = sorted(self.symbols)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s

	# Returns True or False if the instance is satisfied
    def is_satisfied(self, assignment):
        # Loop through every clause in instance
        for clause in self.clauses: 
            solve = False # Flag for if clause has been satisfied
            # Loop through every symbol in clause
            for symbol in clause.symbols:
                # If the assignment makes the symbol true -> the whole clause is true
                try:
                    if(clause.symbols[symbol] == assignment[symbol]):
                        solve = True
                # Symbol is not found in assignment
                except:
                    return False

            # If the clause was never solved -> the assignment fails
            if(solve == False):
                return False

        # All clauses have been solved
        return True

    # Finds a unit clause within an instance.
    # Returns the unit clause symbol and value dictionary entry if found or False if no unit clauses found
    def findUnitClause(self):
        for clause in self.clauses:
            # Look for clauses of length 1
            if(len(clause.symbols) == 1):
                return {next(iter(clause.symbols.keys())): next(iter(clause.symbols.values()))}
        return False # Return False if no unit clauses are found

    # Searches the instance for a clause that is the negative of the unit clause. If found then the instance is unsatisfiable
    # Returns True if no such clause is found, False if it is found
    def noOppositeUnitClause(self, symbol):
        key = next(iter(symbol.keys())) # Unit clause key
        value = next(iter(symbol.values())) # Unit clause value

        for clause in self.clauses:
            # Find unit clauses
            if(len(clause.symbols) == 1):
                # Check if key matches
                if(next(iter(clause.symbols.keys())) == key):
                    # Check if value if opposite
                    if(next(iter(clause.symbols.values())) != value):
                        return False # Opposite clause found
        # No opposite unit clause was found
        return True 

    
        
    # Reduces the clauses by the unit clause.
    # If the matching key and value are found in a clause then the clause is true and can be removed from the instance
    # If the matching key but opposite value is found then that symbol can be removed from the clause
    def simplify(self, symbol):
        key = next(iter(symbol.keys())) # Unit clause key
        value = next(iter(symbol.values())) # Unit clause value

        delete = [] # List of clauses to remove
        index = 0

        for clause in self.clauses:
            try:
                # Clause has the same symbol that is being simplified thus is true and can be removed 
                if(clause.symbols[key] == value):
                    delete = delete + [index] # Add the clauses index    
                    index = index - 1 # While deleting, when the above indexed clauses is removed all other clauses go down an index value                

                # Clause has the opposite symbol that is being simplified thus the symbol can be removed from the clause
                else:
                    clause.symbols.pop(key, None)
         
            # Clause does not have the symbol so skip it
            except:
                pass

            index = index+1
        
        # Delete all the solved clauses
        for i in delete:
            del self.clauses[i]

        return self
 

# Finds a satisfying assignment to a SAT instance,
def solve_dpll(instance):
    c = copy.deepcopy(instance)

    assignment = {}
    assingment = dpllRecurse(instance, assignment) # Get the assignment that solves the instance
    
    # Fill in the symbols that can be assigned
    for symbol in set(instance.symbols) - set(assignment.keys()):
        assignment[symbol] = 1

    assignment = dict(OrderedDict(sorted(assignment.items(), key=lambda t: int(t[0])))) # Sort the assignment dictionary by symbol

    return assignment
    


# Recursively finds the satisfying assignment
# Returns the assignment in dictionary form or False if no satisfying assignment
def dpllRecurse(instance, assignment):
    # If instance has no more clauses then all clauses have been satisfied
    if(len(instance.clauses) == 0):
        return assignment

    # Find all unit clauses in instance
    while(instance.findUnitClause()):
        unitClause = instance.findUnitClause()

        # If the instance also has the opposite unit clause (a and !a) then instance can't be solved
        if(instance.noOppositeUnitClause(unitClause) == False):
            return False
        # Add the unit clause to the assignment and simplify the instance clauses
        else:
            instance.simplify(unitClause)
            assignment[next(iter(unitClause.keys()))] = next(iter(unitClause.values()))

    # If instance has no more clauses then all clauses have been satisfied
    if(len(instance.clauses) == 0):
        return assignment

    # Loop through every symbol and try assigning it to see if it solves the instance
    for symbol in instance.symbols:
        instanceCopy = copy.deepcopy(instance) # Create copy of instance to use if positive assignment fails

        # Check if symbol is already in assignment
        if(symbol not in list(assignment.keys())): 
            # Add the positive symbol to assignment, simplify the instance and recurse on it
            assignment[symbol] = 1
            
            # If opposite clause doesn't exist
            if(instance.noOppositeUnitClause({symbol:1}) == True):
                if(dpllRecurse(instance.simplify({symbol:1}), assignment)): # Recurse with positive symbol
                    return assignment

                # If positve assignment fails try negative assignment
                else:
                    assignment[symbol] = -1
                    # If opposite clause doesn't exist
                    if(instanceCopy.noOppositeUnitClause({symbol:-1}) == True):
                        return dpllRecurse(instanceCopy.simplify({symbol:-1}), assignment) # Recurse with negative symbol   





						
def main(file):
	with open(file, "r") as input_file:
		instance_strs = input_file.read()

	instance_strs = instance_strs.split("\n\n")

	with open("assignments.txt", "w") as output_file:
		for instance_str in instance_strs:
			if instance_str.strip() == "":
				continue
			instance = SatInstance()
			instance.from_str(instance_str)
			assignment = solve_dpll(instance)
			for symbol_index, (symbol,sign) in enumerate(assignment.items()):
				if symbol_index != 0:
					output_file.write(" ")
				token = ""
				if sign == -1:
					token += "-"
				token += symbol
				output_file.write(token)
			output_file.write("\n")
        
        

   
if __name__ == "__main__":
    main(sys.argv[1])














