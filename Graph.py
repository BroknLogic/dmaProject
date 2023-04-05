import dash
import visdcc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import random
from Node import Node


class Graph:
    
    def __init__(self, nodeCount: int, extraEdges: int):
        self.nodes, self.dashNodes = self.makeNodes(nodeCount)
        self.edges = self.makeEdges(self.nodes, extraEdges)
    
    
    def getNodes(self) -> list[Node]:
        return self.nodes
    
    def getDashNodes(self) -> dict[str,str]:
        return self.dashNodes
    
    def getEdges(self) -> dict[str, str]:
        return self.edges
    
    def makeNodes(self, nodeCount: int) -> tuple[list[Node], dict[str,str]]:
        nodes = [Node(str(i)) for i in range(nodeCount)]
        dashNodes = [{'id': str(i), 'label': str(i), 'shape': 'dot', 'size': 7} for i in range(nodeCount)]
        return nodes, dashNodes

    def makeEdges(self, nodes: list[Node], extraEdges: int) -> dict[str, str]:
        nodesAdded = []
        edges = []
        for node in nodes:
            if len(nodesAdded) == 0:
                nodesAdded.append(node.id)
            else:
                source, target = random.choice(nodesAdded), node.id
                mean = random.randrange(1, 7)
                stdDev = random.randrange(1, 7)
                edge = {
                    'id': source + "__" + target,
                    'from': source,
                    'to': target,
                    'width': mean, 
                    'mean': mean,
                    'stdDev': stdDev
                }
                edge2 = {
                    'id': target + "__" + source,
                    'from': target,
                    'to': source,
                    'width': mean, 
                    'mean': mean,
                    'stdDev': stdDev
                }
                nodes[int(source)].addEdge(edge)
                nodes[int(target)].addEdge(edge2)
                edges.append(edge)
                nodesAdded.append(node.getId())
        edgeNum = len(edges)
        while len(edges) < edgeNum + extraEdges:
            source, target = random.choice(nodesAdded), random.choice(nodesAdded)
            mean = random.randrange(1, 7)
            edge = {
                'id': source + "__" + target,
                'from': source,
                'to': target,
                'width': mean, 
                'mean': mean,
                'stdDev': random.randrange(1, 7)
            }
            edge2 = {
                'id': target + "__" + source,
                'from': target,
                'to': source,
                'width': mean, 
                'mean': mean,
                'stdDev': stdDev
            }
            contains = False
            for testEdge in edges:
                if testEdge['id'] == edge['id'] or testEdge['to'] + '__' + testEdge['from'] == edge['id']:
                    contains = True
            if not contains and source != target:
                edges.append(edge)
                nodes[int(source)].addEdge(edge)
                nodes[int(target)].addEdge(edge2)
        return edges


    def visualizeNetwork(self) -> None:
        app = dash.Dash()

        # define layout
        app.layout = html.Div([
            visdcc.Network(id = 'net', 
                            data = {'nodes': self.dashNodes, 'edges': self.edges},
                            options = dict(height= '600px', width= '100%')),
            dcc.RadioItems(id = 'color',
                            options=[{'label': 'Red'  , 'value': '#ff0000'},
                                    {'label': 'Green', 'value': '#00ff00'},
                                    {'label': 'Blue' , 'value': '#0000ff'} ],
                            value='Red'  )             
                            ])

        @app.callback(
        Output('net', 'options'),
        [Input('color', 'value')])
        def myfun(x):
            return {'nodes':{'color': x}}
        
        app.run_server(debug=True)