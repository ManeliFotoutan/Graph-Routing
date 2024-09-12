from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import os

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

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        for neighbor in self.graph[start]:
            if neighbor not in visited:
                self.dfs(neighbor, visited)
        return visited

    def update_paths_on_addition(self, u, v):
        # بروزرسانی فقط مسیرهای مرتبط با یال جدید
        if u in self.paths:
            self.paths[u].update(self.dfs(u))
        else:
            self.paths[u] = self.dfs(u)
        
        if v in self.paths:
            self.paths[v].update(self.dfs(v))
        else:
            self.paths[v] = self.dfs(v)

    def update_paths_on_removal(self, u, v):
        # حذف یال، نیاز به بروزرسانی مسیرهای مرتبط با این دو گره دارد
        self.paths[u] = self.dfs(u)
        self.paths[v] = self.dfs(v)

    def get_paths(self):
        return self.paths

    def draw_graph(self, filename):
        G = nx.Graph(self.graph)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
        
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filename)
        
        plt.savefig(full_path)
        plt.close()
        print(f"Graph saved as {full_path}.")

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
