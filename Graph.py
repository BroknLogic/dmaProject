import dash
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
        self.len_range = (5, 20)
        self.nodes, self.dashNodes = self.makeNodes(nodeCount)
        self.edges: list[Edge] = self.makeEdges(self.nodes, extraEdges, len_range=self.len_range)
        self.random = np.random.normal
        self.location = 0
        self.animate = False
    
    
    def samplePath(self, path: list[str]) -> list[float]:
        samples = []
        for i in range(len(path)-1):
            node = self.nodes[int(path[i])] 
            for edge in node.getEdges():
                if edge.getId() == node.getId() + '__' + path[i+1]:
                    samples.append(max(0, self.random(*edge.randParams())))
                    break
        return samples
    
    def getBlankQMatrix(self, default_val: float = 1.0):
        qMatrix = np.zeros((len(self.nodes), len(self.nodes)))
        for node in self.nodes:
            for edge in node.getEdges():
                qMatrix[int(node.getId())][int(edge.getTarget())] = default_val

        return qMatrix
            
    def getNodes(self) -> list[Node]:
        return self.nodes
    
    def getDashNodes(self, location) -> dict[str,str]:
        return self.dashNodes
    
    def getEdges(self) -> list[Edge]:
        return self.edges
    
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


    def getDeliveries(self, numDelivieries: int, scaler: float) -> dict[str,int]:
        
        return [(str(np.random.randint(1, len(self.nodes))), np.random.uniform() * scaler) for _ in range(numDelivieries)]


    def visualizeNetwork(self, deliveries, paths, qMap) -> None:
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
            'background-color': 'black',
            'line-color': 'black'
        }
    }, 
    {
        'selector': '.delivery',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }
    },
    {
        'selector': '.path',
        'style': {
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
            html.Button('Start/Stop Animation', id='submit-val',),
            dcc.Interval(id='interval', interval=0.5*1000, n_intervals=0)
        ])

        @app.callback(Output('net', 'elements'),
                      Input('interval', 'n_intervals'))
        def update_elements(data):
            dashNodes = self.dashNodes
            self.location += 1
            if self.location > len(deliveries) - 1:
                self.location = 0
            for i in range(len(dashNodes)):
                if i == int(deliveries[self.location]):
                    if dashNodes[i]['classes'] == '':
                        dashNodes[i]['classes'] += 'delivery'
                else:
                    dashNodes[i]['classes'] = ''
            dashNodes[0]['classes'] = 'location'
            dashEdges = [edge.toDict() for edge in self.edges]
            for i in range(len(dashEdges)):
                width = qMap[i][int(dashEdges[i]['data']["source"])][int(dashEdges[i]['data']['target'])]
                dashEdges[i]['style'] = {"width": int(self.len_range[1] * 1.5 - width)}
                if dashEdges[i]['data']['label'] in paths[self.location]:
                    dashEdges[i]['classes'] = 'path'
                else:
                    dashEdges[i]['classes'] = ''
                    
            elements= self.dashNodes + dashEdges
            return elements

        @app.callback(Output('interval', 'disabled'),
                      Input('submit-val', 'n_clicks'))
        def testing(button):
            self.animate = not self.animate
            return self.animate
        
        app.run_server(debug=True)