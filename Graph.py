from Heap import Heap
from GenericCSVReader import readCSVFile
import math
import sys

class GraphVertex:
    """A class for a vertex of an undirected simple graph"""

    def __init__(self, key):
        self.key = key; #Key is the name given to the vertex
        self.adjList = {} #Adjacency list of the vertex
        self.adjList[key] = {'k':self, 'weight':0}

    def add_adjacent(self, vertex, weight=0):
        if type(vertex) is GraphVertex:
            if vertex.key in self.adjList:
                print("ERROR! " +  vertex.key + " already exist in adj-list of " +
                       self.key + ". It was not added")
            else:
                self.adjList[vertex.key] = {'k': vertex, 'weight': weight}

        else:
            raise TypeError

    #Operator Overloading
    def __str__(self):
        str_list = [str(k) + "(" + str(v['weight']) + ")" for k,v in self.adjList.items()]
        return self.key + "|" + "-".join(str_list)


class Graph:
    """A Class for an undirected simple graph"""

    def __init__(self):
        self.vertexList = {} #A dictionary of vertex in the graph

    def add_vertex(self, vertex):
        if type(vertex) is GraphVertex:
            if vertex.key in self.vertexList:
                print("ERROR! " + vertex.key + " already exist in the vertex list" +
                        ". It was not added")
            else:
                self.vertexList[vertex.key] = vertex
        else:
            raise TypeError

    #Operator Overloading
    #__str__
    def __str__(self):
        str = [vertex.__str__() for k, vertex in self.vertexList.items()]
        return '\n'.join(str)

        return str
    #__contains__
    def __contains__(self,value):
        if type(value) is str:
            return value in self.vertexList
        elif type(value) is GraphVertex:
            return value.key in self.vertexList
        else:
            return False

    #Iterator
    def __iter__(self):
        self._iterCount = 0
        self._iterList = sorted(self.vertexList.keys())
        return self

    def __next__(self):
        if self._iterCount < len(self._iterList):
            self._iterCount = self._iterCount + 1
        else:
            raise StopIteration

        return self.vertexList[self._iterList[self._iterCount - 1]]

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

def dijkstra(graph, source, sink):
    if not(source in graph and sink in graph):
        raise ValueError('source and/or sink does not exist in graph')

    def compareVertex(vertex1, vertex2):
        if(vertex1.dist == vertex2.dist):
            return vertex1.key < vertex2.key
        else:
            return vertex1.dist > vertex2.dist

    path = []
    unvisitedQ = Heap("min", compareVertex)

    print("Performing Djikstra...")
    for vertex in graph:
        vertex.dist = math.inf
        vertex.prev = None
        unvisitedQ.insert(vertex)

    source.dist = 0
    unvisitedQ.update(unvisitedQ.heap.index(source))

    while not unvisitedQ.isEmpty():
        u = unvisitedQ.extract()

        print("Visiting vertex " + u.key)
        for k, adjVertex in u.adjList.items():
            alt = u.dist + adjVertex['weight']

            print("     Considering vertex " + k)
            if alt < adjVertex['k'].dist:
                adjVertex['k'].dist = alt
                adjVertex['k'].prev = u
                print("             Updating tentative distance to " + str(alt))
                unvisitedQ.update(unvisitedQ.heap.index(adjVertex['k']))

    vertex = sink
    while vertex != source:
        path.insert(0, vertex)
        vertex = vertex.prev
    path.insert(0, source)

    return path, sink.dist

def yenKSP(graph, source, sink, K):
    #A is a list containing the shortest path A[0] to A[K -1]
    A = []
    #B is a list containing potential k'th shortest path
    B = []

    # Determine the shortest path from source to sink
    A.append(dijkstra(graph,source,sink))

    for k in range(1, K):
        # The spur node ranges from the first node to the next to last last node in the previous k-shortest path
        for i in range(len(A[k - 1][0]) - 1):

            #spur node is retrieved from the previous k-shortest path, k - 1
            spurNode = A[k-1][0][i]

            # The sequence of nodes from the source to the spur node of the previous k-shortest path
            rootPath = A[k-1][0][0:i]

            for path in A:
                if rootPath == path[0][0:i]:
                    # Remove the links that are part of the previous shortest paths which share the same root path.
                    graph.removeEdge(path[0][i],path[0][i+1])
                    del



def approxMVC(graph):

    def compareVertex(vertex1, vertex2):
        if(vertex1.current_degree == vertex2.current_degree):
            return vertex1.key < vertex2.key
        else:
            return vertex1.current_degree > vertex2.current_degree

    #Priority queue to select the heap with the highest degree
    vertexHeap = Heap("max", compareVertex)

    #Vertices that have been visted
    vistedList = []

    #Vertex Cover
    vertexCover = []

    #Set the current degree of each vertex, this is what will be used to sort
    for vertex in graph:
        vertex.current_degree = len(vertex.adjList) - 1
        vertexHeap.insert(vertex)

    while not vertexHeap.isEmpty() and vertexHeap.heap[0].current_degree > 0:
        vertex = vertexHeap.extract()
        vistedList.append(vertex)
        vertexCover.append(vertex)

        print("Visiting vertex: " + vertex.__str__() + ", Visisted = {" + ",".join([vertex.key for vertex in vistedList]) + "}")
        for k, adjVertex in vertex.adjList.items():
            if not (adjVertex['k'] in vistedList) and adjVertex['k'].current_degree != 0: #If it hasn't been
                adjVertex['k'].current_degree = adjVertex['k'].current_degree - 1
                print("     Updating degree of vertex " + k + " to " + str(adjVertex['k'].current_degree))
                vertexHeap.update(vertexHeap.heap.index(adjVertex['k']))
        print()

    print("VERTEX COVER = " + ",".join([vertex.key for vertex in vertexCover]))

    return set(vertexCover)


def main():
    #Using this main submodule as a test harness, bad idea?
    #graph = readGraph1(sys.argv[1])
    #print("Performing Minimum Vertex Cover Approximation...")
    graph = readGraph2(sys.argv[1])
    source = graph.vertexList['C']
    sink = graph.vertexList['E']
    path, cost = dijkstra(graph,source,sink)
    print("\n" + '->'.join([str(vertex.key) for vertex in path]))
    print("Cost = " + str(cost))


if __name__ == "__main__":
    main()
