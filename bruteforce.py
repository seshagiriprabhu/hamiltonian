#!/usr/bin/env python2.7

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

graph1 = {1: [2, 3, 4, 9],
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

def brute_find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = brute_find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def brute_find_cycle(graph):
    cycles=[]
    for startnode in graph:
        for endnode in graph:
            newpaths = brute_find_all_paths(graph, startnode, endnode)
            for path in newpaths:
                if len(path)==len(graph):
                    if path[0] in graph[path[len(graph)-1]]:
                        path.append(path[0])
                        cycles.append(path)
    return cycles


if __name__=="__main__":
    cycles = brute_find_cycle(graph1)
    print "Number of Hamiltonian cycle: ", len(cycles)
    for cycle in cycles:
        for node in cycle:
            print node, "->",
        print

