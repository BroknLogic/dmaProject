import numpy as np
from Graph import Graph

class OptimalScheduler:

    def __init__(self, graph: Graph, qMatrix: np.ndarray[np.ndarray[float]], depotNode: str = '0', epsilon: float = 0.5, gamma: float = 0.01):
        self.graph = graph
        self.qMatrix = qMatrix
        self.useMatrix = np.zeros_like(qMatrix)
        self.epsilon = epsilon
        self.gamma = gamma
        self.source = depotNode
    
    '''Method of getting a path between source and target with user defined randomness given SSSP dictionary'''
    def getRealPath(self, source: str, target: str, path_dict: dict[str, dict[str, int]]) -> list[str]:
        path = [target]
        used_edges = set()
        while path[-1] != source:
            # Epsilon Greedy
            if np.random.uniform(0.0,1.0) < self.epsilon:
                # get all of the edges for the current node
                node_edges = self.graph.getNodes()[int(path[-1])].getEdges().copy()
                # remove an edge if it was already traversed
                for edge in node_edges:
                    if edge.getId() in used_edges:
                        node_edges.remove(edge)
                # Continue if there are no possible random edges
                if len(node_edges) == 0:
                    continue
                # pick edge and add target to path
                edge = np.random.choice(node_edges)
                path.append(edge.getTarget())
                used_edges.add(edge.getId())
                used_edges.add(edge.getTarget() + '__' + edge.getSource())
            else:
                # Pick optimal path
                prev = str(path_dict[path[-1]]['prev'])
                if f'{prev}__{path[-1]}' not in used_edges:    
                    used_edges.add(path[-1] + '__' + prev)
                    used_edges.add(prev + '__' + path[-1])
                path.append(prev)
        path.reverse()
        # Reduce randomness
        self.epsilon -= self.gamma

        return path

    '''Djikstra's algorithm for finding shortest path from source to all other nodes'''
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

    '''Method for finding the minimum distance node'''
    def minDistance(self, dist: list[float], visited: list[bool]) -> int:
        min = float('inf')
        min_index = -1
        for i in range(len(dist)):
            if dist[i] < min and not visited[i]:
                min = dist[i]
                min_index = i
        return min_index    
    
    '''Method for updating the Q matrix given a path'''
    def updateQMatrix(self, path: list[str], path_sample: list[float]) -> None:
        for i in range(len(path)-1):
            # increment the use matrix
            self.useMatrix[int(path[i])][int(path[i+1])] += 1
            # update the q matrix
            n = self.useMatrix[int(path[i])][int(path[i+1])]
            old_val = self.qMatrix[int(path[i])][int(path[i+1])]
            self.qMatrix[int(path[i])][int(path[i+1])] = self.qMatrix[int(path[i+1])][int(path[i])] = (old_val * (n - 1) + path_sample[i]) / n 
        
        return 2 * sum(path_sample)

    '''Method for printing the Q matrix'''
    def printQMatrix(self) -> None:
        print(f'{"":5s}', end=' ')
        for i in range(len(self.qMatrix)):
            print(f'{i:5d}', end=' ')
        print()
        for i, row in enumerate(self.qMatrix):
            print(f'{i:5d}', end=' ')
            for col in row:
                print(f'{col:5.2f}', end=' ')
            print()
    
    '''Method for simulating a shift for the a delivery driver'''
    def simulateDay(self, packages: list[tuple[str, float]], time_limit: float):
        total_time = 0.0
        total_profit = 0.0
        while total_time < time_limit and len(packages) > 0:
            # Get the shortest path from the depot to all other nodes
            path_dict = self.Djikstras(self.source)
            
            # Prioritize packages that are left

            # Find the best package to deliver
            best_package, profit = None
            
            total_profit += profit

            time_to_deliver = self.deliverPackage(best_package, path_dict)

            if total_time + time_to_deliver > time_limit:
                break
            else:
                total_time += time_to_deliver
                
            

        pass
    
    '''Method for delivering a single package'''
    def deliverPackage(self, deliveryNode: str, path_dict: dict[str , dict[str, int]]) -> float:
        real_path = self.getRealPath(self.source, deliveryNode, path_dict)
        path_sample = self.graph.getSample(real_path)
        self.updateQMatrix(real_path, path_sample)

        return 2 * sum(path_sample)



