import numpy as np
from Graph import Graph

class MonteCarloScheduler:

    def __init__(self, graph: Graph, qMatrix: np.ndarray[np.ndarray[float]], gamma: float = 0.01):
        self.graph = graph
        self.qMatrix = qMatrix
        self.useMatrix = np.zeros_like(qMatrix)
        self.gamma = gamma
        self.visitedPaths = []
    
    def getRealPath(self, target: str, source: str, path_dict: dict[str, list[str]]) -> list[str]:
        path = [target]
        used_edges = []
        while path[-1] != source:
            # get all of the edges for the current node
            node_edges = [edge for edge in self.graph.getNodes()[int(path[-1])].getEdges()]
            # remove an edge if it was already traversed
            for edge in node_edges:
                if edge.getId() in used_edges:
                    node_edges.remove(edge)
            # pick edge and add target to path
            edge = np.random.choice(node_edges)
            used_edges.append(edge.getId())
            path.append(edge.getTarget())
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
