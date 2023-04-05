# imports
import dash
import visdcc
import pandas as pd
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import random
from Node import Node
from collections import deque


def getNodes(nodeCount):
    nodes = [Node(str(i)) for i in range(nodeCount)]
    dashNodes = [{'id': str(i), 'label': str(i), 'shape': 'dot', 'size': 7} for i in range(nodeCount)]
    return nodes, dashNodes

def getEdges(nodes, extraEdges):
    nodesAdded = []
    edges = []
    for node in nodes:
        if len(nodesAdded) == 0:
            nodesAdded.append(node.id)
        else:
            source, target = random.choice(nodesAdded), node.id
            mean = random.randrange(1, 7)
            edge = {
                'id': source + "__" + target,
                'from': source,
                'to': target,
                'width': mean, 
                'mean': mean,
                'stdDev': random.randrange(1, 7)
            }
            node.addEdge(edge)
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
        contains = False
        for testEdge in edges:
            if testEdge['id'] == edge['id'] or testEdge['to'] + '__' + testEdge['from'] == edge['id']:
                contains = True
        if not contains and source != target:
            edges.append(edge)
            nodes[int(source)].addEdge(edge)
    return edges


def visualizeNetwork(nodes, edges):
    app = dash.Dash()

    # define layout
    app.layout = html.Div([
        visdcc.Network(id = 'net', 
                        data = {'nodes': nodes, 'edges': edges},
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

def breadth_first(Nodes: list[Node]):
    queue = deque()
    source = Nodes[0]
    destination = Nodes[-1]
    visited = {}
    visited[source.getId()] =  np.inf
    queue.append(source)
    
    while (len(queue)> 0):
        current = queue.popleft()
        
        for edge in current.edges:
            to_node = edge['to']
            if to_node not in visited:
                queue.append(Nodes[int(to_node)])
                visited[to_node] = current.getId()
        print(queue)
    path = [visited[destination.getId()]]
    
    while path[-1] != source.getId():
        path.append(visited[path[-1]])
    
    path.reverse()
    return path
        
        

def main():
    nodeCount = 20
    nodes, dashNodes = getNodes(nodeCount)

    extraEdges = 20
    edges = getEdges(nodes, extraEdges)
    for node in nodes:
        print(node.id)
        for edge in node.edges:
            print(edge)
    try:
        print(breadth_first(nodes))
    except:
        pass
    
    visualizeNetwork(dashNodes, edges)

    
# define main calling
if __name__ == '__main__':
    main()
    