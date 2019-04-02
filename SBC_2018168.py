#!/usr/bin/env python3

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
	name = "Pragyan Mehrotra"
	email = "pragyan18168@iiitd.ac.in"
	roll_num = "2018168"

	def __init__ (self, vertices, edges):
		"""
		Initializes object for the class Graph

		Args:
			vertices: List of integers specifying vertices in graph
			edges: List of 2-tuples specifying edges in graph
		"""

		self.vertices = vertices
		
		ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
		
		self.edges = ordered_edges
		
		self.validate()
		self.links = self.get_links(self.edges)
		self.pairs = []
		for i in self.vertices:
			for j in self.vertices:
				if i!=j and sorted([i,j]) not in self.pairs:
					self.pairs.append(sorted([i,j]))
		self.bet_cen = {}
		for i in self.vertices:
			f=0.0
			self.bet_cen[i] = self.betweenness_centrality(i)
			
		self.top_k_betweenness_centrality()

	def validate(self):
		"""
		Validates if Graph if valid or not

		Raises:
			Exception if:
				- Name is empty or not a string
				- Email is empty or not a string
				- Roll Number is not in correct format
				- vertices contains duplicates
				- edges contain duplicates
				- any endpoint of an edge is not in vertices
		"""

		if (not isinstance(self.name, str)) or self.name == "":
			raise Exception("Name can't be empty")

		if (not isinstance(self.email, str)) or self.email == "":
			raise Exception("Email can't be empty")

		if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
			raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

		if not all([isinstance(node, int) for node in self.vertices]):
			raise Exception("All vertices should be integers")

		elif len(self.vertices) != len(set(self.vertices)):
			duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

			raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

		edge_vertices = list(set(itertools.chain(*self.edges)))

		if not all([node in self.vertices for node in edge_vertices]):
			raise Exception("All endpoints of edges must belong in vertices")

		if len(self.edges) != len(set(self.edges)):
			duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

			raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))
#created a dictionary containing the node as the key and the list of nodes attatched to it as the values
	def get_links(self,edges):
		x = {}
		for i in edges:
			if i[0] in x:
				x[i[0]].append(i[1])
			else:
				x[i[0]] = [i[1]]
		for i in edges:
			if i[1] in x:
				x[i[1]].append(i[0])
			else:
				x[i[1]] = [i[0]]
		for i in x:
			x[i] = list(set(x[i]))
		return x
#BFS implemented here
	def min_dist(self, start_node, end_node,x,dist=0,queue=[]):
		'''
		Finds minimum distance between start_node and end_node

		Args:
			start_node: Vertex to find distance from
			end_node: Vertex to find distance to

		Returns:
			An integer denoting minimum distance between start_node
			and end_node
		'''
		if end_node in queue:
			return dist+1
		if len(queue)==0:
			if start_node in self.visited:
				return None
			else:
				self.visited.append(start_node)
				queue.extend([start_node])
		queue_prev = queue
		self.visited.extend(queue)
		queue =[]
		for i in queue_prev:
			for j in x[i]:
				if j not in self.visited:
					queue.append(j)
		return self.min_dist(start_node,end_node,x,dist+1,queue)
#finds and returns the list of all the paths with the shortest lengths 
	def all_shortest_paths(self,all_paths,dist):
		"""
		Finds all shortest paths between start_node and end_node

		Args:
			start_node: Starting node for paths
			end_node: Destination node for paths

		Returns:
			A list of paths, where each path is a list of integers.
		"""
		t=[]
		for i in range(len(all_paths)):
			t.append(len(all_paths[i]))
		k = min(t)
		a=[]
		for i in range(len(t)):
			if k==len(all_paths[i]):
				a.append(all_paths[i])
		return a
#DFS implemented here
	def all_paths(self,start_node, end_node,x, created_path=[]):
		"""
		Finds all paths from node to destination with length = dist

		Args:
			node: Node to find path from
			destination: Node to reach
			dist: Allowed distance of path
			path: path already traversed

		Returns:
			List of path, where each path is list ending on destination

			Returns None if there no paths
		"""
		if len(created_path)==0:
			created_path.append(start_node)
		if end_node in x[start_node]:
			self.all_path.append(created_path + [end_node])
			return
		for i in x[start_node]:
			if i not in created_path:
				self.all_paths(i,end_node,x,created_path+[i])

	def no_of_shortest_paths_thru_w(self,paths,w):
		no_of_shortest_paths=len(paths)
		no_of_shortest_paths_thru_w=0
		for i in range(len(paths)):
			if w in paths[i]:
				no_of_shortest_paths_thru_w += 1
		return no_of_shortest_paths_thru_w/no_of_shortest_paths

	def betweenness_centrality(self, i):
		"""
		Find betweenness centrality of the given node

		Args:
			node: Node to find betweenness centrality of.

		Returns:
			Single floating point number, denoting betweenness centrality
			of the given node
		"""
		f=0.0
		for j in self.pairs:
			if i not in j:
				self.all_path = []
				self.visited=[]
				self.dist= self.min_dist(j[0],j[1],self.links)
				self.all_paths(j[0],j[1],self.links,[])
				print (self.all_path)
				self.asp = self.all_shortest_paths(self.all_path,self.dist)
				z = self.no_of_shortest_paths_thru_w(self.asp,i)
				f += z
		return (2*f)/((len(vertices)-1)*(len(vertices)-2))
#returns the list of nodes who have the maximum betweenness centrality	
	def top_k_betweenness_centrality(self):
		"""
		Find top k nodes based on highest equal betweenness centrality.

		
		Returns:
			List of integers, denoting top k nodes based on betweenness
			centrality.
		"""
		a=[]
		k = max(list(self.bet_cen.values()))
		for i in self.bet_cen:
			if self.bet_cen[i]==k:
				a.append(i)
		print (a)
		return a	
			

		

if __name__ == "__main__":
	vertices = [1, 2, 3, 4, 5, 6]
	edges	= [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6),(3,6)]
	#vertices = [1,2,3,4,5,6]
	#edges = [(1,2),(1,5),(2,3),(2,4),(3,6),(3,4),(5,6)]
	graph = Graph(vertices, edges)
