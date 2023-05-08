# Name: Clay Beal
# Date: 1/22/23
# Wrote: Board Class
# Class: CIS 163
# Professor: Woodring

import copy
import pygame
import pygame_gui
import random

# Constant for board size.  GUI is optimized for 20.
SIZE = 20


class Game:
    """Game handles the core loop (events, updating, and drawing).  Game keeps an instance of a Board
    that is the world the cells "live" in.  All operations that directly modify the world are encapsulated
    in Board.  Game layout is not flexible; it is optimized for a 20x20 world.
    """

    def __init__(self):
        # A Board is the cells' world
        self._board = Board(SIZE)
        # We will represent a cell with a rectangle from the pygame library.  This function
        # creates them.
        self._rects = self.__make_rects__()
        # Startup pygame
        pygame.init()
        # Create a screen
        self._screen = pygame.display.set_mode([1024, 768])
        pygame.display.set_caption('Life')
        # GUI manager manages buttons, labels, sliders, etc.
        self._manager = pygame_gui.UIManager((1024, 768), "theme.json")
        # Create a play/pause button
        self._play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 75), (100, 50)),
                                                         text='Paused',
                                                         manager=self._manager)
        # Create a label for the generation number
        self._generations_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((700, 150), (250, 50)),
                                                              text='Generations: 0',
                                                              manager=self._manager)
        # Create a button for random board layout
        self._random_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 225), (250, 50)),
                                                              text='Randomize',
                                                              manager=self._manager)
        # Create a button to reset generations and the world
        self._reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 300), (250, 50)),
                                                              text='Reset',
                                                              manager=self._manager)
        # Create a label for the speed slider
        self._speed_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((700, 375), (250, 50)),
                                                              text='Speed: 250ms',
                                                              manager=self._manager)
        # Create a slider to control sim speed
        self._speed_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((700, 450), (250, 50)),
                                                                    start_value=250,
                                                                    value_range=(0, 1000),
                                                                    manager=self._manager)
        # Track if the simulation is running or not
        self._running = False
        # Track if the application should be finished and close
        self._finished = False
        # Number of generations
        self._generations = 0
        # Default delay in milliseconds (ms)
        self._delay = 250

    def loop(self):
        """Main simulation loop.  Checks for events and handles them.  Updates world accordingly.  Redraws
        world.  Starts over if no QUIT event has occurred.  Notice that _delay is a blocking delay; it
        will make the GUI less responsive.  It shouldn't be too hard to change this, but I didn't really care
        that much.
        """

        # Keep a clock for frame limiting
        clock = pygame.time.Clock()
        # Keep going until this changes; will change when a user clicks the close button.
        while not self._finished:
            # Ensure 60 frames per second
            time_delta = clock.tick(60)/1000.0
            # Ask pygame for events
            for event in pygame.event.get():
                # If window close event happens, set _finished to True
                if event.type == pygame.QUIT:
                    self._finished = True
                # Left mouse click events
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Find coordinate of click
                    coords = pygame.mouse.get_pos()
                    # See if that coordinate is in a cell.  If it is, this function returns which one.
                    i, j, rectangle = self.__select_rectangle__(coords)
                    # If function returned None it means we didn't click a cell
                    if rectangle is not None:
                        # We clicked a cell.  Change its color.
                        self._board.change_color(i, j)
                # Did the user click a button?  If so, figure out which and call the
                # appropriate function.
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self._play_button:
                        self.toggle()
                    if event.ui_element == self._reset_button:
                        self.reset()
                    if event.ui_element == self._random_button:
                        self.randomize()
                # Speed slider moved.  Update the label.
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    self._speed_label.set_text("Speed: " + str(self._speed_slider.get_current_value()) + "ms")
                    self._delay = int(self._speed_slider.get_current_value())
                # Have the GUI manager handle GUI events
                self._manager.process_events(event)

            # Let the GUI manager know the time change since last frame
            self._manager.update(time_delta)
            # If we aren't paused, calculate the next generation
            if self._running:
                # Cell updates happen in the Board class.  Call it.
                self._board.update()
                # Increment generations.
                self._generations = self._generations + 1
                # Update generations label
                self._generations_label.set_text("Generations: " + str(self._generations))
                # Wait to delay.  Not the best method, but eh.
                pygame.time.wait(self._delay)

            # Fill the screen with white
            self._screen.fill((255, 255, 255))
            # Redraw the world
            self.__draw_board__()
            # Redraw the GUI elements
            self._manager.draw_ui(self._screen)
            # Flip buffers
            pygame.display.update()

        # Loop is over (user clicked quit).  Shutdown pygame.
        pygame.quit()

    def reset(self):
        """Set the simulation back to its starting point values (blank world, zero generations)."""

        self._board = Board(SIZE)
        self._generations = 0

    def randomize(self):
        """Create a random world.  Would be neat to expand it to accept values for density of cells,
        but I didn't want to today.  Fill level at about 20% works pretty well."""

        self._board = Board(SIZE)
        for i in range(SIZE):
            for j in range (SIZE):
                if random.randint(1, 100) <= 20:
                    self._board.change_color(i, j)

    def toggle(self):
        """Play/pause the sim."""

        self._running = not self._running
        if self._running:
            self._play_button.set_text("Running")
        else:
            self._play_button.set_text("Paused")

    def __select_rectangle__(self, coords: [int, int]) -> (int, int, pygame.Rect):
        """Given a set of coordinates, determine if they lie in one of our rectangles
        that represent our cells.  If so, return coordinates and the rectangle.  Otherwise
        return a triple of None."""

        for i in range(SIZE):
            for j in range(SIZE):
                if self._rects[i][j].collidepoint(coords):
                    return i, j, self._rects[i][j]
        return None, None, None

    def __make_rects__(self):
        """Make and return an SIZE x SIZE list of pygame Rectangles.  These will be
        used to visually represent our cells."""

        rectangles = []
        for i in range(SIZE):
            rectangles.append([])
            for j in range(SIZE):
                rectangles[i].append(pygame.Rect(i * 34, j * 34, 32, 32))
        return rectangles

    def __draw_board__(self):
        """Loop over the board and draw each rectangle with the appropriate color."""

        board = self._board.get_board()
        for i in range(SIZE):
            for j in range(SIZE):
                pygame.draw.rect(self._screen, board[i][j], self._rects[i][j])


# Write your code to complete the project below this line.

# Name: Clay Beal
# Date: 1/22/23
# Class: CIS 163
# Professor: Woodring


class Board:
    """
    The board class is a blueprint for a board which may consist of different
    sizes and creates a tuple (0,0,0) default to hold a color value for each
    individual cell in the size x size board

    Attributes:
        size (int): the size of the board to be created (size x size)
        _board (list): This is a list of lists of tuples (0,0,0) default
                       The number of tuples per list depends on size
        _prior (list): Same as _board, holds a copy of the _board for
                       modifications to take place more easily
    """
    def __init__(self, size) -> None:
        """
        Creates a new board and initializes size, creates the default
        board layout and places a copy of the board into _prior

        Parameters:
            size (int): the size of the board to be created (size x size)
        """
        self.size = size
        # Makes a board using nested lists of (0, 0, 0) (size x size)
        self._board = [[(0, 0, 0) for i in range(size)] for j in range(size)]
        # Makes a copy of the board used for updating the board
        self._prior = copy.deepcopy(self._board)

    def get_board(self) -> list:
        """
        Getter for the board attribute

        Returns:
            _board (list): list of lists of tuples containing the colors
                           for the respective board cells

        """
        return self._board

    def change_color(self, i: int, j: int) -> None:
        """
        This function uses three variables (r, g, b) to compute a random
        color and assigns it to a passed in index on the board

        Parameters:
            i (int): represents a passed in index
            j (int): represents a passed in index

        Variables:
            r_val (int): random integer from 0-255 to represent a color value
            g_val (int): random integer from 0-255 to represent a color value
            b_val (int): random integer from 0-255 to represent a color value
        """
        # Gets a random integer from 0 - 255
        r_val = random.randint(0, 255)
        g_val = random.randint(0, 255)
        b_val = random.randint(0, 255)
        # Sets a specific passed index to a tuple of three random integers
        self._board[i][j] = (r_val, g_val, b_val)

    def count_neighbors(self, i: int, j: int) -> tuple[int, tuple[int, int, int]]:
        """
        Counts the number of neighbors a specific cell has, as well as
        computes the average color of the neighbors if at least one is
        present.

        Parameters:
            i (int): represents a passed in index
            j (int): represents a passed in index

        Variables:
            num_neighbors (int): Holds the number of neighbors a specific cell
                                 has.
            color_list (list): Holds a list of the tuples of active neighbors
                               Ex. [(5,100,150), (20,230,200)]
            r_total (int): Used to get the total of all the r values in the
                           active tuples Ex. (r, g, b)
            g_total (int): Used to get the total of all the g values in the
                           active tuples Ex. (r, g, b)
            b_total (int): Used to get the total of all the b values in the
                           active tuples Ex. (r, g, b)
            avg_color (tuple): Holds the value for the average color of the
                               alive cells

        Returns:
            num_neighbors (int): Number of active neighbor cell's
            avg_color (tuple): Holds the average color of the neighbor cells
        """
        # Holds number of neighbors
        num_neighbors = 0
        # Holds a list of tuples, each one being of an active neighbor cell
        color_list = []
        # Holds the totals of the first, second, and third index of the tuples
        r_total = 0
        g_total = 0
        b_total = 0

        # This algorithm checks to see if the neighboring cells of one at
        # the passed in index hold a tuple that's NOT (0, 0, 0), meaning
        # that they are active. If it is active it saves that specific
        # tuple in a list and increments the active neighbor count
        # Checks a range from -1 to 1
        for x in range(-1, 2):
            # Checks a range from -1 to 1
            for y in range(-1, 2):
                # Passes if x and y are 0, because that would mean we are
                # checking the passed in index instead of it's neighbors
                if x == 0 and y == 0:
                    pass
                else:
                    try:
                        # Checks to see if the indexes neighbors are active
                        # on the prior board, as we only update the actual one
                        # Also makes sure the index isn't checking -1 to ensure
                        # the index doesn't wrap from index [0] to [-1]
                        if self._prior[i + x][j + y] != (0, 0, 0) and\
                                (i + x != -1 and j + y != -1):
                            # Increment neighbor count
                            num_neighbors += 1
                            # Add the active neighbor tuple to the color list
                            color_list.append(self._prior[i + x][j + y])
                    # If there is an index error continue with the other
                    # neighbor checks, must mean the neighbor doesn't exist
                    except IndexError:
                        pass
        # If the number of neighbors is greater than 0
        if num_neighbors > 0:
            # Get the total of the (r, g, b) values respectively
            for color_tuple in color_list:
                r_total += color_tuple[0]
                g_total += color_tuple[1]
                b_total += color_tuple[2]
            # Dives each one of those values by the length of the color list
            # and put it in a tuple
            avg_color = (r_total / len(color_list), g_total / len(color_list),
                         b_total / len(color_list))
        # If there are no neighbors set average color to (0, 0, 0)
        else:
            avg_color = (0, 0, 0)
        # Return the number of neighbors and the average color tuple
        return num_neighbors, avg_color

    def update(self) -> None:
        """
        Looks at the board from the previous generation and updates the board
        depending on the number of neighbors a cell has and color of it's neighbors
        Also gives a chance for a mutation to occur 1% of the time
        """
        # Makes a new copy of the actual board into prior
        self._prior = copy.deepcopy(self._board)
        # Loops through the length and width of the board
        # (i and j being indexes to pass to count_neighbors)
        for i in range(len(self._prior)):
            for j in range(len(self._prior)):
                # Gets the neighbors and average color of the neighbors
                num_neighbors, avg_color = self.count_neighbors(i, j)
                # Checks to see if a specific cell has less than two or more
                # than three neighbors
                if num_neighbors < 2 or num_neighbors > 3:
                    # Makes specific index on the board "dead" (0, 0, 0)
                    self._board[i][j] = (0, 0, 0)
                # Checks to see if the number of neighbors is exactly three
                elif num_neighbors == 3:
                    # Makes that index the average color of the
                    # surrounding neighbors
                    self._board[i][j] = avg_color
                else:
                    pass
        # Sets a variable as a random integer from 0 to 100
        mutation = random.randint(1, 100)
        # Checks to see if that integer is equal to 42
        if mutation == 42:
            # Sets a random cell on the board equal to a random color
            self.change_color(random.randint(0, 19), random.randint(0, 19))
