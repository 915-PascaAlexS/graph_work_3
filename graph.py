from queue import Queue

from graphError import GraphError
from random import randint, choice

class DirectedGraph:
    def __init__(self, numberOfVertices, numberOfEdges):
        self.__numberOfVertices = numberOfVertices
        self.__numberOfEdges = numberOfEdges
        self.__dictionaryIn = {}
        self.__dictionaryOut = {}
        self.__dictionaryCost = {}
        for index in range(numberOfVertices):
            self.__dictionaryIn[index] = []
            self.__dictionaryOut[index] = []

    @property
    def getNumberOfVertices(self):
        return self.__numberOfVertices

    @property
    def getNumberOfEdges(self):
        return self.__numberOfEdges

    @property
    def getDictionaryIn(self):
        return self.__dictionaryIn

    @property
    def getDictionaryOut(self):
        return self.__dictionaryOut

    @property
    def getDictionaryCost(self):
        return self.__dictionaryCost

    def checkIfTheGraphHasGivenVertex(self, givenVertex):
        if givenVertex in self.__dictionaryIn and givenVertex in self.__dictionaryOut:
            return True
        return False

    def checkIfTheGraphHasGivenEdge(self, sourceVertex, targetVertex):
        if self.checkIfTheGraphHasGivenVertex(sourceVertex) is False:
            raise GraphError("Source vertex doesn't exist in current graph!")
        if self.checkIfTheGraphHasGivenVertex(targetVertex) is False:
            raise GraphError("Target vertex doesn't exist in current graph!")

        if sourceVertex not in self.__dictionaryIn[targetVertex] and targetVertex not in self.__dictionaryOut[sourceVertex]:
            return False
        return True

    def addNewVertex(self, vertexToBeAdded):
        if self.checkIfTheGraphHasGivenVertex(vertexToBeAdded):
            raise GraphError("Vertex already exists!")
        self.__dictionaryIn[vertexToBeAdded] = []
        self.__dictionaryOut[vertexToBeAdded] = []
        self.__numberOfVertices += 1
        return True

    def addNewEdge(self, sourceVertex, targetVertex, costOfEdge):
        if self.checkIfTheGraphHasGivenVertex(sourceVertex) is False:
            raise GraphError("Source vertex doesn't exist in current graph!")
        if self.checkIfTheGraphHasGivenVertex(targetVertex) is False:
            raise GraphError("Target vertex doesn't exist in current graph!")

        if sourceVertex in self.__dictionaryIn[targetVertex] or targetVertex in self.__dictionaryOut[sourceVertex]:
            raise GraphError("The edge already exists!")
        self.__dictionaryIn[targetVertex].append(sourceVertex)
        self.__dictionaryOut[sourceVertex].append(targetVertex)
        self.__dictionaryCost[(sourceVertex, targetVertex)] = costOfEdge
        self.__numberOfEdges += 1
        return True

    def parseSetOfVertices(self):
        for vertex in self.__dictionaryIn:
            yield vertex

    def parseSetOfOutboundEdgesOfAVertex(self, givenVertex):
        if self.checkIfTheGraphHasGivenVertex(givenVertex) is False:
            raise GraphError("Given vertex doesn't exist in current graph!")
        for targetVertex in self.__dictionaryOut[givenVertex]:
            yield targetVertex

    def parseSetOfInboundEdgesOfAVertex(self, givenVertex):
        if self.checkIfTheGraphHasGivenVertex(givenVertex) is False:
            raise GraphError("Given vertex doesn't exist in current graph!")
        for sourceVertex in self.__dictionaryIn[givenVertex]:
            yield sourceVertex

    def getInDegreeOfGivenVertex(self, givenVertex):
        if self.checkIfTheGraphHasGivenVertex(givenVertex) is False:
            raise GraphError("Given vertex doesn't exist in current graph!")
        inDegree = len(self.__dictionaryIn[givenVertex])
        return inDegree

    def getOutDegreeOfGivenVertex(self, givenVertex):
        if self.checkIfTheGraphHasGivenVertex(givenVertex) is False:
            raise GraphError("Given vertex doesn't exist in current graph!")
        outDegree = len(self.__dictionaryOut[givenVertex])
        return outDegree

    def getCostOfGivenEdge(self, sourceVertex, targetVertex):
        if self.checkIfTheGraphHasGivenEdge(sourceVertex, targetVertex) is False:
            raise GraphError("Provided edge doesn't exist in current graph!")
        return self.__dictionaryCost[(sourceVertex, targetVertex)]

    def updateTheCostOfGivenEdge(self, sourceVertex, targetVertex, newCostOfTheEdge):
        if self.checkIfTheGraphHasGivenEdge(sourceVertex, targetVertex) is False:
            raise GraphError("Provided edge doesn't exist in current graph!")
        self.__dictionaryCost[(sourceVertex, targetVertex)] = newCostOfTheEdge

    def removeAnEdge(self, sourceVertex, targetVertex):
        if self.checkIfTheGraphHasGivenEdge(sourceVertex, targetVertex) is False:
            raise GraphError("Provided edge doesn't exist in current graph!")
        self.__dictionaryCost.pop((sourceVertex, targetVertex))
        self.__dictionaryIn[targetVertex].remove(sourceVertex)
        self.__dictionaryOut[sourceVertex].remove(targetVertex)
        self.__numberOfEdges -= 1


    def removeVertex(self, givenVertex):
        if self.checkIfTheGraphHasGivenVertex(givenVertex) is False:
            raise GraphError("Given vertex doesn't exist in current graph!")
        for predecessor in list(self.__dictionaryIn[givenVertex]):
            self.removeAnEdge(predecessor, givenVertex)
        for successor in list(self.__dictionaryOut[givenVertex]):
            self.removeAnEdge(givenVertex, successor)
        self.__dictionaryIn.pop(givenVertex)
        self.__dictionaryOut.pop(givenVertex)
        self.__numberOfVertices -= 1

    def bellmanFord(self, start: int, end: int):
        dist = [float('inf')] * self.__numberOfVertices
        pred = [-1] * self.__numberOfVertices
        dist[start] = 0

        queue = Queue()
        queue.put(start)
        inQueue = [False] * self.__numberOfVertices
        inQueue[start] = True

        while not queue.empty():
            u = queue.get()
            inQueue[u] = False

            for v in self.__dictionaryOut[u]:
                if dist[u] + self.__dictionaryCost[(u, v)] < dist[v]:
                    dist[v] = dist[u] + self.__dictionaryCost[(u, v)]
                    pred[v] = u

                    if not inQueue[v]:
                        queue.put(v)
                        inQueue[v] = True

            # check for negative cycles
            if queue.qsize() > self.__numberOfVertices:
                return [], []

        path = []
        current = end
        while current != start:
            path.append(current)
            current = pred[current]
        path.append(start)
        path.reverse()

        return dist, path

def readGraphFromTextFile(textFileName):
    fileToReadFrom = open(textFileName, "rt")
    allLinesFromTextFile = fileToReadFrom.readlines()
    fileToReadFrom.close()
    newGraph = DirectedGraph(0, 0)

    for index in range(len(allLinesFromTextFile)):
        line = allLinesFromTextFile[index].strip()
        line = line.split(' ')

        if index == 0:
            numberOfVertices = int(line[0])
            numberOfEdges = int(line[1])
            newGraph = DirectedGraph(numberOfVertices, numberOfEdges)

        else:
            sourceVertex = int(line[0])
            targetVertex = int(line[1])
            costOfEdge = int(line[2])
            newGraph.getDictionaryIn[targetVertex].append(sourceVertex)
            newGraph.getDictionaryOut[sourceVertex].append(targetVertex)
            newGraph.getDictionaryCost[(sourceVertex, targetVertex)] = costOfEdge
    return newGraph

def writeGraphToTextFile(textFileName, graph):
    fileToWriteIn = open(textFileName, "w")
    firstLine = str(graph.getNumberOfVertices) + ' ' + str(graph.getNumberOfEdges) + '\n'
    fileToWriteIn.write(firstLine)

    for key in graph.getDictionaryCost.keys():
        nextLine = str(key[0]) + ' ' + str(key[1]) + ' ' + str(graph.getDictionaryCost[key]) + '\n'
        fileToWriteIn.write(nextLine)

    for vertex in graph.getDictionaryIn.keys():
        if graph.getInDegreeOfGivenVertex(vertex) == 0 and graph.getOutDegreeOfGivenVertex(vertex) == 0:
            nextLine = str(vertex) + '\n'
            fileToWriteIn.write(nextLine)
    fileToWriteIn.close()

def createRandomGraph(numberOfVertices, numberOfEdges):
    randomGraph = DirectedGraph(numberOfVertices, 0)
    allPossibilitiesForSourceVertex = list(range(numberOfVertices))

    while numberOfEdges > 0:
        sourceVertex = choice(allPossibilitiesForSourceVertex)
        allPossibilitiesForSourceVertex.remove(sourceVertex)
        allPossibilitiesForTargetVertex = list(range(numberOfVertices))

        while len(allPossibilitiesForTargetVertex) > 0 and numberOfEdges > 0:
            targetVertex = choice(allPossibilitiesForTargetVertex)
            allPossibilitiesForTargetVertex.remove(targetVertex)
            costOfEdge = randint(0, 999)
            randomGraph.addNewEdge(sourceVertex, targetVertex, costOfEdge)
            numberOfEdges -= 1
    return randomGraph
