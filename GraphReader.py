from Graph import GraphVertex, Graph
from GenericCSVReader import readCSVFile

#function read in a graph using adjacentcy matrix
def readGraph1(path):
    graph1 = Graph()

    f = open(path, 'r')
    read_data = f.read()
    lineList = read_data.split("\n")

    for i in range(0, len(lineList) - 1):
        line = lineList[i]
        data = line.split(",")

        #Finds the vertex in the graph, if doesn't exist then create a new vertex
        if not (data[0] in graph1):
            rootVertex = GraphVertex(data[0])
            graph1.add_vertex(rootVertex)
        else:
            rootVertex = graph1.vertexList[data[0]]

        #Adds the adjacent vertex to the adj-list of the root vertex
        for i in range(1, len(data)):
            if not (data[i] in graph1):
                adjVertex = GraphVertex(data[i])
                graph1.add_vertex(adjVertex)
            else:
                adjVertex = graph1.vertexList[data[i]]

            rootVertex.add_adjacent(adjVertex)

    return graph1


#This function reads a graph using adj-matrix format
def readGraph2(path):
    vertex_key = []
    graph = Graph()
    data = readCSVFile(path)

    for k, v in data[0].items():
        vertex = GraphVertex(k)
        graph.add_vertex(vertex)
        vertex_key.append(k)

    for i, line in enumerate(data):
        if i < len(data) - 1:
            for k, v in line.items():
                if str(v) != '_':
                    graph.vertexList[vertex_key[i]].add_adjacent(graph.vertexList[k], int(v))
                    
    return graph
