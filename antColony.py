import numpy as np
from Graph import Graph
from Edge import Edge
from Node import Node

class AntColony:

    def __init__(self, graph: Graph, start_node: Node, epsilon: float = 0.5, gamma: float = 0.01, number_of_ants: int = 100, ):
        self.graph = graph
        self.epsilon = epsilon
        self.gamma = gamma
        self.number_of_ants = number_of_ants
    
    # def calc_choice(self, curr_pos: int, pheromone_graph: list[list[float]], visited: list[int]) -> int:
    #     node_idx = curr_pos
    #     row_of_node = self.qMatrix[node_idx]
    #     connected_nodes = [i for i in range(len(row_of_node)) if row_of_node[i] != 0 and i not in visited]
    #     phero_vals = [pheromone_graph[node_idx][i] for i in connected_nodes]
    #     sum_vals = sum(phero_vals)
    #     prob_values = [i/sum_vals for i in phero_vals]
    #     cutoffs = [sum(prob_values[:i+1]) for i in range(len(prob_values))]
    #     random_value = np.random.uniform(0.0,1.0)

    #     for i in range(len(cutoffs)):
    #         if random_value <= cutoffs[i]:
    #             return connected_nodes[i]
    #     raise Exception("No node was chosen")
    
    # def calc_pheromone_value(self, path: list[int], pheromone_graph) -> None:
    #     len_of_path = 0
    #     for i in range(len(path) - 2):
    #         current_cost = self.qMatrix[path[i]][path[i+1]]
    #         len_of_path += current_cost
    #     for i in range(len(path) - 2):
    #         pheromone_graph[path[i]][path[i+1]] += 1/len_of_path
    #         pheromone_graph[path[i+1]][path[i]] += 1/len_of_path

    # def decay(self, pheromone_graph) -> None:
    #     for i in range(len(pheromone_graph)):
    #         for j in range(len(pheromone_graph[i])):
    #             pheromone_graph[i][j] *= 0.9
    
    # def find_ants_path(self, curr_pos: int, target: int, pheromone_graph: list[list[float]]):
    #     path = [curr_pos]
    #     while path[-1] != target:
    #         next_node = self.calc_choice(path[-1], pheromone_graph, path)
    #         path.append(next_node)
    #     return path

    # def populate_pheromones(self, source: int, target: int):
    #     pheromone_graph = self.graph.getBlankQMatrix(1.)
    #     for i in range(self.number_of_ants):
    #         path = self.find_ants_path(source, target, pheromone_graph)
    #         self.calc_pheromone_value(path, pheromone_graph)
    #         self.decay(pheromone_graph)
        
    #     return self.getPhermonePath(target, source, pheromone_graph)

    # def getPheremonePath(self, source: int, target: int, pheremone_graph: list[list[float]]) -> list[int]:
    #     path = [source]
    #     while path[-1] != target:
    #         next_node = np.argmax(pheremone_graph[int(path[-1])])
    #         path.append(next_node)
        
    #     return path

def getRealPath(source: str, target: str, path_dict: dict[str, dict[str, int]]) -> list[str]:
    path = [target]
    used_edges = set()
    while path[-1] != source:
        prev = str(path_dict[path[-1]]['prev'])
        if f'{prev}__{path[-1]}' not in used_edges:    
            used_edges.add(path[-1] + '__' + prev)
            used_edges.add(prev + '__' + path[-1])
        path.append(prev)
    path.reverse()
    # Reduce randomness
    return path



def calc_choice(curr_node: Node, pheromone_graph: list[list[float]]) -> int:
    node_idx = curr_pos
    row_of_node = self.qMatrix[node_idx]
    connected_nodes = [i for i in range(len(row_of_node)) if row_of_node[i] != 0]
    phero_vals = [pheromone_graph[node_idx][i] for i in connected_nodes]
    sum_vals = sum(phero_vals)
    prob_values = [i/sum_vals for i in phero_vals]
    cutoffs = [sum(prob_values[:i+1]) for i in range(len(prob_values))]
    random_value = np.random.uniform(0.0,1.0)

    for i in range(len(cutoffs)):
        if random_value <= cutoffs[i]:
            return connected_nodes[i]
    raise Exception("No node was chosen")

def decay_pheromone(pheromone_graph: list[list[float]]) -> None:
    for i in range(len(pheromone_graph)):
        for j in range(len(pheromone_graph[i])):
            pheromone_graph[i][j] *= 0.9

def ant_search(graph: Graph, start_node: Node, time_limit:float, number_of_ants: int, packages: dict[str, int]):
    pheromone_graph = graph.getBlankQMatrix(1.0)
    curr_node = start_node
    for i in range(number_of_ants):
        time = 0.0
        path = [curr_node.getId()]
        length_of_trail = 0.0
        profit = 0.0
        while time < time_limit:
            next_node_id = calc_choice(start_node, pheromone_graph)
            next_node = graph.getNode(next_node_id)
            current_profit = packages[next_node.getId()]
            edge_from_curr_to_next = curr_node.getEdge(curr_node.getId(), next_node.getId())
            mean, std = edge_from_curr_to_next.randParams()
            time_of_edge = np.random.normal(mean, std)
            decay_pheromone(pheromone_graph)
            if length_of_trail + time_of_edge < time_limit:
                path.append(next_node.getId())
                length_of_trail += time_of_edge
                profit += current_profit
            else:
                break
        propogate_pheromones(path, pheromone_graph, length_of_trail, profit)

def best_path(self, source: int, target: int, pheremone_graph: list[list[float]], packages: dict[str, int]) -> list[int]:
    path = [source]
    profit = 0.0
    while path[-1] != target:
        next_node = np.argmax(pheremone_graph[int(path[-1])])
        
        path.append(next_node)
    
    return path   

def propogate_pheromones(path: list[int], pheromone_graph: list[list[float]], length_of_trail: float, profit: float):
    for i in range(len(path) - 1):
        pheromone_graph[path[i]][path[i+1]] += profit/length_of_trail
        pheromone_graph[path[i+1]][path[i]] += profit/length_of_trail
                



def main():
    nodeCount = 20
    extraEdges = 0
    number_of_days = 1000
    num_packages = 100
    graph = Graph(nodeCount, extraEdges)
    optimizer = OptimalScheduler(graph, graph.getBlankQMatrix(), epsilon=0.7)

    profit = []
    for _ in range(number_of_days):
        packages = graph.getDeliveries(100, 400)
        
        profit_for_day = optimizer.simulateDay(packages, 8 * 60)
        profit.append(profit_for_day)

    plot_profit(number_of_days, profit)

    

if __name__ == "__main__":
    main()