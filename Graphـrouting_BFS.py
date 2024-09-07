from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

class DynamicGraph:
    def __init__(self):
        self.graph = {}
        self.paths = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.update_paths_on_addition(u, v)

    def remove_edge(self, u, v):
        if u in self.graph and v in self.graph[u]:
            self.graph[u].remove(v)
        if v in self.graph and u in self.graph[v]:
            self.graph[v].remove(u)
        self.update_paths_on_removal(u, v)

    def bfs(self, start):
        visited = set()
        queue = deque([start])
        visited.add(start)
        while queue:
            vertex = queue.popleft()
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return visited

    def update_paths_on_addition(self, u, v):
        if u in self.paths:
            self.paths[u].update(self.bfs(u))
        else:
            self.paths[u] = self.bfs(u)
        
        if v in self.paths:
            self.paths[v].update(self.bfs(v))
        else:
            self.paths[v] = self.bfs(v)

    def update_paths_on_removal(self, u, v):
        self.paths[u] = self.bfs(u)
        self.paths[v] = self.bfs(v)

    def get_paths(self):
        return self.paths
    
    def draw_graph(self, filename):
        G = nx.Graph(self.graph)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
        plt.savefig(filename)
        plt.close()   

# Example usage
graph = DynamicGraph()
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.draw_graph("initial_graph_BFS.png")
print(graph.get_paths())
graph.remove_edge(2, 3)
graph.draw_graph("updated_graph_BFS.png")
print(graph.get_paths())
