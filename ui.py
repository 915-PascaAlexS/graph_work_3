from graph import DirectedGraph, readGraphFromTextFile, writeGraphToTextFile, createRandomGraph
from graphError import GraphError
from copy import deepcopy

class Ui:
    def __init__(self):
        self.__allCommands = {
            '1': self.addVertex,
            '2': self.removeVertex,
            '3': self.addEdge,
            '4': self.removeEdge,
            '5': self.getNumberOfVertices,
            '6': self.getNumberOfEdges,
            '7': self.parseTheSetOfVertices,
            '8': self.verifyIfThereIsAnEdgeBetweenTwoVertices,
            '9': self.getInDegreeOfAVertex,
            '10': self.getOutDegreeOfAVertex,
            '11': self.parseSetOfOutboundEdgesOfAVertex,
            '12': self.parseSetOfInboundEdgesOfAVertex,
            '13': self.getTheCostOfASpecifiedEdge,
            '14': self.changeTheCostOfASpecifiedEdge,
            '15': self.createRandomGraph,
            '16': self.createACopyOfTheGraph,
            '17': self.readGraphFromTextFile,
            '18': self.writeGraphToTextFile,
            '19': self.switchCurrentGraph,
            '20': self.lowestCostWalkBetweenTwoVertices,
        }
        self.__listOfGraphs = []
        self.__indexOfCurrentGraph = None


    def createRandomGraph(self):
        numberOfVertices = int(input("Enter the number of vertices: "))
        numberOfEdges = int(input("Enter the number of edges: "))
        if numberOfEdges > numberOfVertices ** 2:
            raise GraphError("Too many edges!")
        if numberOfEdges < 0 or numberOfEdges < 0:
            raise GraphError("Invalid input!")
        self.__listOfGraphs.append(createRandomGraph(numberOfVertices, numberOfEdges))
        self.__indexOfCurrentGraph = len(self.__listOfGraphs) - 1
        print("Successfully!")

    def getNumberOfVertices(self):
        numberOfVertices = self.__listOfGraphs[self.__indexOfCurrentGraph].getNumberOfVertices
        print(f"Number of vertices of the current graph is: {numberOfVertices}")

    def getNumberOfEdges(self):
        numberOfEdges = self.__listOfGraphs[self.__indexOfCurrentGraph].getNumberOfEdges
        print(f"Number of edges of the current graph is: {numberOfEdges}")

    def parseTheSetOfVertices(self):
        listOfAllVertices = []
        for vertex in self.__listOfGraphs[self.__indexOfCurrentGraph].parseSetOfVertices():
            listOfAllVertices.append(vertex)
        print(*listOfAllVertices)

    def verifyIfThereIsAnEdgeBetweenTwoVertices(self):
        sourceVertex = int(input("Enter source vertex: "))
        targetVertex = int(input("Enter target vertex: "))
        edgeFound = self.__listOfGraphs[self.__indexOfCurrentGraph].checkIfTheGraphHasGivenEdge(sourceVertex, targetVertex)
        if edgeFound:
            print(f"The edge ({sourceVertex}, {targetVertex}) exists!")
        else:
            print(f"The edge ({sourceVertex}, {targetVertex}) doesn't exist!")

    def getInDegreeOfAVertex(self):
        givenVertex = int(input("Enter a vertex: "))
        inDegree = self.__listOfGraphs[self.__indexOfCurrentGraph].getInDegreeOfGivenVertex(givenVertex)
        print(f"The in degree of vertex {givenVertex} is: {inDegree}")


    def getOutDegreeOfAVertex(self):
        givenVertex = int(input("Enter a vertex: "))
        outDegree = self.__listOfGraphs[self.__indexOfCurrentGraph].getOutDegreeOfGivenVertex(givenVertex)
        print(f"The out degree of vertex {givenVertex} is: {outDegree}")

    def parseSetOfOutboundEdgesOfAVertex(self):
        listOfAllSuccessorsOfGivenVertex = []
        givenVertex = int(input("Enter a vertex: "))
        for successor in self.__listOfGraphs[self.__indexOfCurrentGraph].parseSetOfOutboundEdgesOfAVertex(givenVertex):
            listOfAllSuccessorsOfGivenVertex.append(successor)
        print(*listOfAllSuccessorsOfGivenVertex)

    def parseSetOfInboundEdgesOfAVertex(self):
        listOfAllPredecessorsOfAGivenVertex = []
        givenVertex = int(input("Enter a vertex: "))
        for predecessor in self.__listOfGraphs[self.__indexOfCurrentGraph].parseSetOfInboundEdgesOfAVertex(givenVertex):
            listOfAllPredecessorsOfAGivenVertex.append(predecessor)
        print(*listOfAllPredecessorsOfAGivenVertex)


    def getTheCostOfASpecifiedEdge(self):
        sourceVertex = int(input("Enter the source vertex of the edge: "))
        targetVertex = int(input("Enter the target vertex of the edge: "))
        costOfEdge = self.__listOfGraphs[self.__indexOfCurrentGraph].getCostOfGivenEdge(sourceVertex, targetVertex)
        print(f"The cost of the edge ({sourceVertex},{targetVertex}) is: {costOfEdge}")

    def changeTheCostOfASpecifiedEdge(self):
        sourceVertex = int(input("Enter the source vertex of the edge: "))
        targetVertex = int(input("Enter the target vertex of the edge: "))
        newCostOfTheEdge = int(input("Enter the new cost of the edge: "))
        self.__listOfGraphs[self.__indexOfCurrentGraph].updateTheCostOfGivenEdge(sourceVertex, targetVertex, newCostOfTheEdge)
        print("Successfully!")

    def addVertex(self):
        newVertex = int(input("Enter the new vertex: "))
        self.__listOfGraphs[self.__indexOfCurrentGraph].addNewVertex(newVertex)
        print("Successfully!")

    def removeVertex(self):
        vertexToDelete = int(input("Enter the vertex: "))
        self.__listOfGraphs[self.__indexOfCurrentGraph].removeVertex(vertexToDelete)
        print("Successfully!")

    def addEdge(self):
        print("Add an edge, provide source vertex, target vertex and the cost of the edge: ")
        sourceVertex = int(input("Source vertex: "))
        targetVertex = int(input("Target vertex: "))
        costOfEdge = int(input("Cost of edge: "))
        self.__listOfGraphs[self.__indexOfCurrentGraph].addNewEdge(sourceVertex, targetVertex, costOfEdge)
        print("Successfully!")

    def removeEdge(self):
        sourceVertex = int(input("Source vertex: "))
        targetVertex = int(input("Target vertex: "))
        self.__listOfGraphs[self.__indexOfCurrentGraph].removeAnEdge(sourceVertex, targetVertex)
        print("Successfully!")

    def createACopyOfTheGraph(self):
        copyOfTheGraph = deepcopy(self.__listOfGraphs[self.__indexOfCurrentGraph])
        self.__listOfGraphs.append(copyOfTheGraph)
        self.__indexOfCurrentGraph = len(self.__listOfGraphs) - 1
        print("Successfully!")

    def readGraphFromTextFile(self):
        textFileName = input("Enter a valid file name to read from: ")
        self.__listOfGraphs.append(readGraphFromTextFile(textFileName))
        self.__indexOfCurrentGraph = len(self.__listOfGraphs) - 1
        print("Successfully!")

    def writeGraphToTextFile(self):
        textFileName = input("Enter a file name: ")
        writeGraphToTextFile(textFileName, self.__listOfGraphs[self.__indexOfCurrentGraph])
        print("Successfully!")

    def createAnEmptyGraph(self):
        emptyGraph = DirectedGraph(0, 0)
        self.__listOfGraphs.append(emptyGraph)
        self.__indexOfCurrentGraph = len(self.__listOfGraphs) - 1

    def switchCurrentGraph(self):
        print(f"You can choose a graph from existing graphs(0 - {len(self.__listOfGraphs) - 1}), index of current graph is: {self.__indexOfCurrentGraph}")
        newIndex = int(input("New index: "))
        if newIndex >= len(self.__listOfGraphs) or newIndex < 0:
            raise ValueError("Invalid index!")
        self.__indexOfCurrentGraph = newIndex
        print("Successfully!")

    def lowestCostWalkBetweenTwoVertices(self):
        sourceVertex = int(input("Source vertex: "))
        targetVertex = int(input("Target vertex: "))

        lowestCostWalk = self.__listOfGraphs[self.__indexOfCurrentGraph].lowestCostWalk(sourceVertex, targetVertex)
        if lowestCostWalk == float("inf"):
            print("There is no path between the two vertices!")
        else:
            print(f"The lowest cost walk between the two vertices is: {lowestCostWalk}")
        print("Successfully!")


    @staticmethod
    def displayMenu():
        print("Menu:")
        print("\t1. Add a vertex.")
        print("\t2. Remove a vertex.")
        print("\t3. Add an edge.")
        print("\t4. Remove an edge.")
        print("\t5. Get the number of vertices.")
        print("\t6. Get the number of edges.")
        print("\t7. Parse the set of vertices.")
        print("\t8. Verify if there is an edge between two vertices.")
        print("\t9. Get the in degree of a vertex.")
        print("\t10. Get the out degree of a vertex.")
        print("\t11. Parse the set of outbound edges of a vertex.")
        print("\t12. Parse the set of inbound edges of a vertex.")
        print("\t13. Get the cost of a specified edge.")
        print("\t14. Change the cost of a specified edge.")
        print("\t15. Create a random graph with specified number of vertices and of edges.")
        print("\t16. Make a copy of the graph.")
        print("\t17. Read a graph from a text file.")
        print("\t18. Write the graph in a text file.")
        print("\t19. Switch between existing graphs.")
        print("\t20. Lowest cost walk between two vertices.")
        print("\t0. Exit.")


    def start(self):
        self.createAnEmptyGraph()
        while True:
            self.displayMenu()
            userOption = input("Enter an option: ")
            if userOption == '0':
                break
            elif userOption in self.__allCommands:
                try:
                    self.__allCommands[userOption]()
                except ValueError as errorMessage:
                    print("--- try again --- " + str(errorMessage))
                except IOError as errorMessage:
                    print("--- try again --- " + str(errorMessage))
                except GraphError as errorMessage:
                    print("--- try again --- " + str(errorMessage))
                except IndexError as errorMessage:
                    print("--- try again --- " + str(errorMessage))
            else:
                print("Invalid command!")