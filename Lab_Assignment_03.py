# Lab Assignment 03-  Random k-SAT Problem Generation and Solving Using Non-Classical Search Algorithms



import random

# -------------------------
# 1. Random k-SAT Generator
# -------------------------
def generate_k_sat(k, m, n):
    """
    Generate a random k-SAT formula.
    Parameters:
        k : int : number of literals per clause
        m : int : number of clauses
        n : int : number of variables
    Returns:
        formula : list of clauses, where each clause is a list of integers
    """
    formula = []
    while len(formula) < m:
        clause = []
        while len(clause) < k:
            var = random.randint(1, n)  # choose a random variable
            if var not in [abs(x) for x in clause]:  # ensure distinct variables in a clause
                if random.random() < 0.5:  # randomly decide if literal is positive or negative
                    clause.append(var)
                else:
                    clause.append(-var)
        formula.append(clause)  # add the clause to the formula
    return formula

# ----------------------------------
# 2. Heuristic Functions
# ----------------------------------
def heuristic_unsatisfied_clauses(state, formula):
    """
    Count the number of clauses that are not satisfied by the current state.
    Lower value indicates a better solution.
    """
    unsat = 0
    for clause in formula:
        satisfied = False
        for lit in clause:
            if (lit > 0 and state[lit-1]) or (lit < 0 and not state[abs(lit)-1]):
                satisfied = True
                break
        if not satisfied:
            unsat += 1  # increment count for unsatisfied clause
    return unsat

def heuristic_penetrance(state, formula):
    """
    Penalize the state based on fraction of literals in each clause that are false.
    Provides a more granular measure than counting only unsatisfied clauses.
    """
    penalty = 0
    for clause in formula:
        false_count = 0
        for lit in clause:
            if (lit > 0 and not state[lit-1]) or (lit < 0 and state[abs(lit)-1]):
                false_count += 1
        penalty += false_count / len(clause)
    return penalty

# ----------------------------------
# 3. Hill Climbing
# ----------------------------------
def hill_climbing(formula, n, heuristic):
    """
    Hill Climbing algorithm for k-SAT:
    - Starts with a random assignment
    - Iteratively explores neighbors by flipping one variable at a time
    - Moves to the neighbor with a better heuristic
    - Stops when no improvement is possible
    """
    state = [random.choice([True, False]) for _ in range(n)]  # initial random state
    while True:
        neighbors = []
        for i in range(n):
            neighbor = state[:]
            neighbor[i] = not neighbor[i]  # flip one variable
            neighbors.append(neighbor)
        
        current_score = heuristic(state, formula)
        best_score = current_score
        best_neighbor = state[:]
        
        # Evaluate all neighbors to find the best
        for neighbor in neighbors:
            score = heuristic(neighbor, formula)
            if score < best_score:
                best_score = score
                best_neighbor = neighbor[:]
        
        # Stop if no improvement
        if best_score >= current_score:
            break
        state = best_neighbor[:]
    
    return state, heuristic(state, formula)

# ----------------------------------
# 4. Beam Search
# ----------------------------------
def beam_search(formula, n, heuristic, beam_width=3, max_steps=100):
    """
    Beam Search algorithm:
    - Maintains multiple candidate states (beam)
    - Expands each candidate by flipping one variable
    - Keeps only top 'beam_width' states
    - Repeats for a fixed number of steps or until solution found
    """
    beams = []
    for _ in range(beam_width):
        beams.append([random.choice([True, False]) for _ in range(n)])  # initialize beam with random states
    
    for _ in range(max_steps):
        new_beams = []
        for state in beams:
            for i in range(n):
                neighbor = state[:]
                neighbor[i] = not neighbor[i]  # flip variable
                new_beams.append(neighbor)
        
        # Evaluate heuristic for all new beams
        scores = [heuristic(b, formula) for b in new_beams]
        
        # Select top 'beam_width' states with lowest heuristic
        sorted_beams = []
        used = [False]*len(new_beams)
        for _ in range(beam_width):
            min_score = None
            min_index = -1
            for j in range(len(new_beams)):
                if not used[j]:
                    if min_score is None or scores[j] < min_score:
                        min_score = scores[j]
                        min_index = j
            if min_index >= 0:
                sorted_beams.append(new_beams[min_index])
                used[min_index] = True
        
        beams = sorted_beams[:]
        if heuristic(beams[0], formula) == 0:  # solution found
            break
    return beams[0], heuristic(beams[0], formula)

# ----------------------------------
# 5. Variable-Neighborhood Descent (VND)
# ----------------------------------
def flip_bits(state, indices):
    """
    Flip the variables at the given indices.
    Used for exploring neighborhoods in VND.
    """
    new_state = state[:]
    for i in indices:
        new_state[i] = not new_state[i]
    return new_state

def vnd(formula, n, heuristic):
    """
    Variable-Neighborhood Descent algorithm:
    - Explores neighborhoods of increasing size (1,2,3 flips)
    - Moves to better states if found
    - Continues until no improvement in all neighborhoods
    """
    state = [random.choice([True, False]) for _ in range(n)]
    
    # Define neighborhoods: single, double, and triple flips
    neighborhoods = [
        [[i] for i in range(n)],  # single flip
        [[i,j] for i in range(n) for j in range(i+1,n)],  # double flip
        [[i,j,k] for i in range(n) for j in range(i+1,n) for k in range(j+1,n)]  # triple flip
    ]
    
    for neighborhood in neighborhoods:
        improved = True
        while improved:
            improved = False
            best_score = heuristic(state, formula)
            best_state = state[:]
            for indices in neighborhood:
                new_state = flip_bits(state, indices)
                score = heuristic(new_state, formula)
                if score < best_score:
                    best_score = score
                    best_state = new_state[:]
                    improved = True
            state = best_state[:]
    return state, heuristic(state, formula)

# ----------------------------------
# 6. Test & Compare Algorithms
# ----------------------------------
if __name__ == "__main__":
    k, m, n = 3, 10, 6  # Example: 3 literals per clause, 10 clauses, 6 variables
    formula = generate_k_sat(k, m, n)
    
    print("Random 3-SAT formula:")
    for clause in formula:
        print(clause)
    
    print("\nHill Climbing:", hill_climbing(formula, n, heuristic_unsatisfied_clauses))
    print("Beam Search (w=3):", beam_search(formula, n, heuristic_unsatisfied_clauses, beam_width=3))
    print("Beam Search (w=4):", beam_search(formula, n, heuristic_unsatisfied_clauses, beam_width=4))
    print("VND:", vnd(formula, n, heuristic_unsatisfied_clauses))
