from Node import Node
from Graph import Graph


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
            to_node = edge['to']
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
    nodes = graph.getNodes(nodeCount)
    edges = graph.getEdges(nodes, extraEdges)
    
    print(breadth_first(nodes))
    
    graph.visualizeNetwork(graph.getDashNodes(), edges)

    
# define main calling
if __name__ == '__main__':
    main()
    