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
        self.update_paths()

    def remove_edge(self, u, v):
        if u in self.graph and v in self.graph[u]:
            self.graph[u].remove(v)
        if v in self.graph and u in self.graph[v]:
            self.graph[v].remove(u)
        self.update_paths()

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        for neighbor in self.graph[start]:
            if neighbor not in visited:
                self.dfs(neighbor, visited)
        return visited

    def update_paths(self):
        self.paths = {}
        for node in self.graph:
            self.paths[node] = self.dfs(node)

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
graph.draw_graph("initial_graph_DFS.png")
print(graph.get_paths())
graph.remove_edge(2, 3)
graph.draw_graph("updated_graph_DFS.png")
print(graph.get_paths())