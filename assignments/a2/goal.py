"""CSC148 Assignment 2

CSC148 Winter 2024
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
Jaisie Sin, and Joonho Kim

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, Jaisie Sin, and Joonho Kim

Module Description:

This file contains the hierarchy of Goal classes and related helper functions.
"""
from __future__ import annotations
import random
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> list[Goal]:
    """Return a randomly generated list of goals with length <num_goals>.

    Each goal must be randomly selected from the two types of Goals provided
    and must have a different randomly generated colour from COLOUR_LIST.
    No two goals can have the same colour.

    Preconditions:
    - num_goals <= len(COLOUR_LIST)
    """
    #  Implement this function
    goals = []
    color_lst = COLOUR_LIST.copy()
    for _ in range(num_goals):
        colour = random.choice(color_lst)
        color_lst.remove(colour)
        goal_types = [PerimeterGoal(colour), BlobGoal(colour)]
        goals.append(random.choice(goal_types))
    return goals


def flatten(block: Block) -> list[list[tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j].

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    # Implement this function
    rslt = []
    if block.level == block.max_depth:
        return [[block.colour]]
    else:
        block_cpy = block.create_copy()
        block_cpy.smash_same_color()
        left_up = flatten(block_cpy.children[1])
        right_up = flatten(block_cpy.children[0])
        left_down = flatten(block_cpy.children[2])
        right_down = flatten(block_cpy.children[3])
        # extend each column of left_up with each column of left_down
        # extend each column of right_up with each column of right_down
        n = 2 ** (block_cpy.max_depth - block_cpy.level)
        for i in range(n // 2):
            rslt.append(left_up[i] + left_down[i])

        for i in range(n // 2):
            rslt.append(right_up[i] + right_down[i])
    return rslt


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    Instance Attributes:
    - colour: The target colour for this goal, that is the colour to which
              this goal applies.
    """
    colour: tuple[int, int, int]

    def __init__(self, target_colour: tuple[int, int, int]) -> None:
        """Initialize this goal to have the given <target_colour>.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given <board>.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A goal to maximize the presence of this goal's target colour
    on the board's perimeter.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.

        The score for a PerimeterGoal is defined to be the number of unit cells
        on the perimeter whose colour is this goal's target colour. Corner cells
        count twice toward the score.
        """
        #  Implement this method
        flat_board = flatten(board)
        size = 2 ** (board.max_depth - board.level)
        score = 0
        for i in range(size):
            for j in range(size):
                # check if the cell is on the perimeter
                is_on_perimeter = (i == 0 or i == size - 1 or j == 0
                                   or j == size - 1)
                if is_on_perimeter and flat_board[i][j] == self.colour:
                    # check if the cell is a corner cell
                    is_corner = ((i == 0 and j == 0) or (i == 0
                                                         and j == size - 1)
                                 or (i == size - 1 and j == 0)
                                 or (i == size - 1 and j == size - 1))
                    score += 2 if is_corner else 1

        return score

    def description(self) -> str:
        """Return a description of this goal.
        """
        # Implement this method
        return f'Perimeter Goal: {colour_name(self.colour)}'


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.

        The score for a BlobGoal is defined to be the total number of
        unit cells in the largest connected blob within this Block.
        """
        # Implement this method
        flat_board = flatten(board)
        visited = [[-1 for _ in range(2 ** (board.max_depth - board.level))]
                   for _ in range(2 ** (board.max_depth - board.level))]
        max_size = 0
        for i in range(2 ** (board.max_depth - board.level)):
            for j in range(2 ** (board.max_depth - board.level)):
                if visited[i][j] == -1:
                    size = self._undiscovered_blob_size((i, j), flat_board,
                                                        visited)
                    max_size = max(max_size, size)
        return max_size

    def _undiscovered_blob_size(self, pos: tuple[int, int],
                                board: list[list[tuple[int, int, int]]],
                                visited: list[list[int]]) -> int:
        """Return the size of the largest connected blob in <board> that (a) is
        of this Goal's target <colour>, (b) includes the cell at <pos>, and (c)
        involves only cells that are not in <visited>.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure (to <board>) that, in each cell,
        contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.

        If <pos> is out of bounds for <board>, return 0.
        """
        # Implement this method
        size = 0
        #  check if the cell is out of bounds
        if pos[0] < 0 or pos[0] >= len(board) or pos[1] < 0 or pos[1] >= len(
                board):
            return 0
        # check if the cell is visited
        if visited[pos[0]][pos[1]] == 1:
            return 0

        # check if the cell is not of the target colour
        visited[pos[0]][pos[1]] = 1
        if board[pos[0]][pos[1]] == self.colour:
            size += 1
            size += self._undiscovered_blob_size((pos[0] - 1, pos[1]), board,
                                                 visited)
            size += self._undiscovered_blob_size((pos[0] + 1, pos[1]), board,
                                                 visited)
            size += self._undiscovered_blob_size((pos[0], pos[1] - 1), board,
                                                 visited)
            size += self._undiscovered_blob_size((pos[0], pos[1] + 1), board,
                                                 visited)
        return size

    def description(self) -> str:
        """Return a description of this goal.
        """
        # Implement this method
        return f'Blob Goal: {colour_name(self.colour)}'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
