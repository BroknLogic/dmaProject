import numpy as np
from Graph import Graph
from Edge import Edge
from Node import Node

class OptimalScheduler:

    def __init__(self, graph: Graph, qMatrix: np.ndarray[np.ndarray[float]], epsilon: float = 0.5, gamma: float = 0.01, number_of_ants: int = 100):
        self.graph = graph
        self.qMatrix = qMatrix
        self.useMatrix = np.zeros_like(qMatrix)
        self.epsilon = epsilon
        self.gamma = gamma
        self.number_of_ants = number_of_ants
    
    '''Method of getting a path between source and target with user defined randomness given SSSP dictionary'''
    def getRealPath(self, target: str, source: str, path_dict: dict[str, list[str]]) -> list[str]:
        path = [target]
        used_edges: list[str] = []
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
                target = path_dict[path[-1]][-2]
                used_edges.append(f"{path[-1]}__{target}")
                used_edges.append(f"{target}__{path[-1]}")
                path.append(target)
                

        path.reverse()
        self.epsilon -= self.gamma
        return path
    
    def calc_choice(self, curr_pos: int, pheromone_graph: list[list[float]], visited: list[int]) -> int:
        node_idx = curr_pos
        row_of_node = self.qMatrix[node_idx]
        connected_nodes = [i for i in range(len(row_of_node)) if row_of_node[i] != 0 and i not in visited]
        phero_vals = [pheromone_graph[node_idx][i] for i in connected_nodes]
        sum_vals = sum(phero_vals)
        prob_values = [i/sum_vals for i in phero_vals]
        cutoffs = [sum(prob_values[:i+1]) for i in range(len(prob_values))]
        random_value = np.random.uniform(0.0,1.0)

        for i in range(len(cutoffs)):
            if random_value <= cutoffs[i]:
                return connected_nodes[i]
        raise Exception("No node was chosen")
    
    def calc_pheromone_value(self, path: list[int], pheromone_graph) -> None:
        len_of_path = 0
        for i in range(len(path) - 2):
            current_cost = self.qMatrix[path[i]][path[i+1]]
            len_of_path += current_cost
        for i in range(len(path) - 2):
            pheromone_graph[path[i]][path[i+1]] += 1/len_of_path
            pheromone_graph[path[i+1]][path[i]] += 1/len_of_path

    def decay(self, pheromone_graph) -> None:
        for i in range(len(pheromone_graph)):
            for j in range(len(pheromone_graph[i])):
                pheromone_graph[i][j] *= 0.9
    
    def find_ants_path(self, curr_pos: int, target: int, pheromone_graph: list[list[float]]):
        path = [curr_pos]
        while path[-1] != target:
            next_node = self.calc_choice(path[-1], pheromone_graph, path)
            path.append(next_node)
        return path

    def populate_pheromones(self, source: int, target: int):
        pheromone_graph = self.graph.getBlankQMatrix(1.)
        for i in range(self.number_of_ants):
            path = self.find_ants_path(source, target, pheromone_graph)
            self.calc_pheromone_value(path, pheromone_graph)
            self.decay(pheromone_graph)
        
        return self.getPhermonePath(target, source, pheromone_graph)

    def getPheremonePath(self, source: int, target: int, pheremone_graph: list[list[float]]) -> list[int]:
        path = [source]
        while path[-1] != target:
            next_node = np.argmax(pheremone_graph[int(path[-1])])
            path.append(next_node)
        
        return path

    def getSSSP(self, source: int, target_nodes: list[int]) -> dict[str, list[str]]:
        path_dict = {}
        for node in target_nodes:
            if node in path_dict:
                continue
            path = self.populate_pheromones(source, node)
            for i in range(len(path) - 1, 0, -1):
                if path[i] not in path_dict:
                    path_dict[str(path[i])] = path[0:i+1]
        return path_dict
    
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

if __name__ == "__main__":
    nodeCount = 20
    extraEdges = 20
    graph = Graph(nodeCount, extraEdges)
    nodes = graph.getNodes()
    
    for node in nodes:
        print(node.getId())
        for edge in node.getEdges():
            print(edge.toDict())
    
    OptimalScheduler_ = OptimalScheduler(graph, graph.getBlankQMatrix(1.0))
    targets = [i for i in range(1, nodeCount)]
    path_dict = OptimalScheduler_.getSSSP(0, targets)
    print(path_dict)
    

    graph.visualizeNetwork()