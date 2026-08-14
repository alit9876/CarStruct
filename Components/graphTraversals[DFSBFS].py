from collections import deque

class BFSAlgorithm:
    def __init__(self, weighted_graph):
        self.graph = weighted_graph

    def bfs_paths(self, source, target):
        queue = deque([(source, [source])])
        paths = []

        while queue:
            current_node, path = queue.popleft()

            for neighbor in self.graph.graph[current_node]:
                if neighbor not in path:
                    if neighbor == target:
                        paths.append(path + [neighbor])
                    else:
                        queue.append((neighbor, path + [neighbor]))

        return paths
    
class DFSAlgorithm:
    def __init__(self, weighted_graph):
        self.graph = weighted_graph

    def dfs_paths(self, source, target):
        visited = set()
        paths = []
        self._dfs_paths(source, target, visited, [source], paths)
        return paths

    def _dfs_paths(self, current_node, target, visited, path, paths):
        visited.add(current_node)

        if current_node == target:
            paths.append(path.copy())
        else:
            for neighbor in self.graph.graph[current_node]:
                if neighbor not in visited:
                    self._dfs_paths(neighbor, target, visited, path + [neighbor], paths)

        visited.remove(current_node)  # Backtrack