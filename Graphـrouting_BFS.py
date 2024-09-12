from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

class DynamicGraph:
    def __init__(self):
        self.graph = {}
        self.paths = {}
        self.pending_changes = []  # For storing pending changes
    
    def add_edge(self, u, v):
        self.pending_changes.append(('add', u, v))
        print(f"Edge ({u}, {v}) added to pending changes.")
    
    def remove_edge(self, u, v):
        self.pending_changes.append(('remove', u, v))
        print(f"Edge ({u}, {v}) added to pending removal.")
    
    def apply_changes(self):
        for change, u, v in self.pending_changes:
            if change == 'add':
                self._add_edge(u, v)
                self.update_paths_on_addition(u, v)  # Update paths on addition
            elif change == 'remove':
                self._remove_edge(u, v)
                self.update_paths_on_removal(u, v)  # Update paths on removal
        self.pending_changes = []  # Clear pending changes after applying

    def _add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)
        print(f"Edge ({u}, {v}) added to graph.")

    def _remove_edge(self, u, v):
        if u in self.graph and v in self.graph[u]:
            self.graph[u].remove(v)
        if v in self.graph and u in self.graph[v]:
            self.graph[v].remove(u)
        print(f"Edge ({u}, {v}) removed from graph.")

    def discard_changes(self):
        self.pending_changes = []
        print("Pending changes discarded.")

    def show_pending_changes(self):
        return self.pending_changes

    def bfs(self, start):
        visited = set()
        queue = deque([start])
        visited.add(start)
        paths = {start: [start]}  # Store the path taken to reach each node
        while queue:
            vertex = queue.popleft()
            for neighbor in self.graph.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    paths[neighbor] = paths[vertex] + [neighbor]
        return paths

    def update_paths_on_addition(self, u, v):
        # Update the paths for both nodes
        self.paths[u] = self.bfs(u)
        self.paths[v] = self.bfs(v)
    
    def update_paths_on_removal(self, u, v):
        # Remove the paths after an edge is removed and update the paths for both nodes
        if u in self.graph:
            self.paths[u] = self.bfs(u)
        if v in self.graph:
            self.paths[v] = self.bfs(v)

    def get_paths(self):
        return self.paths
    
    def draw_graph(self, filename):
        # Debugging print statements
        print("Drawing graph...")
        G = nx.Graph(self.graph)  # Create networkx graph from the dictionary
        pos = nx.spring_layout(G)  # Layout for node positioning
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
        plt.savefig(filename)
        plt.close()
        print(f"Graph saved as {filename}")

def user_interface():
    graph = DynamicGraph()
    while True:
        print("\nChoose Mode:")
        print("A. Add Edge")
        print("R. Remove Edge")
        print("V. View BFS Paths")
        print("P. Apply Pending Changes")
        print("D. Discard Pending Changes")
        print("S. Save Graph to File")
        print("E. Exit")

        choice = input("Choose an option: ").upper()
        
        if choice == 'A':
            u = int(input("Enter the first node: "))
            v = int(input("Enter the second node: "))
            graph.add_edge(u, v)
            print(f"Edge ({u}, {v}) added to pending changes.")
        
        elif choice == 'R':
            u = int(input("Enter the first node: "))
            v = int(input("Enter the second node: "))
            graph.remove_edge(u, v)
            print(f"Edge ({u}, {v}) added to pending removal.")
        
        elif choice == 'V':
            paths = graph.get_paths()
            if not paths:  # Check if paths dictionary is empty
                print("No paths to display.")
            else:
                all_paths_empty = True  # Flag to check if all paths are empty
                for node, path in paths.items():
                    if len(path) > 1:  # There are paths other than just the start node
                        print(f"Paths from node {node}: {path}")
                        all_paths_empty = False
                    else:
                        print(f"No path found from node {node}.")
                
                if all_paths_empty:
                    print("No valid paths found in the graph.")

        
        elif choice == 'P':
            graph.apply_changes()
            print("Pending changes applied.")
        
        elif choice == 'D':
            graph.discard_changes()
            print("Pending changes discarded.")
        
        elif choice == 'S':
            filename = input("Enter filename to save the graph (e.g., graph.png): ")
            graph.draw_graph(filename)
        
        elif choice == 'E':
            print("Exiting.")
            break
        
        else:
            print("Invalid option. Please choose again.")

# Run the user interface
user_interface()

