import numpy as np
from Graph import Graph
from collections import deque

class MonteCarloBFS:

    def __init__(self, graph: Graph, qMatrix: np.ndarray[np.ndarray[float]], gamma: float = 0.01):
        self.graph = graph
        self.qMatrix = qMatrix
        self.useMatrix = np.zeros_like(qMatrix)
        self.gamma = gamma
        self.visitedPaths = []

    def bfs(self, start, end):
        queue = deque([(start, [start])])
        while queue:
            (vertex, path) = queue.popleft()
            for neighbor in self.graph.getNodes()[int(vertex)].getEdges():
                if neighbor.getTarget() == end:
                    return path + [neighbor.getTarget()]
                else:
                    queue.append((neighbor.getTarget(), path + [neighbor.getTarget()]))

    def getRealPath(self, target: str, source: str, path_dict: dict[str, list[str]]) -> list[str]:
        path = self.bfs(source, target)
        path.reverse()
        return path

    def updateQMatrix(self) -> None:
        for path in self.visitedPaths:
            path_sample = self.graph.samplePath(path)
            for i in range(len(path)-2):
                # increment the use matrix
                self.useMatrix[int(path[i])][int(path[i+1])] += 1
                # update the q matrix
                n = self.useMatrix[int(path[i])][int(path[i+1])]
                old_val = self.qMatrix[int(path[i])][int(path[i+1])]
                self.qMatrix[int(path[i])][int(path[i+1])] = (old_val * (n - 1) + path_sample[i]) / n
        self.visitedPaths = []

    def findOptimalPath(self, source: str, target: str, num_episodes: int) -> list[str]:
        for i in range(num_episodes):
            path = self.getRealPath(target, source, {})
            self.visitedPaths.append(path)
        self.updateQMatrix()
        return self.getOptimalPath(source, target)

    def getOptimalPath(self, source: str, target: str) -> list[str]:
        path = [source]
        while path[-1] != target:
            node = int(path[-1])
            edges = self.graph.getNodes()[node].getEdges()
            max_val = float('-inf')
            max_edge = None
            for edge in edges:
                val = self.qMatrix[node][int(edge.getTarget())]
                if val > max_val:
                    max_val = val
                    max_edge = edge
            path.append(max_edge.getTarget())
        return path
