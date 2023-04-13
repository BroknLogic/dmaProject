import dash
import visdcc
import dash_cytoscape as cyto
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import random
from Node import Node
from Edge import Edge
import numpy as np



class Graph:
    
    def __init__(self, nodeCount: int, extraEdges: int):
        self.nodes, self.dashNodes = self.makeNodes(nodeCount)
        self.id_to_node = {int(node.getId()): node for node in self.nodes}
        self.edges: list[Edge] = self.makeEdges(self.nodes, extraEdges)
        self.source_target_to_edge: dict[str, Edge]= {edge.getSource() + edge.getTarget(): edge for edge in self.edges}
        self.random = np.random.normal
        self.location = 0
    
    
    def samplePath(self, path: list[str]) -> list[float]:
        samples = []
        for i, node_id in enumerate(path[:-1]):
            node = self.nodes[int(node_id)] 
            for edge in node.getEdges():
                if edge.getId() == node_id + '__' + path[i+1]:
                    samples.append(max(0, self.random(*edge.randParams())))
                    break
        return samples
    
    def getBlankQMatrix(self, default_val: float = 1.0) -> np.ndarray[np.ndarray[float]]:
        qMatrix = np.zeros((len(self.nodes), len(self.nodes)))
        for node in self.nodes:
            for edge in node.getEdges():
                qMatrix[int(node.getId())][int(edge.getTarget())] = default_val

        return qMatrix
            
    def getNodes(self) -> list[Node]:
        return self.nodes
    
    def getNode(self, id_: int) -> Node:
        return self.id_to_node[id_]

    def getDashNodes(self, location) -> dict[str,str]:
        return self.dashNodes
    
    def getEdges(self) -> dict[str, str]:
        return self.edges
    
    def getEdge(self, source: str, target: str) -> Edge:
        return self.source_target_to_edge[source + target]
    
    def makeNodes(self, nodeCount: int) -> tuple[list[Node], dict[str,str]]:
        nodes = [Node(str(i)) for i in range(nodeCount)]
        dashNodes = [{'data': {'id': str(i), 'label': str(i)}, 'classes':'location' if i == 0 else ''} for i in range(nodeCount)]
        return nodes, dashNodes

    def makeEdges(self, nodes: list[Node], extraEdges: int, len_range: tuple[int, int] = (5, 20)) -> dict[str, str]:
        nodesAdded = []
        edges: list[Edge]= []
        for node in nodes:
            if len(nodesAdded) == 0:
                nodesAdded.append(node.id)
            else:
                source, target = random.choice(nodesAdded), node.id
                mean = random.randrange(*len_range)
                stdDev =  mean//4
                edge = Edge(source, target, mean, stdDev)
                edge2 = Edge(target, source, mean, stdDev)
                nodes[int(source)].addEdge(edge)
                nodes[int(target)].addEdge(edge2)
                edges.append(edge)
                nodesAdded.append(node.getId())
        edgeNum = len(edges)
        while len(edges) < edgeNum + extraEdges:
            source, target = random.choice(nodesAdded), random.choice(nodesAdded)
            mean = random.randrange(*len_range)
            stdDev = random.randrange(1, max(mean//4, 2))
            edge = Edge(source, target, mean, stdDev)
            edge2 = Edge(target, source, mean, stdDev)
            contains = False
            for testEdge in edges:
                if testEdge.getId() == edge.getId() or testEdge.getTarget() + '__' + testEdge.getSource() == edge.getId():
                    contains = True
            if not contains and source != target:
                edges.append(edge)
                nodes[int(source)].addEdge(edge)
                nodes[int(target)].addEdge(edge2)
        return edges


    def getDeliveries(self, numDelivieries: int) -> dict[str,int]:
        deliveries = {}
        for i in numDelivieries:
            node = random.choice(self.nodes)
            deliveries[node.getId] = random.uniform(10, 50)
        return deliveries


    def visualizeNetwork(self) -> None:
        app = dash.Dash()

        default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#A3C4BC'
        }
    },
    {
        'selector': '.location',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }
    }
]

        # define layout
        app.layout = html.Div([
            cyto.Cytoscape(
                id='net',
                layout={'name': 'breadthfirst'},
                stylesheet=default_stylesheet,
                style={'width': '100%', 'height': '400px'},
                elements= self.dashNodes + [edge.toDict() for edge in self.edges]
            ),
            html.Button('Submit', id='submit-val', n_clicks=0),
        ])

        @app.callback(Output('net', 'elements'),
              Input('submit-val', 'n_clicks'))
        def update_elements(button):
            dashNodes = self.dashNodes
            self.location += 1
            if self.location > len(dashNodes) - 1:
                self.location = 0
            for i in range(len(dashNodes)):
                if i == self.location:
                    dashNodes[i]['classes'] += 'location'
                else:
                    dashNodes[i]['classes'] = ''
            elements= self.dashNodes + [edge.toDict() for edge in self.edges]
            return elements

        
        app.run_server(debug=True)