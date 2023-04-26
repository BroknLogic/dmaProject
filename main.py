import matplotlib.pyplot as plt
from Node import Node
from Graph import Graph
from Edge import Edge
import numpy as np
from OptimalScheduler import OptimalScheduler
from MonteCarlo import MonteCarlo

def plot_profit(days: int, greedy_profits: list[float] = None, monteCarlo_profits: list[float]=None):
    plt.xlabel('Days')
    plt.ylabel('Profit')
    plt.title('Profit over time')
    plt.plot(range(days), greedy_profits)
    plt.plot(range(days), monteCarlo_profits)
    plt.legend(['Greedy', 'Monte Carlo'])
    plt.savefig('Figures/GreedyvsMonteCarlo.png')
    plt.show()
        
        

def main():
    nodeCount = 20
    extraEdges = 0
    number_of_days = 1000
    num_packages = 300
    graph = Graph(nodeCount, extraEdges)
    optimizer = OptimalScheduler(graph, graph.getBlankQMatrix(), epsilon=0.7)
    monteCarlo = MonteCarlo(graph, 100)
    
    greedy_profit = []
    monteCarlo_profit = []
    
    for _ in range(number_of_days):
        packages = graph.getDeliveries(num_packages, 400)
        
        greedy_profit_for_day = optimizer.simulateDay(packages, 8 * 60)
        montecarlo_profit_for_day = monteCarlo.simulateDay(packages, 8 * 60)
        
        greedy_profit.append(greedy_profit_for_day)
        monteCarlo_profit.append(montecarlo_profit_for_day)

    plot_profit(number_of_days, greedy_profit, monteCarlo_profit)

    real_paths = optimizer.real_paths
    q_graphs = optimizer.q_graphs

    for edge in graph.getEdges():
        print(f'{edge.getId()} : {edge.randParams()}')

    deliveries, paths = [], []
    for path in real_paths:
        deliveries.append(path[-1])
        stuff = [f"{path[i]}__{path[i+1]}" for i in range(len(path) -1)]
        stuff += [f"{path[i+1]}__{path[i]}" for i in range(len(path) -1)]
        paths.append(stuff)

    optimizer.printQMatrix()

    graph.visualizeNetwork(deliveries, paths, q_graphs)

    
# define main calling
if __name__ == '__main__':
    main()
    
