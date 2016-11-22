# Import necessary libraries
#import numpy as np
import matplotlib.pyplot as plt
from random import randint
from copy import deepcopy
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
        pass

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

    def print_grid(self, fig, ax):
        """
        Prints the current state of the board with matplotlib.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        cells = [[0 for x in range(self.width)] for y in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[x][y].is_alive():
                    cells[x][y] = 1
                else:
                    cells[x][y] = 0
        # fig, ax = plt.subplots(1, 1, tight_layout=True)
        #ax.imshow(cells, interpolation='nearest', cmap=plt.cm.binary)
        ax.axis('off')
        ax.set_data(cells)
        # pylab.show()
        # plt.show()
        fig.canvas.draw()
        return cells


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




# Test Grid
test_game = ConwayGOLGrid(25, 25, optimized=True, variant="B3/S23")

fig, ax = plt.subplots()

im = ax.imshow(test_game.get_living())


### Test Text Grid
test_game = ConwayGOLGrid(25, 25, optimized=True, variant="B3/S23")

# test_game.print_text_grid()
fig, ax = plt.subplots()
#f = plt.figure()
#ax = f.gca()
#f.show()

cells = test_game.print_grid()

count = 0

while count < 40 and test_game.update():
    count += 1
    print count
    # test_game.print_text_grid()
    cells = test_game.print_grid(fig, ax)
    plt.pause(0.05)

print "Finished after ", count, "iterations."
