from Edge import Edge

class Node:
    def __init__(self, id: str) -> None:
        self.id: str = id
        self.edges: list[Edge] = []

    def getId(self) -> str:
        return self.id

    def addEdge(self, edge) -> None:
        self.edges.append(edge)

    def getEdges(self) -> list[Edge]:
        return self.edges