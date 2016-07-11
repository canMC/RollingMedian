import sys
import re
import os
import skiplist

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
    
    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])
    
    #adds a connection from this vertex to another
    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight
    
    def remove_neighbor(self, neighbor):
        try:
            del self.adjacent[neighbor]
        except:
            pass

    #returns all of the vertices in the adjacency list
    def get_connections(self):
        return self.adjacent.keys()

    def get_degree(self):
        return len(self.adjacent)
    
    def get_id(self):
        return self.id
    
    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0
        self.currentMedian = 0
        self.sl = skiplist.IndexableSkiplist(100)
    
    def __iter__(self):
        return iter(self.vert_dict.values())
    
    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex
    
    def remove_vertex(self, node):
        self.num_vertices = self.num_vertices - 1
        try:
            del self.vert_dict[node]
        except:
            pass

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        #update skiplist when connections are added
        if self.vert_dict[frm] not in self.vert_dict[to].get_connections():
            self.currentMedian = 0
            frm_degree = self.vert_dict[frm].get_degree()
            to_degree = self.vert_dict[to].get_degree()
            if (frm_degree) !=0:
                self.sl.remove(frm_degree)
            if (to_degree) !=0:
                self.sl.remove(to_degree)
            self.sl.insert(frm_degree+1)
            self.sl.insert(to_degree+1)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def remove_edge(self, frm, to):

        if frm in self.vert_dict and to in self.vert_dict:
            #update skiplist when connections are removed
            if self.vert_dict[frm] in self.vert_dict[to].get_connections():
                self.sl.remove(self.vert_dict[to].get_degree())
                self.sl.remove(self.vert_dict[frm].get_degree())
                self.vert_dict[frm].remove_neighbor(self.vert_dict[to])
                self.vert_dict[to].remove_neighbor(self.vert_dict[frm])
                self.currentMedian = 0
    
            if self.vert_dict[frm].get_degree() == 0:
                self.remove_vertex(frm)
            else:
                self.sl.insert(self.vert_dict[frm].get_degree())
    
            if self.vert_dict[to].get_degree() == 0:
                self.remove_vertex(to)
            else:
                self.sl.insert(self.vert_dict[to].get_degree())

    #returns the names of all of the vertices in the graph
    def get_vertices(self):
        return self.vert_dict.keys()

    def get_vertices_sorted(self):
        return sorted(self.vert_dict.keys())

    def computeMedianDegree(self):
        #graph was updated, need to recompute median
        if self.currentMedian ==0:
            middleIndex = len(self.sl)//2
            if (len(self.sl)%2 == 1):
                self.currentMedian = self.sl[middleIndex];
            else:
                self.currentMedian = (self.sl[middleIndex-1] + self.sl[middleIndex]) / 2.0;

        return self.currentMedian
