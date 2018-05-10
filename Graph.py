from Heap import Heap
import GraphReader
import math
import sys

class GraphVertex:
    """A class for a vertex of an undirected simple graph"""

    def __init__(self, key):
        self.key = key; #Key is the name given to the vertex
        self.adjList = {} #Adjacency list of the vertex
        self.adjList[key] = {'k':self, 'weight':0, 'availability':True}
        self.availability = True

    def add_adjacent(self, vertex, weight=0, availability=True):
        if type(vertex) is GraphVertex:
            if vertex.key in self.adjList:
                print("ERROR! " +  vertex.key + " already exist in adj-list of " +
                       self.key + ". It was not added")
            else:
                self.adjList[vertex.key] = {'k': vertex, 'weight': weight, 'availability': availability}

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

    for vertex in graph:
        if vertex.availability == True:
            vertex.dist = math.inf
            vertex.prev = None
            unvisitedQ.insert(vertex)

    source.dist = 0
    unvisitedQ.update(unvisitedQ.heap.index(source))

    while not unvisitedQ.isEmpty():
        u = unvisitedQ.extract()

        for k, adjVertex in u.adjList.items():
            if adjVertex['availability'] == True and adjVertex['k'].availability == True:
                alt = u.dist + adjVertex['weight']
            else:
                alt = math.inf

            if alt < adjVertex['k'].dist:
                adjVertex['k'].dist = alt
                adjVertex['k'].prev = u
                unvisitedQ.update(unvisitedQ.heap.index(adjVertex['k']))

    if sink.prev != None:
        vertex = sink
        while vertex != source:
            path.insert(0, vertex)
            vertex = vertex.prev
        path.insert(0, source)
    else:
        path = None

    return path

def calcPathCost(path):
    if path == None:
        return math.inf
    else:
        cost = 0
        for i in range(len(path) - 1):
            try:
                cost = cost + path[i].adjList[path[i+1].key]['weight']
            except KeyError:
                return math.inf

    return cost

def yenKSP(graph, source, sink, K):

    #A is a list containing the shortest path A[0] to A[K -1]
    A = []
    #B is a list containing potential k'th shortest path
    B = Heap("min", lambda x,y: calcPathCost(x) > calcPathCost(y))

    # Determine the shortest path from source to sink
    A.append(dijkstra(graph,source,sink))
    print("k: 0")
    print("     Shortest path: " + '->'.join([node.key for node in A[0]]) + ", cost = " + str(calcPathCost(A[0])))

    for k in range(1, K):
        print("k: " + str(k))
        # The spur node ranges from the first node to the next to last last node in the previous k-shortest path
        for i in range(len(A[k - 1]) - 1):

            #spur node is retrieved from the previous k-shortest path, k - 1
            spurNode = A[k-1][i]

            print("     Heap: " + ','.join([str(calcPathCost(path)) for path in B.heap]))
            print("     Spur Node: " + spurNode.key)

            # The sequence of nodes from the source to the spur node of the previous k-shortest path
            rootPath = A[k-1][0:i+1]
            print("     Root path: " + '->'.join([node.key for node in rootPath]) + ", cost = " + str(calcPathCost(rootPath)))

            for path in A:
                if rootPath == path[0:i+1]:
                    # Remove the links that are part of the previous shortest paths which share the same root path.
                    if path[i].adjList[path[i+1].key]['availability'] == True:
                        path[i].adjList[path[i+1].key]['availability'] = False
                        print("         Removing edge: " + path[i].key + "->" + path[i].adjList[path[i+1].key]['k'].key)

            for rootPathNode in rootPath: #remove each node in the rootpath excep spur node
                if rootPathNode != spurNode:
                    rootPathNode.availability = False

            #Calculate the spur path from the spur node to the sink
            spurPath = dijkstra(graph, spurNode, sink)
            if(spurPath != None):
                spurPath = spurPath[1:]
                print("     Spur path: " + '->'.join([node.key for node in spurPath]) + ", cost = " + str(calcPathCost(spurPath)))
                totalPath = rootPath + spurPath
                print("     Total path: " + '->'.join([node.key for node in totalPath]) + ", cost = " + str(calcPathCost(totalPath)))
                if not totalPath in B.heap:
                    print("     Inserting Total Path to heap")
                    B.insert(totalPath)
                    print("     Heap: " + ','.join([str(calcPathCost(path)) for path in B.heap]))
                else:
                    print("     Path already exists")
            else:
                print("     No Spur path found")

            print()
            #Resstore edge and nodes that were remove from the graph
            for vertex in graph:
                vertex.availability = True
                for key, adjVertex in vertex.adjList.items():
                    adjVertex['availability'] = True

        if len(B.heap) == 0:
        # This handles the case of there being no spur paths, or no spur paths left.
        # This could happen if the spur paths have already been exhausted (added to A),
        # or there are no spur paths at all - such as when both the source and sink vertices
        # line alone a "dead end"
            break

        if len(B.heap) >= K - k + 1:
            print("     Heap has more than required k path: " + str(len(B.heap)))
            for _ in range(0, K - k):
                A.append(B.extract())
            break

        A.append(B.extract())
        print("     Shortest path: " + '->'.join([node.key for node in A[k]]) + ", cost = " + str(calcPathCost(A[k])))

    return A

def main():
    #Using this main submodule as a test harness, bad idea?
    #graph = readGraph1(sys.argv[1])
    #print("Performing Minimum Vertex Cover Approximation...")
    graph = GraphReader.readGraph2(sys.argv[1])
    source = graph.vertexList['C']
    sink = graph.vertexList['E']

    A = yenKSP(graph, source, sink,40) #Find 3 shortest path from C to E
    for i, path in enumerate(A):
        cost = calcPathCost(path)
        if path != None:
            print("\n" + str(i+1) + ". " + '->'.join([str(vertex.key) for vertex in path]))
        print("Cost = " + str(cost))


if __name__ == "__main__":
    main()
