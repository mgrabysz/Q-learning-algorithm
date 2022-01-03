import numpy as np
import random
from copy import deepcopy

class Environment:
    def __init__(self, size=8, probability=0.2, start_point=None, end_point=None, seed=None):

        self._size = size
        self._probability = probability
        self._seed = seed

        if seed:
            random.seed(seed)

        if not start_point:
            start_point = self.random_coordinates(exclude=[end_point])
        if not end_point:
            end_point = self.random_coordinates(exclude=[start_point])
        self._start_point = start_point
        self._end_point = end_point

        is_board_correct = False
        while not is_board_correct:
            board = self.generate_board()
            is_board_correct = self.find_path_dfs(board)
            print(board)

        self._board = board
        self._board[self._end_point] = 10

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
        board = np.zeros((size, size))

        for i in range(self._size):
            for j in range(self._size):
                if random.random() < self._probability:
                    board[i][j] = -1

        board[self._start_point] = 0
        board[self._end_point] = 0
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
            if board[neighbour] == -1 or neighbour in visited:
                continue

            path_found = self._find_path_dfs(neighbour, board, visited)
            if path_found:
                return True

        return False


    def __str__(self):
        return str(self._board)

    def check_accessibility(self, board):

        dRow = [0, 1, 0, -1]
        dCol = [-1, 0, 1, 0]

        vis = [[False for i in range(self._size)] for j in range(self._size)]
        st = []
        st.append(self.get_start())

        while (len(st) > 0):
            curr = st[len(st) - 1]
            st.remove(st[len(st) - 1])
            row = curr[0]
            col = curr[1]

            if (self.check_validity(vis, curr, board) == False):
                continue
            vis[row][col] = True

            for i in range(4):
                adjx = row + dRow[i]
                adjy = col + dCol[i]
                st.append([adjx, adjy])
        if(vis[self._end[0]][self._end[1]] is True):
            return True
        return False


    def check_validity(self, visited, field, board):
        size = self._size
        if (field[0] < 0 or field[1] < 0 or field[0] >= size or field[1] >= size):
            return False

        if (visited[field[0]][field[1]]):
                return False

        if(board[field[0]][field[1]] == '|'):
            return False

        return True


    def print_board(self):
        first_row = [i for i in range(self._size)]
        print("    ", '   '.join(map(str, first_row)))
        print()
        for i in range(len(self._board)):
            print(i,"  ", '   '.join(self._board[i]))
        # print(self._board)

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_board(self):
        return self._board

    def get_size(self):
        return self._size

    def update_field(self, field, character):
        self._board[field[0]][field[1]] = character


class Player():
    def __init__(self, board, if_random):
        self._board = board
        self._current_pos = board.get_start()
        self._neighbours = self.get_neighbours()
        self._if_random = if_random

    def update_neighbours(self):
        self._neighbours = self.get_neighbours()

    def get_neighbours(self):
        neighbours = []
        neighbours.append([self._current_pos[0], self._current_pos[1]-1])
        neighbours.append([self._current_pos[0]-1, self._current_pos[1]])
        neighbours.append([self._current_pos[0]+1, self._current_pos[1]])
        neighbours.append([self._current_pos[0], self._current_pos[1]+1])
        return neighbours

    def check_win(self, next_move):
        if(self._board.get_end() == next_move):
            return True
        else:
            return False

    def next_move(self):
        if(self._if_random):
            next_move = random.choice(self._neighbours)
            if(self.check_move_valid(next_move)):
                if(self.check_win(next_move)):
                    self._board.update_field(self._current_pos, 'V')
                    self._current_pos = next_move
                    self._board.update_field(self._current_pos, 'W')
                    print("Zwycięztwo")
                    print(next_move)
                    return False
                else:
                    self._board.update_field(self._current_pos, 'V')
                    self._current_pos = next_move
                    self._board.update_field(self._current_pos, 'R')
                    self.update_neighbours()
                    return True
            else:
                if(self.check_out_of_board(next_move)):
                    self._board.update_field(self._current_pos, 'C')
                else:
                    self._board.update_field(self._current_pos, 'V')
                    self._current_pos = next_move
                    self._board.update_field(self._current_pos, 'C')
                print("Porażka")
                print(next_move)
                return False

    def check_out_of_board(self, next_move):
        size = self._board.get_size()
        if(next_move[0] > size-1 or next_move[0] < 0 or next_move[1] > size-1 or next_move[1] < 0):
            return True
        else:
            return False

    def check_move_valid(self, next_move):
        if(self.check_out_of_board(next_move)):
            return False
        elif(self._board.get_board()[next_move[0]][next_move[1]] == '|'):
            return False
        else:
            return True

    def game(self):
        still_playing = True
        round_counter = 0
        while(still_playing):
            still_playing = self.next_move()
            round_counter += 1
        self._board.print_board()
