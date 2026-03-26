# algorithms/search_dfs.py

def run_dfs(grid, start, goal):
    """
    Finds a path from start to goal using Depth-First Search.
    Does NOT guarantee the shortest path.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # A Stack uses Last-In, First-Out (LIFO). 
    # We use a standard Python list for this.
    stack = [(start, [start])]
    
    # Keep track of where we've been
    visited = set()
    
    # Directions we can move: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while stack:
        # Pop the NEWEST item from the top of the stack
        current_node, path = stack.pop()
        
        # With DFS, we mark nodes as visited when we pop them off the stack, 
        # not when we add them.
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Did we reach the goal?
        if current_node == goal:
            return path
            
        r, c = current_node
        
        # Check all 4 adjacent neighbors
        for dr, dc in directions:
            next_r, next_c = r + dr, c + dc
            
            # 1. Inside the grid?
            # 2. Empty space (0)?
            if (0 <= next_r < rows) and (0 <= next_c < cols):
                if grid[next_r][next_c] == 0 and (next_r, next_c) not in visited:
                    # Push the valid neighbor to the top of the stack
                    stack.append(((next_r, next_c), path + [(next_r, next_c)]))
                    
    # No path found
    return None