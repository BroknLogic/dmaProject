import numpy as np
from Graph import Graph
from Node import Node

class MonteCarlo:

    def __init__(self, graph: Graph, numberOfParticles: int, depotNode: str = '0'):
        self.graph: Graph = graph
        self.numberOfParticles = numberOfParticles
        self.depot = depotNode
    
    def breadth_first(self, source, target, Nodes: list[Node]):
        queue = []
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
    
        path = [target]
    
        while path[-1] != source.getId():
            path.append(visited[path[-1]])
    
        path.reverse()
        return path 

    def particleDay(self, packages, timeLimit):
        totalProfit = 0
        totalTime = 0
        
        while totalTime < timeLimit:
            # Get a random package
            package = np.random.choice(packages)
            # Get the path from the package
            path = self.breadth_first(self.depot, package[0], self.graph.getNodes())
            # Get the time it takes to travel the path
            time = 2 * sum(self.graph.samplePath(path))
            # Get the profit of the package
            
            if totalTime + time > timeLimit:
                break
            
            
            # Add the time and profit to the total
            totalTime += time
            totalProfit += package[1]
        
        return totalProfit
        
        
        
    
    def simulateDay(self, packages, timeLimit):
        profit = []
        
        for _ in range(self.numberOfParticles):
            particleProfit = self.particleDay(packages, timeLimit)
            profit.append(particleProfit)
        
        return profit[np.argmax(profit)]