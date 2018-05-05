from Heap import Heap

class GraphVertex:
    """A class for a vertex of an undirected simple graph"""

    def __init__(self, key):
        self.key = key; #Key is the name given to the vertex
        self.adjList = {} #Adjacency list of the vertex
        self.adjList[key] = self

    def add_adjacent(self, vertex):
        if type(vertex) is GraphVertex:
            if vertex.key in self.adjList:
                print("ERROR! " +  vertex.key + " already exist in adj-list of " +
                       self.key + ". It was not added")
            else:
                self.adjList[vertex.key] = vertex
        else:
            raise TypeError

    #Operator Overloading
    def __str__(self):
        return self.key + "|" + "-".join(self.adjList.keys())


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

def readGraph(path):
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

def main():
    #Using this main submodule as a test harness, bad idea?
    graph = readGraph("Graph4.txt")
    print(graph)
    print("Performing Minimum Vertex Cover Approximation...")
    seenVertex = 1

    #Priority queue to select the heap with the highest degree
    vertexHeap = Heap("max", lambda x: x.current_degree)

    #Vertices that have been visted
    vistedList = []

    #Vertex Cover
    vertexCover = []

    #Set the current degree of each vertex, this is what will be used to sort
    for vertex in graph:
        vertex.current_degree = len(vertex.adjList) - 1
        vertexHeap.insert(vertex)

    while not vertexHeap.isEmpty() and seenVertex > 0:
        print("Current heap = " + vertexHeap.__str__())
        vertex = vertexHeap.extract()
        vistedList.append(vertex)

        seenVertex = vertex.current_degree
        if (vertex.current_degree > 0):
            vertexCover.append(vertex)

        print("Visiting vertex: " + vertex.key + ", Visisted = {" + ",".join([vertex.key for vertex in vistedList]) + "}")
        for k, adjVertex in vertex.adjList.items():
            if not (adjVertex in vistedList) and adjVertex.current_degree != 0: #If it hasn't been
                adjVertex.current_degree = adjVertex.current_degree - 1
                print("     Updating degree of adjacent vertex: " + k + " to " + str(adjVertex.current_degree))
                vertexHeap.update(vertexHeap.heap.index(adjVertex))

        print()

    print("VERTEX COVER = " + ",".join([vertex.key for vertex in vertexCover]))


if __name__ == "__main__":
    main()
