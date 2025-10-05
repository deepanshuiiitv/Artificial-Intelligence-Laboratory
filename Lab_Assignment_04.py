# Lab Assignment 04- Solving Jigsaw Puzzle Using Simulated Annealing




import random
import math

# -----------------------------
# Example: Scrambled Puzzle
# -----------------------------
# This example demonstrates solving a simple 4x4 puzzle using Simulated Annealing.
# Each puzzle block is represented by an integer from 0 to 15. 
# In a real puzzle, each block could be an image segment or pixel grid.
blocks = list(range(16))  # Create a list of blocks in correct order

# Scramble the blocks to generate an initial puzzle state
scrambled = blocks.copy()  # Copy the original list to avoid modifying it
random.shuffle(scrambled)   # Randomly shuffle to simulate a scrambled puzzle

# Define the puzzle size (4x4)
N = 4

# -----------------------------
# Cost Function
# -----------------------------
# The cost function evaluates how far the current puzzle state is from the goal.
# Here, the goal is each block being in its "correct" position.
# A lower cost indicates a state closer to the solution.
def cost(state):
    c = 0
    for i in range(len(state)):
        if state[i] != i:  # If the block is not in the correct position
            c += 1          # Add a penalty of 1
    return c  # Return total cost

# -----------------------------
# Simulated Annealing Algorithm
# -----------------------------
# This function attempts to find the puzzle solution by exploring states probabilistically.
# Simulated Annealing allows "uphill" moves (worse solutions) to escape local minima.
def simulated_annealing(initial_state, initial_temp, cooling_rate, max_iter):
    current_state = initial_state.copy()      # Start from the initial scrambled state
    current_cost = cost(current_state)        # Compute the cost of the initial state
    best_state = current_state.copy()         # Keep track of the best solution found
    best_cost = current_cost
    temp = initial_temp                        # Initialize temperature

    # Main loop: iterate a fixed number of times
    for iteration in range(max_iter):
        # Generate a neighbor state by swapping two random blocks
        i, j = random.sample(range(len(current_state)), 2)
        new_state = current_state.copy()
        new_state[i], new_state[j] = new_state[j], new_state[i]

        new_cost = cost(new_state)            # Compute cost of new state
        delta = new_cost - current_cost       # Change in cost

        # Accept the new state probabilistically:
        #   - Always accept if new cost is lower
        #   - Sometimes accept if new cost is higher (controlled by temperature)
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_state = new_state
            current_cost = new_cost

        # Update the best solution found so far
        if current_cost < best_cost:
            best_state = current_state.copy()
            best_cost = current_cost

        # Gradually reduce the temperature (cooling schedule)
        temp *= cooling_rate

        # Optional: print progress every 100 iterations
        if iteration % 100 == 0:
            print(f"Iteration {iteration}, Cost: {best_cost}")

    # Return the best puzzle state and its cost
    return best_state, best_cost

# -----------------------------
# Run the Simulated Annealing Algorithm
# -----------------------------
best_state, best_cost = simulated_annealing(
    scrambled,      # Starting puzzle state
    initial_temp=100,  # Initial temperature
    cooling_rate=0.95, # Cooling rate per iteration
    max_iter=1000      # Maximum number of iterations
)

# Print results
print("Initial scrambled:", scrambled)   # Show the scrambled puzzle
print("Best solution    :", best_state) # Show the puzzle state found
print("Best cost        :", best_cost)  # Show the cost (number of misplaced blocks)
