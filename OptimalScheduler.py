import numpy as np
from Graph import Graph

class OptimalScheduler:

    def __init__(self, graph: Graph, qMatrix: np.ndarray[np.ndarray[float]], epsilon: float = 0.5, gamma: float = 0.01):
        self.graph = graph
        self.qMatrix = qMatrix
        self.useMatrix = np.zeros_like(qMatrix)
        self.epsilon = epsilon
        self.gamma = gamma
    
    '''Method of getting a path between source and target with user defined randomness given SSSP dictionary'''
    def getRealPath(self, target: str, source: str, path_dict: dict[str, list[str]]) -> list[str]:
        path = [target]
        used_edges = []
        while path[-1] != source:
            # Epsilon Greedy
            if np.random.uniform(0.0,1.0) < self.epsilon:
                # get all of the edges for the current node
                node_edges = [edge for edge in self.graph.getNodes()[int(path[-1])].getEdges()]
                # remove an edge if it was already traversed
                for edge in node_edges:
                    if edge.getId() in used_edges:
                        node_edges.remove(edge)
                # pick edge and add target to path
                edge = np.random.choice(node_edges)
                path.append(edge.getTarget())
            else:
                path.append(path_dict[path[-1]][-2])

        path.reverse()
        self.epsilon -= self.gamma
        return path


    def antColonyPath(self, target: str, source: str):
        pass
    
    '''Method for updating the Q matrix given a path'''
    def updateQMatrix(self, path: list[str]) -> None:
        path_sample = self.graph.samplePath(path)
        for i in range(len(path)-2):
            # increment the use matrix
            self.useMatrix[int(path[i])][int(path[i+1])] += 1
            # update the q matrix
            n = self.useMatrix[int(path[i])][int(path[i+1])]
            old_val = self.qMatrix[int(path[i])][int(path[i+1])]
            self.qMatrix[int(path[i])][int(path[i+1])] = (old_val * (n - 1) + path_sample[i]) / n 