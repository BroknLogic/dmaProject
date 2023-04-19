import matplotlib.pyplot as plt
from Node import Node
from Graph import Graph
from Edge import Edge
import numpy as np
from OptimalScheduler import OptimalScheduler

def breadth_first(Nodes: list[Node]):
    queue = []
    source = Nodes[0]
    destination = Nodes[-1]
    visited = {}
    visited[source.getId()] =  np.inf
    queue.append(source)
    
    while (len(queue)> 0):
        current = queue.pop(0) 
        for edge in current.getEdges():
            to_node = edge.getTarget()
            if to_node not in visited:
                queue.append(Nodes[int(to_node)])
                visited[to_node] = current.getId()
    
    path = [destination.getId()]
    
    while path[-1] != source.getId():
        path.append(visited[path[-1]])
    
    path.reverse()
    return path

def plot_profit(days: int, profits: list[float]):
    plt.plot(range(days), profits)
    plt.xlabel('Days')
    plt.ylabel('Profit')
    plt.title('Profit over time')
    plt.show()
        
        

def main():
    nodeCount = 20
    extraEdges = 20
    number_of_days = 1000
    num_packages = 100
    graph = Graph(nodeCount, extraEdges)
    optimizer = OptimalScheduler(graph, graph.getBlankQMatrix())

    profit = []
    for _ in range(number_of_days):
        packages = graph.getDeliveries(100, 400)
        
        profit_for_day, real_paths = optimizer.simulateDay(packages, 8 * 60)
        profit.append(profit_for_day)

    optimizer.printQMatrix()
    plot_profit(number_of_days, profit)

    for edge in graph.getEdges():
        print(f'{edge.getId()} : {edge.randParams()}')

    graph.visualizeNetwork()

    
# define main calling
if __name__ == '__main__':
    main()
    