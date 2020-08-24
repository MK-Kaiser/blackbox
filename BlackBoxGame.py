#!/usr/bin/env python3
# Author: Mark Kaiser
# Date: 8/9/20
# Description: A game called BlackBox played on a 10x10 grid where the guessing player will start with 25 points
# during each turn, the player will shoot rays into the black box. 5 points are lost for incorrect guesses, and 1 point
# is lost for each new entry/exit point. Behavior of the ray serves as an indicator of where the player should guess.
# The goal is to correctly guess where each atom position is and target each atom with a ray.


class BlackBoxGame:
    """Responsible for overall state of the game, creates new Player and Board object and atom positions.
    Interacts with Player class object to set/get player score, previous guesses, and previous entry/exit points.
    Interacts with Board class object to get board layout and set atom positions in place."""

    def __init__(self, atom_positions):
        """Initializes datamembers that create Player object and Board object with atom_positions. Initializes
        legal entry points, list of grid edges, list of atoms found to be within these grid edge positions,
        set of deflection and reflection squares and builds a set of all deflection, double deflection and
        reflection squares with deflection_squares(), double_deflection_squares() and reflection_squares() methods."""
        self._player = Player()  # creates Player class object
        self._board = Board(atom_positions)  # creates Board class object
        self._atom_positions = atom_positions
        self._atoms_left = dict()  # dictionary to track atoms remaining versus hit
        for a in atom_positions:   # adds atoms to dictionary
            self._atoms_left[a] = 'remaining'
        self._legal_entry = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (2, 0), (3, 0),
                             (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9),
                             (7, 9), (8, 9), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8)]
        self._board.set_board(self._legal_entry)
        self._grid_edge = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 8), (3, 8), (4, 8),
                           (5, 8), (6, 8), (7, 8), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (8, 2),
                           (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
        self._atom_on_grid_edge = [atom for atom in atom_positions if atom in self._grid_edge]
        self._double_deflection_squares = set()  # set to store tuples considered as double deflection squares
        self._deflection_squares = set()  # set to store tuples considered as deflection squares
        self._reflection_squares = set()  # set to store tuples considered as reflection squares
        self.reflection_squares()  # calls method to search for reflection squares
        self.deflection_squares()  # calls method to search for deflection squares
        self.double_deflection_squares()  # calls method to search for double deflection squares

    def shoot_ray(self, row, column):
        """Takes as parameters the row and column of the entry border square.
        If this is a corner square or a non-border square, will return False.
        Otherwise, as helper function will kick off rec_shoot_ray() and return a tuple with (row,column) exit point."""
        position = (row, column)
        if position not in self._legal_entry:  # checks if entry is legal
            return False
        else:
            return self.rec_shoot_ray(position, position)

    def rec_shoot_ray(self, position, previous):
        """Takes as parameters the current square. Will recursively move through board squares and do checks for
        different situations such as reflection, deflection, double deflection, and detour/combos. If any of these
        situational methods are initiated entry/exit score adjustments are made by calling set_score().
        This will continue until ray reaches exit square and returns a tuple of the row and column exit point or
        detects an atom hit. Checks current position for an atom. If successfully hit atom, ray will not exit."""
        if position in self._legal_entry and previous not in self._legal_entry:  # base case: checks if exit reached
            self._player.set_entry_exit(position)
            return position  # returns tuple
        elif position in self._atom_positions:  # detects a hit
            return
        elif position in self._reflection_squares:  # handles reflections
            self._player.set_entry_exit(position)
            return position
        elif position in self._double_deflection_squares:  # if position is double deflection square
            return self.double_deflection(position, previous)  # determines next position based on double deflection
        elif position in self._deflection_squares:  # if position is deflection square
            new_position = self.deflection(position, previous)  # determines next position based on deflection handling
            previous = position
            return self.rec_shoot_ray(new_position, previous)
        else:
            new_position = self.move(position, previous)  # if none of the above apply, continues moving forward
            previous = position
            return self.rec_shoot_ray(new_position, previous)

    def move(self, position, previous):
        """Handles the first movement of the ray from the grid edge. Returns a new position"""
        if position in self._legal_entry and previous not in self._grid_edge:  # first move only
            self._player.set_entry_exit(position)
            if position[0] == 0:  # moving right, along row
                return ((position[0] + 1), position[1])
            if position[0] == 9:  # moving left, along row
                return ((position[0] - 1), position[1])
            if position[1] == 0:  # moving down, along column
                return (position[0], (position[1] + 1))
            if position[1] == 9:  # moving up, along column
                return (position[0], (position[1] - 1))
        else:
            return self.successive_move(position, previous)

    def successive_move(self, position, previous=None):
        """If not the first move, then moves forward based on previous position. Returns a new position."""
        if previous is not None and position is not None:
            # post deflection movement handling
            if position[0] > previous[0] and position[1] != previous[1]:
                return ((position[0] + 1), (position[1]))
            if position[0] < previous[0] and position[1] != previous[1]:
                return ((position[0] - 1), (position[1]))
            if position[1] > previous[1] and position[0] != previous[0]:
                return ((position[0]), (position[1] + 1))
            if position[1] < previous[1] and position[0] != previous[0]:
                return ((position[0]), (position[1] - 1))
            # normal movement handling
            if position[0] > previous[0]:  # if moving right, along row
                return ((position[0] + 1), position[1])
            if position[0] < previous[0]:  # if moving left, along row
                return ((position[0] - 1), position[1])
            if position[1] > previous[1]:  # if moving down, along column
                return (position[0], (position[1] + 1))
            if position[1] < previous[1]:  # if moving up, along column
                return (position[0], (position[1] - 1))

    def deflection_squares(self):
        """Finds and builds a set containing square positions that require special handling. Searches the board for
        deflection squares, which are all empty positions diagonal to an atom."""
        # creates a list of all non-grid_edge atoms
        non_grid_atoms = [atom for atom in self._atom_positions if atom not in self._atom_on_grid_edge]
        for n in non_grid_atoms:  # iterate through list and compare if any are 1 position apart from another
            for a in range(0, 3):
                if self._board.get_board()[(n[0] - 1)][(n[1] - 1)] == ' ':  # diagonal up and left of atom
                    self._deflection_squares.add(((n[0] - 1), (n[1] - 1)))
                if self._board.get_board()[(n[0] + 1)][(n[1] - 1)] == ' ':  # diagonal down and left of atom
                    self._deflection_squares.add(((n[0] + 1), (n[1] - 1)))
                if self._board.get_board()[(n[0] - 1)][(n[1] + 1)] == ' ':  # diagonal up and right of atom
                    self._deflection_squares.add(((n[0] - 1), (n[1] + 1)))
                if self._board.get_board()[(n[0] + 1)][(n[1] + 1)] == ' ':  # diagonal down and right of atom
                    self._deflection_squares.add(((n[0] + 1), (n[1] + 1)))

    def deflection(self, position, previous):
        """Takes in current position and if is a deflection square, determines new direction of movement.
        Returns a new position as a tuple so that move() can continue the course."""
        for a in self._atom_positions:
            if position == ((a[0] - 1), (a[1] - 1)):  # check if diagonal up and left of atom
                if previous == ((position[0] - 1), (position[1])):  # coming from above
                    return ((position[0]), (position[1] - 1))
                elif previous == ((position[0]), (position[1] - 1)):  # coming from left
                    return ((position[0] - 1), (position[1]))
            if position == ((a[0] + 1), (a[1] - 1)):  # check if diagonal down and left of atom
                if previous == ((position[0] + 1), (position[1])):  # coming from below
                    return ((position[0]), (position[1] - 1))
                elif previous == ((position[0]), (position[1] - 1)):  # coming from left
                    return ((position[0] + 1), (position[1]))
            if position == ((a[0] - 1), (a[1] + 1)):  # check if diagonal up and right of atom
                if previous == ((position[0] - 1), (position[1])):  # coming from above
                    return ((position[0]), (position[1] + 1))
                elif previous == ((position[0]), (position[1] + 1)):  # coming from right
                    return ((position[0] - 1), (position[1]))
            if position == ((a[0] + 1), (a[1] + 1)):  # check if diagonal down and right of atom
                if previous == ((position[0] + 1), (position[1])):  # coming from below
                    return ((position[0]), (position[1] + 1))
                elif previous == ((position[0]), (position[1] + 1)):  # coming from right
                    return ((position[0] + 1), (position[1]))

    def double_deflection_squares(self):
        """Finds overlapping deflection squares that are identified as deflection squares for two separate atoms.
        Adds double defleciton squares to a set. These squares are adjacent to the square between two atoms."""
        for n in self._atom_positions:
            for a in self._atom_positions:
                # vertical double deflection squares
                if (n[0], (n[1] + 2)) == a:
                    self._double_deflection_squares.add(((n[0] + 1), (n[1] + 1)))
                    self._double_deflection_squares.add(((n[0] - 1), (n[1] + 1)))
                if (n[0], (n[1] - 2)) == a:
                    self._double_deflection_squares.add(((n[0] + 1), (n[1] - 1)))
                    self._double_deflection_squares.add(((n[0] - 1), (n[1] - 1)))
                # horizontal double deflection squares
                if ((n[0] + 2), n[1]) == a:
                    self._double_deflection_squares.add(((n[0] + 1), (n[1] + 1)))
                    self._double_deflection_squares.add(((n[0] + 1), (n[1] - 1)))
                if ((n[0] - 2), n[1]) == a:
                    self._double_deflection_squares.add(((n[0] - 1), (n[1] + 1)))
                    self._double_deflection_squares.add(((n[0] - 1), (n[1] - 1)))

    def double_deflection(self, position, previous):
        """Takes in current position if is a double deflection square. Reverses ray direction to return to sender."""
        new_position = previous
        previous = position
        return self.rec_shoot_ray(new_position, previous)

    def reflection_squares(self):
        """Finds and builds a set containing square positions as tuples that require special handling.
        Searches the board for reflection squares. These are entry squares adjacent to an atom."""
        for a in self._atom_on_grid_edge:
            # handles special case corner atoms
            if a == (8, 8):
                self._reflection_squares.add((9, 7))
                self._reflection_squares.add((7, 9))
            elif a == (8, 1):
                self._reflection_squares.add((7, 0))
                self._reflection_squares.add((9, 2))
            elif a == (1, 1):
                self._reflection_squares.add((2, 0))
                self._reflection_squares.add((0, 2))
            elif a == (1, 8):
                self._reflection_squares.add((0, 7))
                self._reflection_squares.add((2, 9))
                # handles regular reflections
            if a[0] == 1:  # handling of top horizontal edge
                self._reflection_squares.add((a[0] - 1, a[1] + 1))  # add square to right of atom
                self._reflection_squares.add((a[0] - 1, a[1] - 1))  # add square to left of atom
            elif a[0] == 8:  # handling of bottom horizontal edge
                self._reflection_squares.add((a[0] + 1, a[1] + 1))  # add square to right of atom
                self._reflection_squares.add((a[0] + 1, a[1] - 1))  # add square to left of atom
            elif a[1] == 1:  # handling of right and left column edges
                self._reflection_squares.add((a[0] + 1, a[1] - 1))  # add square below atom
                self._reflection_squares.add((a[0] - 1, a[1] - 1))  # add square above atom
            elif a[1] == 8:
                self._reflection_squares.add((a[0] + 1, a[1] + 1))  # add square below atom
                self._reflection_squares.add((a[0] - 1, a[1] + 1))  # add square above atom

    def guess_atom(self, row, column):
        """Takes as parameters a row and column.
        If there is an atom at that location, will return True, otherwise will return False.
        The player's score will be adjusted accordingly by calling set_score within Player class object.
        The found_atom method within Board object will be called to mark atom as found."""
        positions = self._board.get_atoms()
        position = (row, column)
        for atom in positions:  # iterates through list of atoms
            if position == atom:  # looks for a match
                self._player.set_guess(position)
                self.found_atom(position)  # marks atom as found
                return True
        else:
            if position not in self._player.get_guess():
                self._player.set_guess(position)
                self._player.set_score('miss')  # adjusts score for a miss
                return False
            else:
                return False

    def get_score(self):
        """Returns the current score from Player class object from it's get_score() method."""
        return self._player.get_score()

    def found_atom(self, atom):
        """Takes in atom, and marks specified atom value as found in dictionary stored within datamember _atoms_left.
        This method is called when guess_atom() method from BlackBoxGame class matches an atom position"""
        self._atoms_left[atom] = 'found'

    def atoms_left(self):
        """Returns the number of atoms remaining (not hit) from Board class object's get_atoms method by iterating
        through dictionary values and counting how many hold value 'remaining'. Returns integer with count."""
        count = 0
        for atom in self._atoms_left.values():
            if atom == 'remaining':
                count += 1
        return count

    def print_board(self):
        """Retrieves/prints current board from Board class object get_board() method."""
        for i in range(len(self._board.get_board())):
            print(self._board.get_board()[i])


class Player:
    """Creates Player class object for tracking player score. Methods within BlackBoxGame will rely/interact with
    methods within Player class object to get/set player score, keep track of previous guesses/entry/exit so that
    repeat guesses are not allowed and not penalized multiple times."""

    def __init__(self):
        """Initializes datamembers for player _score, previous _entry_exit, and _guess. _score holds current score.
        _entry_exit is a set that holds used entry/exits. _guess holds set of previously guessed positions."""
        self._score = 25
        self._entry_exit = set()
        self._guess = set()

    def set_score(self, reason):
        """Sets score, takes in a reason and adjusts the score based on game rules."""
        if reason == 'miss':  # checks for a miss
            self._score -= 5  # 5 points deducted
        if reason == 'entry/exit':  # checks if new entry point
            self._score -= 1  # 1 point deducted

    def get_score(self):
        """Returns the current score from _score datamember."""
        return self._score

    def get_guess(self):
        """Returns list of tuples that have already been guessed/targeted from _guess datamember."""
        return self._guess

    def set_guess(self, guess):
        """Updates list of player guesses after each guess, takes in a tuple and updates the list _guess datamember."""
        self._guess.add(guess)

    def get_entry_exit(self):
        """Returns list of previous entry/exit points from _entry_exit datamember."""
        return self._entry_exit

    def set_entry_exit(self, position):
        """Updates list of previous entry or exit points, takes in a tuple and updates the list in _entry_exit."""
        if position not in self._entry_exit:    # if new entry/exit point
            self.set_score('entry/exit')        # calls set_score to adjust score
        self._entry_exit.add(position)          # adds position to list of used entry/exits


class Board:
    """Creates Board class object for tracking/managing locations of atoms.
    Methods within BlackBoxGame will interact with Board class object to see state of the game board
    and to set/hit atom positions."""

    def __init__(self, atom_positions):
        """Initializes datamember that builds the game board with a list of lists by list comprehension.
        Takes in a list of atom_positions from BlackBoxGame class and adds atoms to default board layout.
        Atoms will be represented on the board as 'A'. During gameplay the player will not be able to see
        the locations."""
        self._board = [[" " for col in range(10)] for row in range(10)]     # builds board w/ list of lists
        self._atom_positions = atom_positions

    def set_board(self, legal):
        """Modifies default board layout to position atoms into place from _atom_positions datamember, adds visual
        markers of * and X to represent legal entry points and corner positions."""
        corners = [(0, 0), (0, 9), (9, 0), (9, 9)]
        for atom in self._atom_positions:
            self._board[atom[0]][atom[1]] = 'A'     # places visual representation of atom locations on the board
        for l in legal:
            self._board[l[0]][l[1]] = '*'           # places visual representation of legal entry points on the board
        for c in corners:
            self._board[c[0]][c[1]] = 'X'           # places visual representation of illegal entry points on the board

    def get_atoms(self):
        """Returns list of remaining atoms."""
        return self._atom_positions

    def get_board(self):
        """Returns the current game board."""
        return self._board
