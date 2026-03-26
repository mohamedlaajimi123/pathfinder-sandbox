# algorithms/search_ids.py

def run_dls(grid, start, goal, limit):
    """
    Runs Depth-First Search but strictly stops at the given 'limit'.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Stack stores: (current_node, path_so_far, current_depth)
    stack = [(start, [start], 0)]
    
    # We track the shortest depth at which we visited a node to prevent loops
    visited = {start: 0} 
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while stack:
        current_node, path, depth = stack.pop()
        
        if current_node == goal:
            return path
            
        # Only expand if we haven't hit our depth limit!
        if depth < limit:
            r, c = current_node
            
            for dr, dc in directions:
                next_r, next_c = r + dr, c + dc
                
                # Check grid boundaries and walls (1)
                if (0 <= next_r < rows) and (0 <= next_c < cols) and grid[next_r][next_c] != 1:
                    next_node = (next_r, next_c)
                    
                    # Only add to stack if unvisited, OR if we found a faster way to get here
                    if next_node not in visited or visited[next_node] > depth + 1:
                        visited[next_node] = depth + 1
                        stack.append((next_node, path + [next_node], depth + 1))
                        
    # Goal not found within this depth limit
    return None


def run_ids(grid, start, goal, max_possible_depth=100):
    """
    Iterative Deepening: Runs DLS repeatedly, increasing the limit by 1 each time.
    """
    # Start at depth 0 and increase by 1 each loop
    for limit in range(max_possible_depth):
        # print(f"Trying depth limit: {limit}") # Optional: uncomment to watch it work!
        result = run_dls(grid, start, goal, limit)
        
        # If DLS returns a path, we are done!
        if result is not None:
            return result
            
    return None