# Instance of quadtree from Malcom Kesson for use in Game of Life
# This code is a copy of his code from http://www.fundza.com/algorithmic/quadtree/index.html
# Instead of using inheritance, I just modified what I needed.
# I had to override every function to make it match my needs.

import matplotlib.pyplot as plt

class GoLNode():
	ROOT = 0
	BRANCH = 1
	LEAF = 2
	EMPTY = 3

	def __init__(self, parent, rect):
		"""
		Initializes an instance of a Quadtree Node

		Parameters
		----------
		Parent is the parent Node
		rect is the bounding rectangle	
		"""
		self.parent = parent
		self.children = [None, None, None, None]

		self.rect = rect
		x0, y0, x1, y1 = rect

		# Determine node type
		if parent == None:
			self.depth = 0
			self.type = GoLNode.ROOT
		else:
			self.depth = parent.depth + 1
			# Leaf iff 1 space wide
			if(x1 - x0) == 0:
				self.type = GoLNode.LEAF
			else:
				self.type = GoLNode.BRANCH


	def getinstance(self, rect):
		"""
		Returns an instance of a GoL Node
		
		Parameters
		----------
		rect is the bounding rectangle for the Node to be created
		"""

		return GoLNode(self, rect)


	def spans_feature(self, rect, point = None):
		"""
		This very simply checks if the point in question is within a rectangle

		Parameters
		----------
		rect is the bounding rectangle
		point is the point within the rectangle

		Returns
		-------
		True if point is in rect, false otherwise
		"""

		if point == None:
			return False

		x,y = point
		x0, y0, x1, y1 = rect
	
		if x >= x0 and x <= x1 and y >= y0 and y <= y1:
			return True

		return False

	def subdivide(self, point = None):
		"""
		This is a modification of the subdivide function in the base class
		It requires a point to subdivide to assist with insertion

		Paramters
		---------
		Point to subdivide on and check against

		Returns
		-------
		None
		"""
		
		if self.type == GoLNode.LEAF:
			return
		
		x,y = point

		x0, y0, x1, y1 = self.rect
		h = (x1 - x0) / 2
		rects = []
		rects.append((x0, y0, x0 + h, y0 + h))
		rects.append((x0, y0 + h + 1, x0 + h, y1))
		rects.append((x0 + h + 1, y0 + h + 1, x1, y1))	
		rects.append((x0 + h + 1, y0, x1, y0 + h))
		#print rects

		for n in range(len(rects)):
			if self.spans_feature(rects[n], point):
				#if x == x0 and x == x1 and y == y0 and y == y1:
				#print "Creating child for ", point, "at depth ", self.depth, " and child ", n, rects[n]
				self.children[n] = self.getinstance(rects[n])
				self.children[n].subdivide(point)

	def contains(self, x, y):
		"""
		Determines if the given coordinates are contained within the Node's bounding rectangle

		Parameters
		----------
		x and y are the coordinates of the input point
		
		Returns
		-------
		True if contained, false otherwise
		"""
		x0, y0, x1, y1 = self.rect
		if x >= x0 and x <= x1 and y >= y0 and y <= y1:
			return True

		return False

	def return_point(self):
		"""
		Returns the point pointed to by node IFF it is a Leaf Node

		Parameters
		----------
		None

		Returns
		-------
		Returns (x,y) tuple to indicate which point is represented.
		Returns None when node is not a Leaf node.
		"""
		
		if self.type != GoLNode.LEAF:
			return None

		return (self.rect[0], self.rect[1])
		

class GoLQuadTree():
	maxdepth = 1
	leaves = set()
	allnodes = []
	
	def __init__(self, rootnode, minrect):
		"""
		Initializes the Quad tree

		Parameters
		----------
		Rootnode is the root of the tree, needs to be (2^n)-1 and square
		Minrect is leftover from Malcom's Implementation
		
		Returns
		-------
		None
		"""
		GoLNode.minsize = minrect
		GoLQuadTree.leaves.clear()
		GoLQuadTree.allnodes = []

	def traverse(self, node):
		"""
		This traverses the tree and puts ALL nodes into one list
		and puts the leaves into a seperate list as well.  The max
		depth is recorded during the recursion.

		Parameters
		----------
		node is the current node being examined

		Returns
		-------
		None
		"""

		# If beginning of recursion (root node), then clear out all data
		# structures and reset depth.
		if node.depth == 0:
			GoLQuadTree.allnodes = []
			GoLQuadTree.leaves = set()
			GoLQuadTree.maxdepth = 1

		# Add the current node to all nodes
		GoLQuadTree.allnodes.append(node)
		# And save leaves into leaves
                if node.type == GoLNode.LEAF:
                        GoLQuadTree.leaves.add(node.return_point())
                        if node.depth > GoLQuadTree.maxdepth:
                                GoLQuadTree.maxdepth = node.depth

		# Recurse on non-empty children
                for child in node.children:
                        if child != None:
                                self.traverse(child)

	def prune(self, node):
		"""
		Prune determines if a node has children with leaves and cuts
		off any branches that have no leaves.

		Parameters
		----------
		node is the node to check for missing leaves

		Returns
		-------
		None
		"""
                if node.type == GoLNode.LEAF:
                        return 1
                leafcount = 0
                removals = []
                for child in node.children:
                        if child != None:
                                leafcount += self.prune(child)
                                if leafcount == 0:
                                        removals.append(child)
                for item in removals:
                        n = node.children.index(item)
                        node.children[n] = None
                return leafcount
	

	def insert(self, root, point):
		"""
		Use this to add a point to the Quad Tree
		The function finds the first None child then calls subdivide from that node
		This is also a recursive function (root becomes the child)

		Parameters
		----------
		root is the root node
		point is the point we want to add, or the cell that will become Alive

		Returns
		-------
		None	
		"""

		# Recursively traverse the tree until the correct non-empty node is
		# found that contains the bounding rectangle of our point to insert
		# We could call subdivide on the root, but this method is a little
		# more efficient.
		found = False
		for child in root.children:
			if child != None and child.contains(point[0], point[1]):
				found = True
				self.insert(child, point)
				
		
		if not found:
			#print "Subdividing to add point ", point
			root.subdivide(point)

		

	def delete(self, root, point):
		"""
		Use this to delete a point from the QuadTree.
		This function clears a child and then prunes if the point was
		found and deleted.

		Parameters
		----------
		root is the root node
		point to delete from the tree

		Returns
		-------
		True if item found and deleted, else false
		"""
		
		found = False

		# Need to check each child
		for child in range(len(root.children)):
			# Only search if not found.  
			if not found and root.children[child] != None and root.children[child].contains(point[0], point[1]):
				if root.children[child].type == GoLNode.LEAF:
					found = True
					#print "Deleting ", point
					root.children[child] = None
				else:
					found = self.delete(root.children[child], point)
		

		# Prune each parent to remove excess nodes.
		# We need to do this for each parent to save the most space.
		# This can be modified to save less space but run quicker by pruning
		# only the root node as shown below in comments.
		# We only try and delete when we actually have deleted something (found)
		#if found and root != None and root.parent != None:
		#	self.prune(root.parent)

		#if root.type == GoLNode.ROOT:
		#	self.prune(root)
			
		return found

	def is_element(self, root, point):
		"""
		This determines if point is an element of the QuadTree

		Parameters
		----------
		Root is the center of the grid
		Point is the element we are searching for

		Returns
		-------
		True if found, false if not.
		"""

		for child in root.children:
			if child != None and child.contains(point[0], point[1]):
				if child.type == GoLNode.LEAF:
					return True
				return self.is_element(child, point)

		return False

	
	def show_tree(self, root):
		"""
		This function attempts to show the status of the quadtree graphically

		Parameters
		----------
		Root is the center of the grid and all connections will be drawn from here

		Returns
		-------
		None
		"""
	
		# Verify working on the root node.
		if root.type != GoLNode.ROOT:
			print "Given node is not the root node."
			return

		x0, y0, x1, y1 = root.rect

		# Set initial figure and set axes to dimensions of root
		#plt.figure()

		plt.xlim(x0, x1)
		plt.ylim(y0, y1)

		# Recursive function that prints all connections
		self.print_tree(root)		

		#plt.show()	

	def print_tree(self, parent):
		"""
		This is a helper function to draw the lines on a figure

		Parameters
		----------
		Parent is the parent node and we will draw lines to its children

		Returns
		-------
		None
		"""
		x0, y0, x1, y1 = parent.rect
		lines = []

		x_cent = (x1-x0)/2+x0
		y_cent = (y1-y0)/2+y0		

		# This recursively calls the function for every child
		# and then draws a line from the center of the child's rect to the 
		# center of its parent's rect.
		for child in parent.children:
			if child != None:
				self.print_tree(child)
				
				cx0, cy0, cx1, cy1 = child.rect
				cx_cent = ((cx1-cx0)/2)+cx0
				cy_cent = ((cy1-cy0)/2)+cy0
			
				#print "Drawing line ", (x_cent, y_cent), (cx_cent, cy_cent)
				

				plt.plot((x_cent, cx_cent), (y_cent, cy_cent), 'bo-')
			
			

		

# Need to write spans_feature to check if point we are adding exists in the rectangle.  So we need to store the points somehow.  Save them in a set like the circle example?  Or should each node save it's own point if it is a leaf?  Then we need to override subdivide (basically rewrite the class at that point). 

# Tree where each branch has 4 children.  Root node is direct center of grid.  256x256 -> (128,128)
# Whenever adding a node, need to refine, by quadrant, down to single point
# No need to use instances of ConwayGOLCell, if a cell exists in quadtree, it's alive 
# Need to write add and del functions to add items and remove them from the tree efficiently
# Also need a good way to find neighbors, or store them on creation.
# 	Maybe use a set within the QuadTree to maintain alive items and check against this for neighbors
# 
# To add a node, need to subdivide (if necessary) and create the node to be added. This may require modifying
# 	the subdivide routine.
# To delete a node, just need to set it's position on it's parent to None then prune.
# 
#


if __name__ == '__main__':

	baserect = [0, 0, 16, 16]
	rootnode = GoLNode(None, baserect)
	tree = GoLQuadTree(rootnode, 0)

	tree.insert(rootnode, (0, 0))
	tree.show_tree(rootnode)
	tree.insert(rootnode, (5, 8))
	tree.show_tree(rootnode)
	tree.insert(rootnode, (1,1))
	tree.show_tree(rootnode)
	tree.insert(rootnode, (14, 11))
	tree.show_tree(rootnode)

	tree.delete(rootnode, (14,11))
	tree.show_tree(rootnode)
	

	baserect = [0, 0, 256, 256]
	rootnode = GoLNode(None, baserect)
	tree = GoLQuadTree(rootnode, 1)

	tree.show_tree(rootnode)

	tree.insert(rootnode, (34, 34))
	

	tree.show_tree(rootnode)

	tree.insert(rootnode, (56, 3))

	tree.show_tree(rootnode)

	tree.insert(rootnode, (128, 5))
	tree.show_tree(rootnode)

	tree.insert(rootnode, (253, 120))
	tree.show_tree(rootnode)



	tree.insert(rootnode, (253, 247))
	tree.insert(rootnode, (253, 248))
	tree.insert(rootnode, (238, 139))
	tree.insert(rootnode, (160, 230))
	tree.insert(rootnode, (178, 35))
	tree.insert(rootnode, (190, 78))
	tree.insert(rootnode, (32, 156))
	tree.insert(rootnode, (79, 230))
	tree.insert(rootnode, (120, 129))

	tree.show_tree(rootnode)

	tree.delete(rootnode, (253, 247))
	tree.delete(rootnode, (34, 34))
	tree.delete(rootnode, (56, 3))
	tree.delete(rootnode, (32, 156))
	tree.delete(rootnode, (79, 230))
	tree.delete(rootnode, (128, 5))
	tree.delete(rootnode, (160, 230))
	tree.delete(rootnode, (178, 35))
	tree.delete(rootnode, (120, 129))
	tree.delete(rootnode, (190, 78))

	tree.show_tree(rootnode)




















