import numpy as np
from Graph import Graph
from Edge import Edge
from Node import Node
import typing

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



def calc_choice(curr_node: Node, pheromone_graph: np.ndarray[typing.Any]) -> int:
    node_idx = int(curr_node.getId())
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

def decay_pheromone(pheromone_graph: np.ndarray[typing.Any]) -> None:
    for i in range(len(pheromone_graph)):
        for j in range(len(pheromone_graph[i])):
            pheromone_graph[i][j] *= 0.9

def ant_search(graph: Graph, start_node: Node, time_limit:float, number_of_ants: int, packages: list[tuple[int, float]]):
    pheromone_graph = graph.getBlankQMatrix(1.0)
    curr_node = start_node
    for i in range(number_of_ants):
        time = 0.0
        path = [start_node.getId()]
        length_of_trail = 0.0
        total_profit = 0.0
        while time < time_limit:
            next_node_id = calc_choice(start_node, pheromone_graph)
            next_node = graph.getNode(next_node_id)
            current_profit = [(i , package[1]) for i, package in enumerate(packages) if package[0] == int(next_node_id)]
            index_of_best_package = max(current_profit, key=lambda x: x[1])[0]
            profit = packages[index_of_best_package][1]
            packages.pop(index_of_best_package)
            time_of_edge = sum(graph.samplePath([curr_node.getId(), next_node.getId()]))
            decay_pheromone(pheromone_graph)
            if length_of_trail + time_of_edge < time_limit:
                path.append(next_node.getId())
                length_of_trail += time_of_edge
                total_profit += profit
                curr_node = next_node
            else:
                break
        propogate_pheromones(path, pheromone_graph, length_of_trail, profit)
    best_path_overall = best_path(start_node.getId(), path[-1], packages, time_limit)
    return best_path_overall

def best_path(source: int, pheremone_graph: list[list[float]], packages: dict[str, int], time_limit: float) -> list[int]:
    path = [source]
    profit = 0.0
    length_of_trail = 0.0
    total_profit = 0.0
    time = 0.0
    while time < time_limit:
        next_node = np.argmax(pheremone_graph[int(path[-1])])
        current_profit = [(i , package[1]) for i, package in enumerate(packages) if package[0] == int(next_node_id)]
        index_of_best_package = max(current_profit, key=lambda x: x[1])[0]
        profit = packages[index_of_best_package][1]
        packages.pop(index_of_best_package)
        time_of_edge = sum(graph.samplePath([curr_node.getId(), next_node.getId()]))
        decay_pheromone(pheromone_graph)
        if length_of_trail + time_of_edge < time_limit:
            path.append(next_node.getId())
            length_of_trail += time_of_edge
            total_profit += profit
        else:
            break

        path.append(next_node)
    
    return profit

def propogate_pheromones(path: list[int], pheromone_graph: np.ndarray[typing.Any], length_of_trail: float, profit: float):
    for i in range(len(path) - 1):
        pheromone_graph[path[i]][path[i+1]] += profit/length_of_trail
        pheromone_graph[path[i+1]][path[i]] += profit/length_of_trail

def main():
    nodeCount = 20
    extraEdges = 0
    number_of_days = 1000
    num_packages = 100
    graph = Graph(nodeCount, extraEdges)

    profit = []
    for _ in range(number_of_days):
        packages = graph.getDeliveries(100, 400)
        
        profit_for_day = ant_search(graph, graph.getNode(0), 60* 8.0, 100, packages)
        profit.append(profit_for_day)

    plot_profit(number_of_days, profit)

    

if __name__ == "__main__":
    main()