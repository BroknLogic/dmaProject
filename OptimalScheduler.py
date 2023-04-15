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
    def getRealPath(self, source: str, target: str, path_dict: dict[str, dict[str, int]]) -> list[str]:
        path = [target]
        used_edges = []
        while path[-1] != source:
            # Epsilon Greedy
            if np.random.uniform(0.0,1.0) < self.epsilon:
                # get all of the edges for the current node
                node_edges = self.graph.getNodes()[int(path[-1])].getEdges()
                # remove an edge if it was already traversed
                for edge in node_edges:
                    if edge.getId() in used_edges:
                        node_edges.remove(edge)
                # pick edge and add target to path
                edge = np.random.choice(node_edges)
                path.append(edge.getTarget())
                used_edges.append(edge.getId())
                used_edges.append(edge.getTarget() + '__' + edge.getSource())
            else:
                prev = str(path_dict[path[-1]]['prev'])
                used_edges.append(path[-1] + '__' + prev)
                used_edges.append(prev + '__' + path[-1])
                path.append(prev)
                

        path.reverse()
        self.epsilon -= self.gamma
        return path


    def Djikstras(self, source: str):
        visited = [False for _ in range(len(self.graph.getNodes()))]
        dist = [float('inf') for _ in range(len(self.graph.getNodes()))]
        prev = [None for _ in range(len(self.graph.getNodes()))]
        dist[int(source)] = 0

        while not all(visited):

            vist_node = self.minDistance(dist, visited)
            visited[vist_node] = True

            for node in range(len(dist)):
                if self.qMatrix[vist_node][node] > 0 and not visited[node] and dist[node] > dist[vist_node] + self.qMatrix[vist_node][node]:
                    dist[node] = dist[vist_node] + self.qMatrix[vist_node][node]
                    prev[node] = vist_node
        
        return {str(i): {'prev': prev[i], 'dist': dist[i]} for i in range(len(dist))}


    def minDistance(self, dist: list[float], visited: list[bool]) -> int:
        min = float('inf')
        min_index = -1
        for i in range(len(dist)):
            if dist[i] < min and not visited[i]:
                min = dist[i]
                min_index = i
        return min_index
        
    
    '''Method for updating the Q matrix given a path'''
    def updateQMatrix(self, path: list[str]) -> None:
        path_sample = self.graph.samplePath(path)
        for i in range(len(path)-1):
            # increment the use matrix
            self.useMatrix[int(path[i])][int(path[i+1])] += 1
            # update the q matrix
            n = self.useMatrix[int(path[i])][int(path[i+1])]
            old_val = self.qMatrix[int(path[i])][int(path[i+1])]
            self.qMatrix[int(path[i])][int(path[i+1])] = (old_val * (n - 1) + path_sample[i]) / n 