import { useState } from 'react';
import './App.css';

// We rename this to DEFAULT_GRID so we can reset to it later
const DEFAULT_GRID = [
  [0, 0, 0, 1, 0],
  [0, 1, 0, 1, 0],
  [0, 1, 2, 2, 0],
  [0, 0, 0, 1, 0],
  [1, 1, 0, 0, 0]
];

const START_POS = [0, 0];
const GOAL_POS = [4, 4];

function App() {
  // 1. Put the grid into React State so it can change dynamically
  const [grid, setGrid] = useState(DEFAULT_GRID);
  const [algorithm, setAlgorithm] = useState('bfs');
  const [path, setPath] = useState([]);
  const [status, setStatus] = useState('Ready');

  // 2. The function that runs when you click a square
  const handleCellClick = (r, c) => {
    // Don't allow clicking on the Start or Goal squares
    if ((r === START_POS[0] && c === START_POS[1]) || (r === GOAL_POS[0] && c === GOAL_POS[1])) {
      return;
    }

    // Create a copy of the current grid
    const newGrid = grid.map(row => [...row]);
    
    // Cycle the cell value: 0 (Empty) -> 1 (Wall) -> 2 (Traffic) -> 0 (Empty)
    newGrid[r][c] = (newGrid[r][c] + 1) % 3;
    
    // Update the state
    setGrid(newGrid);
    
    // Clear the old AI path because the map just changed!
    setPath([]); 
    setStatus('Grid updated. Ready to run AI.');
  };

  const runAI = async () => {
    setStatus('Thinking...');
    setPath([]); 

    try {
      const response = await fetch('http://127.0.0.1:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          grid: grid, // 3. We now send the DYNAMIC grid to Python!
          start: START_POS,
          goal: GOAL_POS,
          algorithm: algorithm
        })
      });

      const data = await response.json();

      if (data.status === 'success') {
        setStatus(`Success! Found path in ${data.steps} steps.`);
        setPath(data.path);
      } else {
        setStatus('Error: ' + data.message);
      }
    } catch (error) {
      console.error(error);
      setStatus('Failed to connect to backend.');
    }
  };

  const getCellClass = (r, c, value) => {
    if (r === START_POS[0] && c === START_POS[1]) return 'cell start';
    if (r === GOAL_POS[0] && c === GOAL_POS[1]) return 'cell goal';
    
    const isPath = path.some(p => p[0] === r && p[1] === c);
    if (isPath) return 'cell path';

    if (value === 1) return 'cell wall';
    if (value === 2) return 'cell traffic';
    return 'cell';
  };

  return (
    <div className="app-container">
      <h1>Warehouse AI Pathfinding</h1>
      <p style={{ marginBottom: '20px', color: '#555' }}>
        Click any white square to toggle it into a <b>Wall</b> (dark) or <b>Traffic</b> (yellow)!
      </p>
      
      <div className="controls">
        <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
          <option value="bfs">Breadth-First Search (BFS)</option>
          <option value="dfs">Depth-First Search (DFS)</option>
          <option value="ucs">Uniform-Cost Search (UCS)</option>
          <option value="ids">Iterative Deepening (IDS)</option>
        </select>
        <button onClick={runAI}>Run AI</button>
        
        {/* Added a reset button for convenience */}
        <button onClick={() => { setGrid(DEFAULT_GRID); setPath([]); }}>Reset Grid</button>
      </div>

      <h2>Status: {status}</h2>

      <div className="grid">
        {grid.map((row, rIndex) => (
          <div key={rIndex} className="row">
            {row.map((cellValue, cIndex) => (
              <div 
                key={`${rIndex}-${cIndex}`} 
                className={getCellClass(rIndex, cIndex, cellValue)}
                onClick={() => handleCellClick(rIndex, cIndex)}
                style={{ cursor: 'pointer' }} // Makes it obvious it's clickable
              >
                {cellValue === 2 ? '⚠️' : ''}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;