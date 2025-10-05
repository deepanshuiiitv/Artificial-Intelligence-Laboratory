# Lab Assignment 02- Plagiarism Detection Using A* Search for Text Alignment



import heapq
import re
from itertools import product

# -----------------------------
# 1. Text Preprocessing
# -----------------------------
def preprocess(text):
    """
    Convert raw text into a list of normalized sentences.
    Steps:
        1. Split text into sentences using punctuation marks.
        2. Remove non-word characters and extra spaces.
        3. Convert all text to lowercase for uniformity.
    """
    sentences = re.split(r'[.!?]', text)  # Split text into sentences
    sentences = [re.sub(r'\W+', ' ', s).strip().lower() for s in sentences if s.strip()]
    return sentences

# -----------------------------
# 2. Levenshtein Distance (Edit Distance)
# -----------------------------
def edit_distance(s1, s2):
    """
    Compute the minimum number of single-character edits (insertions, deletions, substitutions)
    required to change string s1 into string s2.
    This is used as a similarity measure between sentences.
    """
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    
    # Initialize base cases
    for i in range(m+1):
        dp[i][0] = i  # cost of deleting all characters
    for j in range(n+1):
        dp[0][j] = j  # cost of inserting all characters
    
    # Compute distances
    for i, j in product(range(1, m+1), range(1, n+1)):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1]  # no cost if characters match
        else:
            dp[i][j] = 1 + min(dp[i-1][j],    # deletion
                               dp[i][j-1],    # insertion
                               dp[i-1][j-1])  # substitution
    return dp[m][n]

# -----------------------------
# 3. A* Search for Sentence Alignment
# -----------------------------
def a_star_align(doc1, doc2):
    """
    Align sentences of two documents using A* search:
    - Each state contains current cost, positions in doc1 and doc2, and alignment so far.
    - Transitions:
        1. Align a sentence from doc1 with one from doc2.
        2. Skip a sentence in doc1.
        3. Skip a sentence in doc2.
    - The algorithm returns a list of aligned sentence pairs with their edit distances.
    """
    n, m = len(doc1), len(doc2)
    start_state = (0, 0, 0, [])  # (cost_so_far, pos_doc1, pos_doc2, alignment)
    heap = []
    heapq.heappush(heap, (0, start_state))  # priority queue sorted by f = g + h
    visited = {}  # keep track of visited positions with minimum cost

    while heap:
        f_cost, (g_cost, i, j, align) = heapq.heappop(heap)
        
        if (i, j) in visited and visited[(i,j)] <= g_cost:
            continue
        visited[(i,j)] = g_cost
        
        # Goal: both documents fully aligned
        if i == n and j == m:
            return align
        
        # Generate next states
        next_states = []
        
        # 1. Align sentences i and j
        if i < n and j < m:
            cost = edit_distance(doc1[i], doc2[j])
            next_states.append((g_cost + cost, i+1, j+1, align + [(doc1[i], doc2[j], cost)]))
        
        # 2. Skip sentence in doc1
        if i < n:
            next_states.append((g_cost + len(doc1[i].split()), i+1, j, align + [(doc1[i], "", len(doc1[i].split()))]))
        
        # 3. Skip sentence in doc2
        if j < m:
            next_states.append((g_cost + len(doc2[j].split()), i, j+1, align + [("", doc2[j], len(doc2[j].split()))]))
        
        # Push next states to heap
        for state in next_states:
            g_new = state[0]
            h = 0  # heuristic: can be improved, currently set to zero
            heapq.heappush(heap, (g_new + h, state))
    
    return []

# -----------------------------
# 4. Plagiarism Detection
# -----------------------------
def detect_plagiarism(text1, text2, threshold=5):
    """
    Detect potential plagiarism between two documents:
    1. Preprocess both texts into sentences.
    2. Align sentences using A* search.
    3. For each aligned pair, mark as potential plagiarism if edit distance <= threshold.
    """
    doc1 = preprocess(text1)
    doc2 = preprocess(text2)
    alignment = a_star_align(doc1, doc2)
    
    print("\nAligned Sentences with Edit Distances:\n")
    for s1, s2, dist in alignment:
        status = "Potential Plagiarism" if dist <= threshold else "No Plagiarism"
        print(f"{s1}\n{'' if s2=='' else s2}\nEdit Distance: {dist} -> {status}\n")
    
    return alignment

# -----------------------------
# 5. Test Cases
# -----------------------------
if __name__ == "__main__":
    text1 = "Artificial Intelligence is the simulation of human intelligence. It is used in many fields."
    text2 = "Artificial Intelligence simulates human intelligence. Many fields use it."
    
    detect_plagiarism(text1, text2)
