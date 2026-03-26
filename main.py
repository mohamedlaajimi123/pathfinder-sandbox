# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple

# Import your AI brain!
from algorithms.search_bfs import run_bfs
from algorithms.search_dfs import run_dfs
from algorithms.search_ucs import run_ucs
from algorithms.search_ids import run_ids

# Initialize the API
app = FastAPI(title="Smart Warehouse AI")

# --- CORS Block ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all frontend domains to talk to this API
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, etc.
    allow_headers=["*"],
)

# Define the exact structure of the data the frontend will send us
class PathRequest(BaseModel):
    grid: List[List[int]]
    start: Tuple[int, int]
    goal: Tuple[int, int]
    algorithm: str  # "bfs", "dfs", "ucs", or "ids"

# Create the endpoint that the frontend will call
@app.post("/solve")
def solve_path(request: PathRequest):
    algo = request.algorithm.lower()
    
    # Route the request to the correct algorithm
    if algo == "bfs":
        path = run_bfs(request.grid, request.start, request.goal)
    elif algo == "dfs":
        path = run_dfs(request.grid, request.start, request.goal)
    elif algo == "ucs":
        path, cost = run_ucs(request.grid, request.start, request.goal)
    elif algo == "ids":
        path = run_ids(request.grid, request.start, request.goal)
    else:
        raise HTTPException(status_code=400, detail="Invalid algorithm chosen.")
        
    # If the AI couldn't find a path
    if path is None:
        return {"status": "error", "message": "No path found. The robot is trapped!"}
        
    # Send the successful data back to the frontend
    return {
        "status": "success",
        "algorithm": algo,
        "steps": len(path) - 1,
        "path": path
    }