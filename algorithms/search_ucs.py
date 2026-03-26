# algorithms/search_ucs.py
import heapq

def run_ucs(grid, start, goal):
    """
    Finds the cheapest path from start to goal using Uniform-Cost Search.
    0 = clear path (cost 1)
    1 = wall (impassable)
    2 = traffic/spill (cost 5)
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Priority Queue stores: (cumulative_cost, tie_breaker, current_node, path)
    pq = []
    tie_breaker = 0 # Helps heapq decide what to do if two paths have the exact same cost
    heapq.heappush(pq, (0, tie_breaker, start, [start]))
    
    # Dictionary to keep track of the absolute lowest cost to reach any specific node
    visited_costs = {start: 0}
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while pq:
        # Pop the CHEAPEST item from the priority queue
        current_cost, _, current_node, path = heapq.heappop(pq)
        
        # Did we reach the goal?
        if current_node == goal:
            return path, current_cost
            
        r, c = current_node
        
        for dr, dc in directions:
            next_r, next_c = r + dr, c + dc
            
            # Is it inside the grid?
            if (0 <= next_r < rows) and (0 <= next_c < cols):
                cell_value = grid[next_r][next_c]
                
                # If it's NOT a wall...
                if cell_value != 1: 
                    # Step cost is 5 if it's a traffic zone (2), otherwise 1
                    step_cost = 5 if cell_value == 2 else 1
                    new_cost = current_cost + step_cost
                    next_node = (next_r, next_c)
                    
                    # If we haven't visited this node yet, OR we just found a CHEAPER way to get to it
                    if next_node not in visited_costs or new_cost < visited_costs[next_node]:
                        visited_costs[next_node] = new_cost
                        tie_breaker += 1
                        heapq.heappush(pq, (new_cost, tie_breaker, next_node, path + [next_node]))
                        
    # No path found
    return None, float('inf')