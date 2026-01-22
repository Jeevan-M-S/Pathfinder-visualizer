# Maze Pathfinder Visualizer

Visualize how different pathfinding algorithms efficiently navigate and solve a maze. This interactive tool allows you to observe algorithms like Dijkstra's, A*, BFS, DFS, and Greedy Search in action.

![img.png](imgs/img.png)

![img_1.png](imgs/img_1.png)

![img_2.png](imgs/img_2.png)


## Overview

The Maze Pathfinder Visualizer is a Python-based application that demonstrates the step-by-step process of various search algorithms. It generates a random maze and allows the user to select an algorithm to find the path from a start point (green) to an end point (red).

### Supported Algorithms
- **Dijkstra's Algorithm**: Finds the shortest path in a weighted graph (here, all weights are equal).
- **Breadth-First Search (BFS)**: Guarantees the shortest path in an unweighted grid.
- **A\* Search**: Uses heuristics to find the shortest path more efficiently.
- **Depth-First Search (DFS)**: Explores as far as possible along each branch before backtracking.
- **Greedy Best-First Search**: Expands the node that is closest to the goal according to a heuristic.

## Requirements

- **Python**: 3.10+ (tested with 3.13)
- **Library**: [arcade](https://api.arcade.academy/en/latest/)

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Pathfinder-visualizer.git
   cd Pathfinder-visualizer
   ```

2. **Install dependencies**:
   ```bash
   pip install arcade
   ```
   *(Note: You may want to use a virtual environment)*

## Running the Application

To start the visualizer, run the following command from the root directory:

```bash
python main.py
```

## Scripts

- `main.py`: The entry point of the application. Handles the GUI, maze generation, and visualization logic.
- `Algorithms/`: Contains the implementation of the pathfinding algorithms.

## Project Structure

```text
Pathfinder-visualizer/
├── Algorithms/         # Pathfinding algorithm implementations
│   ├── A_Star.py
│   ├── BFS.py
│   ├── DFS.py
│   ├── Dijkstra.py
│   └── Greedy.py
├── imgs/               # Screenshots for README
├── main.py             # Main entry point and GUI logic
└── README.md           # Project documentation
```
