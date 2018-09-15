# bfs_kbacon.py
"""Volume 2A: Breadth-First Search (Kevin Bacon).
<Tyler>
<Blue>
<10/13/16>
"""
import networkx as nx
from collections import defaultdict


class Graph(object):
    """A graph object, stored as an adjacency dictionary. Each node in the
    graph is a key in the dictionary. The value of each key is a list of the
    corresponding node's neighbors.

    Attributes:
        dictionary: the adjacency list of the graph.
    """

    def __init__(self, adjacency):
        """Store the adjacency dictionary as a class attribute."""
        self.dictionary = adjacency

    def __str__(self):
        """String representation: a sorted view of the adjacency dictionary.

        Example:
            >>> test = {'A':['B'], 'B':['A', 'C',], 'C':['B']}
            >>> print(Graph(test))
            A: B
            B: A; C
            C: B
        """
        my_string = ""
        mykeys = sorted(self.dictionary.keys())
        for i in mykeys:
            my_string += str(i) + ": "
            my_string += "; ".join(sorted(self.dictionary[i]))
            my_string += "\n"
        return my_string

    def traverse(self, start):
        """Begin at 'start' and perform a breadth-first search until all
        nodes in the graph have been visited. Return a list of values,
        in the order that they were visited.

        Inputs:
            start: the node to start the search at.

        Returns:
            the list of visited nodes (in order of visitation).

        Raises:
            ValueError: if 'start' is not in the adjacency dictionary.

        Example:
            >>> test = {'A':['B'], 'B':['A', 'C',], 'C':['B']}
            >>> Graph(test).traverse('B')
            ['B', 'A', 'C']
        """
        if start not in self.dictionary:
            raise ValueError("Start node not in dictionary.")
        que = [start]
        visited = set([start])
        order = []

        while len(que)>0:
            for i in self.dictionary[que[0]]:
                if i not in visited:
                    if i not in que:
                        que.append(i)
            n = que.pop(0)
            visited.add(n)
            order.append(n)

        return order

    def DFS(self, start):
        """Begin at 'start' and perform a depth-first search until all
        nodes in the graph have been visited. Return a list of values,
        in the order that they were visited. If 'start' is not in the
        adjacency dictionary, raise a ValueError.

        Inputs:
            start: the node to start the search at.

        Returns:
            the list of visited nodes (in order of visitation)
        """
        if start not in self.dictionary:
            raise ValueError("Start node not in dictionary.")
        q = [start]
        visited = set([start])
        order = []
        while len(q)>0:
            n = q.pop()
            visited.add(n)
            order.append(n)
            for i in self.dictionary[n]:
                if i not in visited:
                    if i not in q:
                        q.append(i)
        return order

    def shortest_path(self, start, target):
        """Begin at the node containing 'start' and perform a breadth-first
        search until the node containing 'target' is found. Return a list
        containg the shortest path from 'start' to 'target'. If either of
        the inputs are not in the adjacency graph, raise a ValueError.

        Inputs:
            start: the node to start the search at.
            target: the node to search for.

        Returns:
            A list of nodes along the shortest path from start to target,
                including the endpoints.

        Example:
            >>> test = {'A':['B', 'F'], 'B':['A', 'C'], 'C':['B', 'D'],
            ...         'D':['C', 'E'], 'E':['D', 'F'], 'F':['A', 'E', 'G'],
            ...         'G':['A', 'F']}
            >>> Graph(test).shortest_path('A', 'G')
            ['A', 'F', 'G']
        """
        if start not in self.dictionary:
            raise ValueError("Start node not in graph.")
        elif target not in self.dictionary:
            raise ValueError("Target node not in graph.")

        path = {}
        q = [start]

        #dictionary is the graph edges
        #q is the list of nodes to visit soon
        while len(q)>0:
            path.update({q[0]:[]})
            for i in self.dictionary[q[0]]:
                if i == target:
                    path[q[0]].append(i)
                    break
                if i not in path:
                    if i not in q:
                        q.append(i)
                    path[q[0]].append(i)
            n = q.pop(0)

        prev = target
        short = [target]
        while prev != start:
            connected = False
            for i in path:
                if prev in path[i]:
                    prev = i
                    short.append(i)
                    connected = True
                    break
            if not connected:
                raise Exception("No connecting path exists!")

        short.reverse()
        return short

    def has_node(self, node):
        return node in self.dictionary


def convert_to_networkx(dictionary):
    """Convert 'dictionary' to a networkX object and return it."""
    nx_graph = nx.Graph()

    for i in dictionary:
        for j in dictionary[i]:
            nx_graph.add_edge(i, j)
    return nx_graph


def parse(filename="movieData.txt"):
    """Generate an adjacency dictionary where each key is
    a movie and each value is a list of actors in the movie.
    """

    # open the file, read it in, and split the text by '\n'
    with open(filename, 'r', encoding='ISO-8859-1') as movieFile:
        moviesList = movieFile.read().split('\n')
    graph = defaultdict(list)

    # for each movie in the file,
    for movie in moviesList:
        # get movie name and list of actors
        names = movie.split('/')
        title = names[0]
        #graph[title] = []
        # add the actors to the dictionary
        for actor in names[1:]:
            graph[title].append(actor)
            graph[actor].append(title)

    return graph


class BaconSolver(object):
    """Class for solving the Kevin Bacon problem."""

    # Problem 6
    def __init__(self, filename="movieData.txt", fast=False):
        """Initialize the networkX graph and with data from the specified
        file. Store the graph as a class attribute. Also store the collection
        of actors in the file as an attribute.

        My implementation is highly inefficient. Setting fast=True will use networkx.
        """
        dct = parse(filename)

        #create a set for actors names contained in our graph
        self.actors = set()
        for i in dct:
            for j in dct[i]:
                self.actors.add(j)
        self.fast = fast
        if self.fast:
            self.g = convert_to_networkx(dct)
        else:
            self.g = Graph(dct)

    def path_to_bacon(self, start, target="Bacon, Kevin"):
        """Find the shortest path from 'start' to 'target'."""
        if self.g.has_node(start) and self.g.has_node(target):
            if self.fast:
                return nx.shortest_path(self.g, start, target)
            else:
                return self.g.shortest_path(start, target)
        else:
            raise ValueError("Actor name not found!")

    def bacon_number(self, start, target="Bacon, Kevin"):
        """Return the Bacon number of 'start'."""
        path  = self.path_to_bacon(start, target)
        return len(path[::2])-1 # ignore the films and the Kevin Bacon vertex

    def actor_search(self, query):
        """Help find the exact name of an actor"""
        results = [None]
        query = query.lower()
        for actor in self.actors:
            if query in actor.lower():
                results.append(actor)
        if len(results) > 21:
            print("Print first 20 results.")
        for i,name in enumerate(results[1:20+1]):
            print("{: >2}.\t".format(i+1),name)
        return results

    def average_bacon(self, target="Bacon, Kevin"):
        """Calculate the average Bacon number in the data set.
        Note that actors are not guaranteed to be connected to the target.

        Inputs:
            target (str): the node to search the graph for
        """
        total_bacon = 0
        actor_cnt = 0
        unconnected_cnt = 0
        max_num = 0
        names = []
        names_dct = {}
        for i in self.actors:
            try:
                num = self.bacon_number(i)
                names_dct[num] = i
                if num == max_num:
                    names.append(i)
                elif num > max_num:
                    max_num = num
                    names = [i]
                total_bacon += num
                actor_cnt +=1
            except:
                unconnected_cnt+=1
        print(names_dct)

        return float(total_bacon)/actor_cnt

# =========================== END OF FILE =============================== #
