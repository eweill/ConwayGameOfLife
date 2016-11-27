# Import necessary libraries
#import numpy as np
import matplotlib.pyplot as plt
from random import randint
from copy import deepcopy
import numpy as np
import unittest, sys
#import pylab


# Conway Game of Life Grid Class
class ConwayGOLGrid():
    """
    Represents a grid in the Conway's Game of Life problem where each of the cells contained in the
    grid may be either alive of dead for any given state.
    """

    def __init__(self, width=100, height=100, startCells=[],
                 optimized=True, variant="B3/S23"):
        """
        Initializes a Grid as a 2D list and comprised of Cells.

        Parameters
        ----------
        width, height: size of the board
        startCells: list of cells to start as alive.
            If startCells is empty, cells spawn as alive at a rate of 30%.
            startCells should be a list of coordinates (x, y)
        optimized: determines whether or not to use data structures to improve run-time.
        variant: defines variant of life played. Options as follows:
            B3/S23: default (Born with 3, Survives with 2 or 3)
            B6/S16
            B1/S12
            B36/S23: High life
            B2/S3: Seeds
            B2/S
        """
        self.width, self.height = width, height
        self.__optimized = optimized
        self.cells = []
        self.__living = set()

        if variant == "B3/S23":
            self.__born = [3]
            self.__survives = [2, 3]
        elif variant == "B6/S16":
            self.__born = [6]
            self.__survives = [1, 6]
        elif variant == "B1/S12":
            self.__born = [1]
            self.__survives = [1, 2]
        elif variant == "B36/S23":
            self.__born = [3, 6]
            self.__survives = [2, 3]
        elif variant == "B2/S3":
            self.__born = [2]
            self.__survives = [3]
        elif variant == "B2/S":
            self.__born = [2]
            self.__survives = []
        else:
            print variant, " is not a valid variant. Using B3/S23."
            self.__born = [3]
            self.__survives = [2, 3]

        for x in range(self.width):
            # Create new list for 2D structure
            self.cells.append([])

            for y in range(self.height):
                # If startCells not provided, randomly init grid
                if len(startCells) == 0 and randint(0, 100) < 30:
                    self.cells[x].append(ConwayGOLCell(x, y, True))
                    self.__living.add((x, y))

                else:
                    self.cells[x].append(ConwayGOLCell(x, y))

        # Give life to all cells in the startCells list
        for cell in startCells:
            self.cells[cell[0]][cell[1]].spawn()
            self.__living.add((cell))

    def update(self):
        """
        Updates the current state of the game using the standard Game of Life rules.

        Parameters
        ----------
        None

        Returns
        -------
        True if there are remaining alive cells.
        False otherwise.
        """
        alive = False

        if not self.__optimized:
            # Deep copy list to make sure entire board updates correctly
            tempGrid = deepcopy(self.cells)

            # For every cell, check the neighbors.
            for x in range(self.width):
                for y in range(self.height):
                    neighbors = self.cells[x][y].num_neighbors(self)

                    # Living cells stay alive with __survives # of neighbors, else die
                    if self.cells[x][y].is_alive():
                        if not (neighbors in self.__survives):
                            tempGrid[x][y].die()
                        else:
                            alive = True

                    # Non living cells come alive with 3 neighbors
                    else:
                        if neighbors in self.__born:
                            tempGrid[x][y].spawn()
                            alive = True

            # Deep copy the tempGrid to prevent losing reference
            self.cells = deepcopy(tempGrid)

        else:
            count = [[0 for y in range(self.height)] for x in range(self.width)]
            to_check = set()

            # For each cell that is alive...
            for cell in self.__living:
                x, y = cell
                to_check.add(cell)

                # Retrieve all neighbors
                for neighbor in self.cells[x][y].neighbors:
                    n_x, n_y = neighbor
                    # If neighbors are valid
                    if (n_x >= 0 and n_y >= 0 and
                                n_x < self.width and n_y < self.height):
                        # Then increment count and add them to the set
                        count[n_x][n_y] += 1
                        to_check.add(neighbor)

            # Start over living.
            self.__living = set()

            # Above, we add 1 to the count each time a cell is touched by an alive cell.
            # So we know count contains the number of alive neighbors any given cell has.
            # We use this to quickly check the rules of life and add cells to living list.
            for cell in to_check:
                x, y = cell

                if self.cells[x][y].is_alive():
                    if not count[x][y] in self.__survives:
                        self.cells[x][y].die()
                    else:
                        self.__living.add(cell)
                        alive = True
                else:
                    if count[x][y] in self.__born:
                        self.cells[x][y].spawn()
                        self.__living.add(cell)
                        alive = True

        return alive

    def get_living(self):
	"""
	Returns a 2D list with False representing dead cells and True representing alive cells.

	Parameters
	----------
	None

	Returns
	-------
	2D binary list with 1's counting as alive cells

	"""	
	cells = [[False for y in range(self.height)] for x in range(self.width)]

	for x, y in self.__living:
		cells[x][y] = True

	return cells

    def print_text_grid(self):
        """
        Prints the current state of the board using text.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[x][y].is_alive():
                    print "X",
                else:
                    print ".",
            print "\n"
        print "\n\n"

    def print_grid(self, im, fig):
        """
        Prints the current state of the board with matplotlib.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        cells = self.get_living()
        im.set_data(cells)
        fig.canvas.draw()



### Conway Game of Life Cell Class
class ConwayGOLCell():
    """
    Represents a cell in the Conway's Game of Life problem where a cell can either be alive or
    dead and the next state of the cell is based on the states of the immediates (8) neighbors.
    """

    def __init__(self, x, y, alive=False):
        """
        Create information for teh given cell including the x and y coordinates of the cell,
        whether it is currently alive or dead, it's neighbors, and its current color.

        Parameters
        ----------
        x, y: gives the coordinates fo the cell in the grid
        alive: gives current state of the cell

        Returns
        -------
        None
        """
        self.x, self.y = x, y
        self.alive = alive
        self.neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                          (x - 1, y), (x + 1, y),
                          (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        self.color = (255, 255, 255)

    def spawn(self):
        """
        Changes the state of a cell from dead to alive. Assumes that the cell is dead to be
        changed to alive (no need to modify if already alive).

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        assert self.alive == False
        self.alive = True

    def die(self):
        """
        Changes the state of a cell from alive to dead. Assumes that the call is alive to be
        changed to dead (no need to modify if already dead).

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        assert self.alive == True
        self.alive = False

    def is_alive(self):
        """
        Returns status of a cell.

        Parameters
        ----------
        None

        Returns
        -------
        True if cell is alive, false otherwise.
        """
        return self.alive

    def num_neighbors(self, grid):
        """
        Returns the number of neighbors of a cell.

        Parameters
        ----------
        grid: the ConwayGOLGrid object containing all cells

        Returns
        -------
        number of alive neighbors
        """
        num_neighbors = 0

        for cell in self.neighbors:
            x, y = cell
            if (x >= 0 and x < grid.width and
                y >= 0 and y < grid.height and
                grid.cells[x][y].is_alive()):
                num_neighbors += 1

        return num_neighbors



# Write a set of unit tests to check the functionality and correctness of each
# method that is part of class above.
class TestConwayCell(unittest.TestCase):
	def test_cell_is_alive(self):
		"""Test status of each cell (living or dead)."""
		# Initialize a Conway Grid with a few living cells.
		# Alive cells: (1,3), (3,6), (5,5), (7,2), (9,6)
		test_game = ConwayGOLGrid(10, 10, [(1, 3), (3, 6), (5, 5), (7, 2), (9, 6)], 
			optimized=True, variant="B1/S12")
		self.assertEqual(test_game.cells[1][3].is_alive(), True)	# Live cell
		self.assertEqual(test_game.cells[3][6].is_alive(), True)	# Live cell
		self.assertEqual(test_game.cells[5][5].is_alive(), True)	# Live cell
		self.assertEqual(test_game.cells[7][2].is_alive(), True)	# Live cell
		self.assertEqual(test_game.cells[9][6].is_alive(), True)	# Live cell
		self.assertEqual(test_game.cells[1][1].is_alive(), False)	# Dead cell
		self.assertEqual(test_game.cells[5][4].is_alive(), False)	# Dead cell
		self.assertEqual(test_game.cells[9][9].is_alive(), False)	# Dead cell

	def test_cell_spawn(self):
		"""Test spawning a cell (brining to life a dead cell)."""
		# Initialize a Conway Grid with a few living cells.
		# Alive cells: (1,3), (3,6), (5,5), (7,2), (9,6)
		test_game = ConwayGOLGrid(10, 10, [(1, 3), (3, 6), (5, 5), (7, 2), (9, 6)], 
			optimized=True, variant="B1/S12")
		self.assertEqual(test_game.cells[9][6].is_alive(), True)	# Live cell
		self.assertEqual(test_game.cells[1][1].is_alive(), False)	# Dead cell
		# Spawn a cell on the grid in position (1,1)
		test_game.cells[1][1].spawn()
		self.assertEqual(test_game.cells[1][1].is_alive(), True)	# New live cell

	def test_cell_die(self):
		"""Test killing a cell (taking the live from an alive cell)."""
		# Initialize a Conway Grid with a few living cells.
		# Alive cells: (1,3), (3,6), (5,5), (7,2), (9,6)
		test_game = ConwayGOLGrid(10, 10, [(1, 3), (3, 6), (5, 5), (7, 2), (9, 6)], 
			optimized=True, variant="B1/S12")
		self.assertEqual(test_game.cells[9][6].is_alive(), True)	# Live cell
		self.assertEqual(test_game.cells[1][1].is_alive(), False)	# Dead cell
		test_game.cells[9][6].die()
		self.assertEqual(test_game.cells[9][6].is_alive(), False)	# New dead cell

	def test_cell_num_neighbors(self):
		"""Test the number of neighbors that are alive for a given cell."""
		# Initialize a Conway Grid with a few living cells.
		# Alive cells: (1,2), (1,3), (2,1), (3,1), (3,3),
		#			   (6,6), (6,7), (7,7), (7,8), (8,8)
		test_game = ConwayGOLGrid(10, 10, [(1, 2), (1, 3), (2, 1), (3, 1), (3, 3),
			(6, 6), (6, 7), (7, 7), (7, 8), (8, 8)], optimized=True, variant="B1/S12")
		# Test to make sure method works on dead cells
		self.assertEqual(test_game.cells[2][2].num_neighbors(test_game), 5)	# (2, 2) has 5 neighbors
		# Test to make sure method works on alive cells
		self.assertEqual(test_game.cells[7][7].num_neighbors(test_game), 4)

class TestConwayGrid(unittest.TestCase):
	def test_grid_get_living(self):
		"""Test the get living function to make sure it returns the correct grid."""
		# Initialize a Conway Grid with a few living cells (on a 5x5 grid)
		# Alive cells: (1,1), (2,4), (3,1), (4,3)
		test_game = ConwayGOLGrid(5, 5, [(1, 1), (2, 4), (3, 1), (4, 3)],
			optimized=True, variant="B1/S12")
		cells = test_game.get_living()
		for y in range(test_game.height):
			for x in range(test_game.width):
				if (x==1 and y==1) or (x==2 and y==4) or (x==3 and y==1) or (x==4 and y==3):
					self.assertEqual(cells[x][y], True)
				else:
					self.assertEqual(cells[x][y], False)

	def test_grid_update_box(self):
		"""Test the update function with the B3/S23 rule and a box"""
		# Initialize the board with a box and test B3/S23 (Should remain a box)
		test_game_box = ConwayGOLGrid(4, 4, [(2, 2), (2, 3), (3, 2), (3, 3)],
			optimized=True, variant="B3/S23")
		# Perform an update step and make sure the box remains
		cells_before_update = test_game_box.get_living()
		test_game_box.update()
		cells_after_update = test_game_box.get_living()
		self.assertEqual(cells_before_update, cells_after_update)
		test_game_box.update()
		cells_after_update2 = test_game_box.get_living()
		self.assertEqual(cells_after_update, cells_after_update2)

	def test_grid_update_beehive(self):
		"""Test the update function with the B2/S23 rule and a beehive"""
		# Initialize the board with a beehive and test B2/S23 (Should remain a beehive)
		test_game_beehive = ConwayGOLGrid(6, 6, [(2, 3), (2, 4), (3, 2), (3, 5), (4, 3), (4, 4)],
			optimized=True, variant="B3/S23")
		cells_before_update = test_game_beehive.get_living()
		test_game_beehive.update()
		cells_after_update = test_game_beehive.get_living()
		self.assertEqual(cells_before_update, cells_after_update)
		test_game_beehive.update()
		cells_after_update2 = test_game_beehive.get_living()
		self.assertEqual(cells_after_update, cells_after_update2)

	def test_grid_update_blinker(self):
		"""Test the update function with the B3/S23 rule and a blinker"""
		# Initialize the board with a blinker (after update should rotate 90 degrees)
		test_game_blinker = ConwayGOLGrid(4, 4, [(1, 2), (2, 2), (3, 2)],
			optimized=True, variant="B3/S23")
		cells_beginning = test_game_blinker.get_living()
		# Perform an update step and make sure the blinker rotates 90 degrees
		test_game_blinker.update()
		# Check to see if the only cells that are alive are the rotated blinker
		for y in range(test_game_blinker.height):
			for x in range(test_game_blinker.width):
				if (x==2 and y==1) or (x==2 and y==2) or (x==2 and y==3):
					self.assertEqual(test_game_blinker.cells[x][y].is_alive(), True)
				else:
					self.assertEqual(test_game_blinker.cells[x][y].is_alive(), False)
		# Run another update step and make sure the blinker returns to original
		test_game_blinker.update()
		cells_after_update2 = test_game_blinker.get_living()
		self.assertEqual(cells_beginning, cells_after_update2)

	def test_grid_update_toad(self):
		"""Test the update functionw with the B3/S23 rule and a toad"""
		# Initialize the board with a toad (after update should blink then return)
		test_game_toad = ConwayGOLGrid(6, 6, [(3, 3),(3, 4),(3, 5),(4, 2),(4, 3),(4, 4)],
			optimized=True, variant="B3/S23")
		cells_beginning = test_game_toad.get_living()
		# Perform an update step and make sure the toad transforms correctly
		test_game_toad.update()
		# Check to see if the correct cells are alive
		for y in range(test_game_toad.height):
			for x in range(test_game_toad.width):
				if ((x==2 and y==4) or (x==3 and y==2) or (x==3 and y==5) or 
					(x==4 and y==2) or (x==4 and y==5) or (x==5 and y==3)):
					self.assertEqual(test_game_toad.cells[x][y].is_alive(), True)
				else:
					self.assertEqual(test_game_toad.cells[x][y].is_alive(), False)
		# Run another update step and make sure the toad returns to original
		test_game_toad.update()
		cells_after_update2 =test_game_toad.get_living()
		self.assertEqual(cells_beginning, cells_after_update2)


# Main function to test Conway's Game of Life
if __name__ == '__main__':
	# Test Grid
	test_game = ConwayGOLGrid(200, 200, [(100, 100)], optimized=True, variant="B1/S12")
	fig, ax = plt.subplots()
	ax.axis('off')
	im = ax.imshow(test_game.get_living(), interpolation='nearest', cmap=plt.cm.binary)
	fig.show()

	count = 0
	while count < 20 and test_game.update():
		count += 1
		test_game.print_grid(im, fig)
		plt.pause(0.05)

	print "Finished after ", count, "iterations."

	cell_suite = unittest.TestLoader().loadTestsFromTestCase(TestConwayCell)
	unittest.TextTestRunner().run(cell_suite)

	grid_suite = unittest.TestLoader().loadTestsFromTestCase(TestConwayGrid)
	unittest.TextTestRunner().run(grid_suite)
