# Instance of quadtree from Malcom Kesson for use in Game of Life

from quadtree import Node, QuadTree

class GoLNode(Node):
	def getinstance(self, rect):
		return GoLNode(self, rect)


	def spans_feature(self, rect):
		new_x0, new_y0, new_x1, new_y1 = rect
	

class GoLQuadTree(QuadTree):

	def add_node(self, rect):
	"""
	Use this to add a point to the Quad Tree
	Will call subdivide as necessary
	

	"""
		pass

	def del_node(self, rect):
		pass

# Need to write spans_feature to check if point we are adding exists in the rectangle.  So we need to store the points somehow.  Save them in a set like the circle example?  Or should each node save it's own point if it is a leaf?  Then we need to override subdivide (basically rewrite the class at that point).  
