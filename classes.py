import numpy as np
import random
from copy import deepcopy

class Environment:
    def __init__(self, size=8, probability=0.2, start_point=None, end_point=None, seed=None,
                good_square=-1, bad_square=-5, end_square=10):

        self._size = size
        self._probability = probability
        self._seed = seed
        self._is_done = False
        self._agent_won = None

        # rewards for each type of square
        self._good_square = good_square
        self._bad_square = bad_square
        self._end_square = end_square

        if seed:
            random.seed(seed)

        if not start_point:
            start_point = self.random_coordinates(exclude=[end_point])
        if not end_point:
            end_point = self.random_coordinates(exclude=[start_point])
        self._start_point = start_point
        self._end_point = end_point

        self._board = self.generate_correct_board()
        self._board[self._end_point] = self._end_square # assign reward to end point

        self._agent_coordinates = self._start_point

    def random_coordinates(self, exclude=None):
        """
        Returns random coordinates from within the board
        exclude : list (optional)
            list of points that cannot be returned
        """
        if not exclude:
            exclude = []

        x = random.randint(0, self._size-1)
        y = random.randint(0, self._size-1)

        while (x, y) in exclude:
            x = random.randint(0, self._size-1)
            y = random.randint(0, self._size-1)

        return (x, y)

    def generate_board(self):
        size = self._size
        board = np.full((size, size), self._good_square)

        for i in range(self._size):
            for j in range(self._size):
                if random.random() < self._probability:
                    board[i][j] = self._bad_square

        board[self._start_point] = self._good_square
        board[self._end_point] = self._good_square
        return board

    def generate_correct_board(self):
        """
        Ensures that generated board is correct
        (path between start and end exists)
        Tries 500 times
        """
        for _ in range(500):
            board = self.generate_board()
            if self.find_path_dfs(board):
                return board

    def neighbours(self, coordinates):
        neighbours = []
        x = coordinates[0]
        y = coordinates[1]

        # up
        if x != 0:
            neighbours.append((x-1, y))
        # right
        if y != self._size - 1:
            neighbours.append((x, y+1))
        # down
        if x != self._size - 1:
            neighbours.append((x+1, y))
        # left
        if y != 0:
            neighbours.append((x, y-1))

        return neighbours

    def find_path_dfs(self, board):
        visited = []
        coordinates = self._start_point
        return self._find_path_dfs(coordinates, board, visited)

    def _find_path_dfs(self, coordinates, board, visited):
        """
        This recursive function should not be called by user
        """
        visited.append(coordinates)

        if coordinates == self._end_point:
            return True     # end point reached, path found

        for neighbour in self.neighbours(coordinates):
            if board[neighbour] == self._bad_square or neighbour in visited:
                continue

            path_found = self._find_path_dfs(neighbour, board, visited)
            if path_found:
                return True

        return False

    def state(self):
        """
        'Flattens' board to one dimension and returns
        agent's location as one number
        """
        x = self._agent_coordinates[0]
        y = self._agent_coordinates[1]
        return x * self._size + y

    def reset(self):
        """
        Prepares to new episode
        """
        self._agent_coordinates = self._start_point
        self._agent_won = None
        self._is_done = False

    def step(self, action):
        """
        Performs given action. Is is assumpted that action is available
        action : int
            0: up, 1: right, 2: down, 3: left
        Returns: new state, reward, done
        """
        x = self._agent_coordinates[0]
        y = self._agent_coordinates[1]

        if action == 0:
            new_coordinates = (x-1, y)
        elif action == 1:
            new_coordinates = (x, y+1)
        elif action == 2:
            new_coordinates = (x+1, y)
        else:
            new_coordinates = (x, y-1)

        self._agent_coordinates = new_coordinates
        reward = self._board[new_coordinates]

        if reward == self._bad_square:
            self._is_done = True
            self._agent_won = False
        elif reward == self._end_square:
            self._is_done = True
            self._agent_won = True

        return self.state(), reward, self._is_done

    def available_actions(self):
        actions = []
        x = self._agent_coordinates[0]
        y = self._agent_coordinates[1]

        # up
        if x != 0:
            actions.append(0)
        # right
        if y != self._size - 1:
            actions.append(1)
        # down
        if x != self._size - 1:
            actions.append(2)
        # left
        if y != 0:
            actions.append(3)

        return actions

    def space(self):
        return pow(self._size, 2)


    def __str__(self):
        return str(self._board)

    def get_start(self):
        return self._start_point

    def get_end(self):
        return self._end_point

    def get_board(self):
        return self._board

    def get_size(self):
        return self._size

    def get_agent_won(self):
        return self._agent_won