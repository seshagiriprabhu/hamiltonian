#!/usr/bin/env python2
# https://gist.github.com/turbofart/3428880

import math
import random

graphs = {'1': ['2', '4','5'],
        '2': ['1', '3','5'],
        '3': ['2','5','6'],
        '4': ['1','7','5'],
        '5': ['1','2','3', '4','6','7','8','9'],
        '6': ['3','5','9'],
        '7': ['4','5','8'],
        '8': ['7','5','9'],
        '9': ['8','5','6']}

graph = {'1': ['2'],
        '2': ['3', '4','5'],
        '3': ['2','4','6'],
        '4': ['2','3','4', '5'],
        '5': ['2','4','6', '7'],
        '6': ['3','4','5'],
        '7': ['5']}


class PathManager:
    pathNodes = []

    def addNodes(self, node):
        self.pathNodes.append(node)

    def getNode(self, index):
        self.pathNodes(index)

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
            for i in range(0, self.pathManager.numberOfNodes):
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


    def generateIndividual(self):
        for nodeIndex in range(0, self.pathManager.numberOfNodes()):
            self.setNode(nodeIndex, self.nodeManager.getNode(nodeIndex))
        random.shuffle(self.path)


