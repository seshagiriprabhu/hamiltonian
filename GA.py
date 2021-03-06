#!/usr/bin/env python2

import math
import random

nohc1 = {1: [2,3],
        2: [1,3],
        3: [1, 2, 4, 5],
        4: [3, 6],
        5: [3, 6],
        6: [4, 5, 7, 8],
        7: [6, 8],
        8: [6, 7]}

nohc2 = {1: [2],
        2: [3, 4,5],
        3: [2,4,6],
        4: [2,3,4, 5],
        5: [2,4,6, 7],
        6: [3,4,5],
        7: [5]}

graph = {1: [2, 3, 4, 9],
        2: [3, 7, 8, 9],
        3: [1, 2, 5, 6, 7],
        4: [1, 5, 9, 10],
        5: [1, 3, 4, 6, 12],
        6: [3, 5, 7, 11, 12],
        7: [2, 3, 8, 11],
        8: [2, 7, 9, 10, 11],
        9: [1, 2, 4, 10],
        10: [4, 8, 9, 11, 12],
        11: [7, 8, 6, 10, 12],
        12: [4, 5, 6, 10, 11]}

graph0 = {1: [2, 4,5],
        2: [1, 3,5],
        3: [2,5,6],
        4: [1,7,5],
        5: [1,2,3, 4, 6, 7, 8, 9],
        6: [3,5,9],
        7: [4,5,8],
        8: [7,5,9],
        9: [8,5,6]}

graph1 = {1: [3, 5],
        2: [4, 5],
        3: [1, 4],
        4: [2, 3],
        5: [1, 2]}

graph2 = {1: [2, 5, 6],
        2: [1, 3, 4, 5],
        3: [2, 4, 5],
        4: [2, 3, 5],
        5: [1, 2, 3, 4],
        6: [1, 4]}

class Node:
    def __init__(self, index=None, adj=[]):
        self.index = index
        self.adj = adj
    
    def getIndex(self):
        return self.index
    
    def getAdjacent(self):
        return self.adj
    
    def ifAdjacentTo(self, node):
        if node.index in self.adj:
            return True
        return False


class PathManager:
    pathNodes = []

    def addNode(self, node):
        self.pathNodes.append(node)

    def getNode(self, index):
        return self.pathNodes[index]

    def numberOfNodes(self):
        return len(self.pathNodes)


class WalkOver:
    def __init__(self, pathManager, path=None):
        self.pathManager = pathManager
        self.path = []
        self.fitness = 0.0

        if path is not None:
            self.path = path
        else:
            for i in range(0, self.pathManager.numberOfNodes()):
                self.path.append(None)

    def __len__(self):
        return len(self.path)

    def __getitem__(self, index):
        return self.path[index]

    def __setitem__(self, key, value):
        self.path[key] = value

    def __repr__(self):
        geneString = "|"
        for i in range(0, self.pathSize()):
            geneString += str(self.getNode(i)) +"|"
        return geneString

    def getNode(self, nodePosition):
        return self.path[nodePosition]

    def setNode(self, nodePosition, node):
        self.path[nodePosition] = node
        self.fitness = 0.0

    def pathSize(self):
        return len(self.path)

    def containsNode(self, node):
        return node in self.path

    def generateIndividual(self):
        for nodeIndex in range(0, self.pathManager.numberOfNodes()):
            self.setNode(nodeIndex, self.pathManager.getNode(nodeIndex))
        random.shuffle(self.path)
    
    def getFitness(self):
        if self.fitness == 0.0:
            self.fitness = float(self.calculateFitness())/40
        return self.fitness
    
    def checkLastElementCycle(self):
        """
        Check if the last node in the path and the first node in the path has
        connection
        """
        last = self.getNode(len(self.path)-1)
        first = self.getNode(0).getIndex()
        if first in last.getAdjacent():
            return True
        else: return False
    
    def checkConnection(self):
        """
        Check if all the nodes in the path are connected
        """
        for i in range(self.pathSize()):
            if i + 1 < self.pathSize():
                if not self.path[i+1].getIndex() in self.path[i].getAdjacent():
                    return False
        return True

    def checkAllUnique(self):
        seen = set()
        return not any(i in seen or seen.add(i) for i in self.path)
    
    def getPath(self):
        return self.path

    def calculateFitness(self):
        score = 0
        if self.pathSize() == pathManager.numberOfNodes():
            score = score + 10
        #    print 'a',
        if self.checkAllUnique():
            score = score + 10
        #    print 'b',
        if self.checkLastElementCycle():
            score = score + 10
        #    print 'c',
        if self.checkConnection():
            score = score + 10
        #    print 'd',
        #print
        return score


class Population:
    def __init__(self, pathManager, populationSize, initalize):
        self.paths = []

        for i in range (0, populationSize):
            self.paths.append(None)

        if initalize:
            for i in range(0, populationSize):
                newPath = WalkOver(pathManager)
                newPath.generateIndividual()
                self.savePath(i, newPath)

    def __setitem__(self, key, value):
        self.paths[key] = value

    def __getitem__(self, index):
        return self.paths[index]
    
    def savePath(self, index, path):
        self.paths[index] = path

    def getPath(self, index):
        return self.paths[index]

    def populationSize(self):
        return len(self.paths)

    def getFittest(self):
        fittest = self.paths[0]
        for i in range(0, self.populationSize()):
            if fittest.getFitness() <= self.getPath(i).getFitness():
                fittest = self.getPath(i)
        return fittest


class GA:
    def __init__(self, pathManager):
        self.pathManager = pathManager
        self.mutationRate = 0.015
        self.tournamentSize = 5
        self.elitism = True

    def evolvePopulation(self, pop):
        newPopulation = Population(self.pathManager, pop.populationSize(), False)
        elitismOffset = 0
        if self.elitism:
            newPopulation.savePath(0, pop.getFittest())
            elitismOffset = 1

        for i in range(elitismOffset, newPopulation.populationSize()):
            parent1 = self.tournamentSelection(pop)
            parent2 = self.tournamentSelection(pop)
            child = self.crossover(parent1, parent2)
            newPopulation.savePath(i, child)

        for i in range(elitismOffset, newPopulation.populationSize()):
            self.mutate(newPopulation.getPath(i))

        return newPopulation

    def crossover(self, parent1, parent2):
        child = WalkOver(self.pathManager)
        
        startPos = int(random.random() * parent1.pathSize())
        endPos = int(random.random() * parent2.pathSize())
    
        for i in range(0, child.pathSize()):
            if startPos < endPos and i > startPos and i < endPos:
                child.setNode(i, parent1.getNode(i))
            elif startPos > endPos:
                if not (i < startPos and i > endPos):
                    child.setNode(i, parent1.getNode(i))

        for i in range(0, parent2.pathSize()):
            if not child.containsNode(parent2.getNode(i)):
                for j in range(0, child.pathSize()):
                    if child.getNode(j) == None:
                        child.setNode(j, parent2.getNode(i))
                        break

        return child

    def mutate(self, path):
        for pathPos1 in range(0, path.pathSize()):
            if random.random() < self.mutationRate:
                pathPos2 = int(random.random() * path.pathSize())

                node1 = path.getNode(pathPos1)
                node2 = path.getNode(pathPos2)
                
                path.setNode(pathPos2, node1)
                path.setNode(pathPos1, node2)

    def tournamentSelection(self, pop):
        tournament = Population(self.pathManager, self.tournamentSize, False)
        for i in range(0, self.tournamentSize):
            randomId = int(random.random() * pop.populationSize())
            tournament.savePath(i, pop.getPath(randomId))
        fittest = tournament.getFittest()
        return fittest

if __name__=="__main__":
    
    pathManager = PathManager()
    G = graph1
    # Create and add nodes to the pathManager
    for key,values in G.items():
        node = Node(key, values)
        pathManager.addNode(node)

    # Initialize population
    print 'Graph:', G
    pop = Population(pathManager, 10, True)
    print "Intial Fitness score: " + str(pop.getFittest().getFitness())

    # Evolve population for 100 generations
    ga = GA(pathManager)
    pop = ga.evolvePopulation(pop)
    
    for i in range(0, 100):
        pop = ga.evolvePopulation(pop)

    fittest = pop.getFittest()
    if fittest.getFitness() == 1.0:
        print "Final Fitness score: " + str(pop.getFittest().getFitness())
        print "HC:",
        for node in fittest:
            print str(node.getIndex()) + '->',
        print fittest[0].getIndex()
    else: 
        print "No Hamiltonian cycle in this graph"

