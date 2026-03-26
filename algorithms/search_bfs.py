from collections import deque

def run_bfs(grid, start, goal):
    """
    Finds the shortest path from start to goal using Breadth-First Search.
    grid: 2D list where 0 is empty, 1 is a wall.
    start: tuple (row, col)
    goal: tuple (row, col)
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # The queue stores: (current_position, path_taken_so_far)
    queue = deque([(start, [start])])
    
    # Keep track of where we've been so we don't go in circles
    visited = set()
    visited.add(start)
    
    # Directions we can move: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        # Pop the oldest item from the front of the queue
        current_node, path = queue.popleft()
        
        # Did we reach the goal?
        if current_node == goal:
            return path
            
        r, c = current_node
        
        # Check all 4 adjacent neighbors
        for dr, dc in directions:
            next_r, next_c = r + dr, c + dc
            
            # 1. Is it inside the grid?
            # 2. Is it an empty space (0)?
            # 3. Have we NOT visited it yet?
            if (0 <= next_r < rows) and (0 <= next_c < cols):
                if grid[next_r][next_c] == 0 and (next_r, next_c) not in visited:
                    visited.add((next_r, next_c))
                    # Add the valid neighbor to the queue, and update its path
                    queue.append(((next_r, next_c), path + [(next_r, next_c)]))
                    
    # If the queue empties and we never hit the goal, there is no path
    return None