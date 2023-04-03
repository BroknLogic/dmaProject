class Node:
    def __init__(self, id) -> None:
        self.id = id
        self.edges = []

    def getId(self):
        return self.id

    def addEdge(self, edge):
        self.edges.append(edge)

    def getEdges(self):
        return self.edges