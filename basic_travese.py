from Node import Node
from Graph import Graph
from Edge import Edge
import numpy as np

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
        
        

def main():
    nodeCount = 20
    extraEdges = 20
    graph = Graph(nodeCount, extraEdges)
    nodes = graph.getNodes()
    
    for node in nodes:
        print(node.getId())
        for edge in node.getEdges():
            print(edge.toDict())
    
    
    path = breadth_first(nodes)
    print(path)
    sample = graph.samplePath(path)
    print(sample)

    q = graph.getBlankQMatrix()
    for row in q:
        print(row)

    graph.visualizeNetwork()

    
# define main calling
if __name__ == '__main__':
    main()
    