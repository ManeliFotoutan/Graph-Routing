# Dynamic Graph with Incremental BFS/DFS and Visualization

## Project Overview

This project implements a dynamic undirected graph that supports:

- Adding and removing edges dynamically (pending changes are staged before applying)
- Incrementally updating BFS or DFS paths on graph changes
- Visualizing the graph using `networkx` and `matplotlib`
- Command-line user interface for interactive graph modification and visualization


## Features

- **Dynamic Edge Management:** Edges can be added or removed and staged as pending changes. Changes apply together for efficient updates.

- **Incremental BFS/DFS Path Updates:** Upon edge additions or removals, BFS/DFS traversals update paths related to affected nodes only.

- **Graph Visualization:** Visualize and save the current graph to image files.

- **Interactive CLI:** User-friendly command line interface to add/remove edges, view BFS paths, apply or discard changes, save graph images, and exit.


## Installation

Make sure Python 3 is installed. Install dependencies:
```bash
pip install matplotlib networkx
```

## Usage

Run the script, then choose from the menu options:

- **A:** Add an edge (will be staged in pending changes)
- **R:** Remove an edge (staged for removal)
- **V:** View BFS paths from nodes (shows reachable nodes)
- **P:** Apply all pending changes and update paths
- **D:** Discard all pending changes
- **S:** Save the current graph visualization to a PNG file
- **E:** Exit the program

## Code Structure Highlights

- `DynamicGraph` class manages the graph data, pending changes, and path updates.
- BFS/DFS used to update reachable nodes after changes.
- Visualization handled with `networkx` and `matplotlib`.
- Command line interface drives the interactive session.
