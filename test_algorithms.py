# test_algorithms.py
from algorithms.search_bfs import run_bfs
from algorithms.search_ids import run_ids

warehouse_grid = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0], 
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0]
]

start_position = (0, 0) 
goal_position = (4, 4)  

print("--- Running BFS ---")
bfs_path = run_bfs(warehouse_grid, start_position, goal_position)
print(f"BFS Path: {bfs_path}\n")

print("--- Running IDS ---")
# IDS should find the exact same shortest path as BFS!
ids_path = run_ids(warehouse_grid, start_position, goal_position)
print(f"IDS Path: {ids_path}")