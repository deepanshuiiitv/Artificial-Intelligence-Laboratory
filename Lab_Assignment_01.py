# Lab Assignment 01- Solving the Rabbit Leap Puzzle Using State-Space Search Techniques


import time
import tracemalloc
from collections import deque
import matplotlib.pyplot as plt

# -------------------------------
# 1. Rabbit Leap Puzzle Definitions
# -------------------------------
# Puzzle: 3 white (W) and 3 empty (E) blocks separated by a blank ('_')
# Goal: swap positions of E and W while following puzzle rules
initial_state = ['E', 'E', 'E', '_', 'W', 'W', 'W']
goal_state = ['W', 'W', 'W', '_', 'E', 'E', 'E']

def is_goal(state):
    """
    Check if the current state matches the goal state.
    """
    return state == goal_state

def get_successors(state):
    """
    Generate all possible successor states from the current state:
    - E blocks can move right into the blank if adjacent or by jumping one block.
    - W blocks can move left into the blank if adjacent or by jumping one block.
    """
    successors = []
    empty_index = state.index('_')  # locate the blank
    for i, piece in enumerate(state):
        # Move E block to the right
        if piece == 'E' and i < empty_index:
            if empty_index - i == 1 or empty_index - i == 2:
                new_state = state[:]
                new_state[empty_index], new_state[i] = new_state[i], new_state[empty_index]
                successors.append(new_state)
        # Move W block to the left
        elif piece == 'W' and i > empty_index:
            if i - empty_index == 1 or i - empty_index == 2:
                new_state = state[:]
                new_state[empty_index], new_state[i] = new_state[i], new_state[empty_index]
                successors.append(new_state)
    return successors

# -------------------------------
# 2. BFS Implementation
# -------------------------------
def bfs(start):
    """
    Breadth-First Search to find the shortest solution:
    - Uses a queue (FIFO) to explore states level by level
    - Keeps track of visited states to avoid revisiting
    """
    queue = deque([(start, [])])  # queue holds (state, path_to_state)
    visited = set()
    while queue:
        state, path = queue.popleft()
        state_tuple = tuple(state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        if is_goal(state):
            return path + [state]
        for succ in get_successors(state):
            queue.append((succ, path + [state]))
    return None

# -------------------------------
# 3. DFS Implementation
# -------------------------------
def dfs(start):
    """
    Depth-First Search to find a solution:
    - Uses a stack (LIFO) to explore states along one path deeply
    - Keeps track of visited states to avoid revisiting
    """
    stack = [(start, [])]  # stack holds (state, path_to_state)
    visited = set()
    while stack:
        state, path = stack.pop()
        state_tuple = tuple(state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        if is_goal(state):
            return path + [state]
        for succ in get_successors(state):
            stack.append((succ, path + [state]))
    return None

# -------------------------------
# 4. Measure Performance
# -------------------------------
def measure(func):
    """
    Measure moves, execution time, and memory usage of a search algorithm.
    - Uses tracemalloc to track memory
    - Returns number of moves, execution time in seconds, memory used in KB
    """
    tracemalloc.start()
    start_time = time.time()
    result = func(initial_state)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    moves = len(result) - 1 if result else 0
    return moves, end_time - start_time, peak / 1024  # memory in KB

# Run BFS and DFS and measure performance
bfs_moves, bfs_time, bfs_memory = measure(bfs)
dfs_moves, dfs_time, dfs_memory = measure(dfs)

# -------------------------------
# 5. Visual Comparison Graphs
# -------------------------------
algorithms = ['BFS', 'DFS']
moves_taken = [bfs_moves, dfs_moves]
time_taken = [bfs_time, dfs_time]
memory_used = [bfs_memory, dfs_memory]

# ----- Graph 1: Moves Taken -----
plt.figure(figsize=(6,4))
plt.bar(algorithms, moves_taken, color=['blue', 'orange'])
plt.ylabel('Moves Taken')
plt.title('BFS vs DFS: Moves Taken')
plt.ylim(0, max(moves_taken)+5)
for i, v in enumerate(moves_taken):
    plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
plt.show()

# ----- Graph 2: Time Taken -----
plt.figure(figsize=(6,4))
plt.bar(algorithms, time_taken, color=['green', 'red'])
plt.ylabel('Time Taken (seconds)')
plt.title('BFS vs DFS: Execution Time')
plt.ylim(0, max(time_taken)+0.01)
for i, v in enumerate(time_taken):
    plt.text(i, v + 0.001, f"{v:.5f}", ha='center', fontweight='bold')
plt.show()

# ----- Graph 3: Memory Used -----
plt.figure(figsize=(6,4))
plt.bar(algorithms, memory_used, color=['purple', 'brown'])
plt.ylabel('Memory Used (KB)')
plt.title('BFS vs DFS: Memory Usage')
plt.ylim(0, max(memory_used)+20)
for i, v in enumerate(memory_used):
    plt.text(i, v + 2, f"{v:.2f}", ha='center', fontweight='bold')
plt.show()
