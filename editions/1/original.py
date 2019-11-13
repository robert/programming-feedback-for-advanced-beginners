## This code is made available under the Creative Commons Zero 1.0 License (https://creativecommons.org/publicdomain/zero/1.0)

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:40:33 2019

"""

from random import randint


class Board:
    """
    Class defining a tic-tac-toe board and associated methods
    """

    def __init__(self, dim=3, num_players=2):
        self.num_players = num_players
        if dim > 9:
            raise ValueError("Board too big")
        self.dim = dim
        self.board = [[None for i in range(0, self.dim)] for j in range(0, self.dim)]
        self.players = ["X", "O"] + [chr(i) for i in range(65, 90)]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        """
        print a board in this form:
              1 2 3
              ------
            1 - X O
            2 X - O
            3 X - O
        """
        return_string = (
            " "
            + "".join([str(i).rjust(2, " ") for i in range(1, len(self.board[0]) + 1)])
            + "\n"
        )
        return_string = return_string + "--" * (len(self.board[0]) + 1) + "\n"
        i = 1
        for row in self.board:
            return_string = return_string + str(i) + ":"
            for item in row:
                if item is not None:
                    return_string = return_string + self.players[item] + " "
                else:
                    return_string = return_string + "- "
            return_string = return_string + "\n"
            i = i + 1
        return return_string

    def random_board(self, fill_level=0):
        """
        returns a correcty filled board with fill_level fields
        filled 
        """
        if fill_level == 0:
            fill_level = self.dim ** 2
        if fill_level > self.dim ** 2:
            raise ValueError("fill_level too high")
        self.board = [[None for i in range(0, self.dim)] for j in range(0, self.dim)]
        player = 0
        for _ in range(0, fill_level):
            pos = self.get_move_random_position()
            self.update(pos, player)
            player = (player + 1) % self.num_players
        return self

    def flatten(self):
        """
        returns a 1d array of the board
        """
        flattened = []
        for row in self.board:
            flattened = flattened + row
        return flattened

    def reshape(self, flattened):
        """
        reshapes a 1d array to a rectangular board
        """
        self.board = [
            flattened[i : i + self.dim] for i in range(0, len(flattened), self.dim)
        ]

    def update(self, coord, player):
        """
        Sets a position on a board for a player. No check if position is legal 
        done at this point
        """
        #        new_board = self.board
        x_coord = coord[0] - 1
        y_coord = coord[1] - 1
        if self.board[x_coord][y_coord] is None:
            self.board[x_coord][y_coord] = player
        #            self.board = new_board
        else:
            raise ValueError("position already filled")

    def valid_move(self, coord):
        """
        Returns True if the move is valid (i.e. position not yet blocked
        and coordinates not out of range)
        """
        x_coord = coord[0] - 1
        y_coord = coord[1] - 1
        try:
            valid_move = self.board[x_coord][y_coord] is None
        except IndexError:
            valid_move = False
        return valid_move

    def winner(self):
        """
        Decide whether there is a winner on the current board.
        Currently this only works for 3x3 boards
        """
        if self.dim != 3:
            raise ValueError("winner not implemented for dimensions other than 3")
        rows_and_cols = (
            [[self.board[i][j] for i in range(0, 3)] for j in range(0, 3)]
            + [[self.board[j][i] for i in range(0, 3)] for j in range(0, 3)]
            + [[self.board[i][i] for i in range(0, 3)]]
            + [[self.board[2 - i][i] for i in range(0, 3)]]
        )
        for row in rows_and_cols:
            winner = (len(set(row)) == 1) and (row[0] is not None)
            if winner:
                winning_player = self.players[row[0]]
                return winning_player
        if None in self.flatten():
            return None
        return "Draw"

    def get_move_user_input(self, player):
        print(self.__repr__())
        input_string = input(f"{self.players[player]}: ")
        x_coord, y_coord = int(input_string[0]), int(input_string[1])
        return x_coord, y_coord

    def get_move_random_position(self, player=0):
        """
        Find a random open position and return it.
        First count all None's, then find a random one in the board
        """
        legal_moves = self.get_all_legal_moves()
        if len(legal_moves) == 0:
            return None
        pos = randint(0, len(legal_moves) - 1)
        return legal_moves[pos]

    def get_move_heuristic_1(self, player=0):
        """
        Check if center position is empty, if yes, take it
        """
        x_coord = int((self.dim + 1) // 2)
        y_coord = int((self.dim + 1) // 2)
        if self.valid_move((x_coord, y_coord)):
            return x_coord, y_coord
        return self.get_move_random_position()

    def get_move_heuristic_2(self, player=0):
        """
        Check if center position is empty, otherwise put weights on
        corners and choose best corner
        """
        x_coord = int((self.dim + 1) // 2)
        y_coord = int((self.dim + 1) // 2)
        if self.valid_move((x_coord, y_coord)):
            return x_coord, y_coord
        corners = [(1, 1), (3, 1), (1, 3), (3, 3)]
        free_corners = {}

        for corner in corners:
            free_corners[corner] = 1 * self.valid_move(corner)

        # calculate weights by looking if adjacent corners are also empty
        if sum(free_corners.values()) > 0:
            weights = {}
            weights[(3, 3)] = free_corners[(3, 3)] * (
                1 + free_corners[(3, 1)] + free_corners[(1, 3)]
            )
            weights[(1, 1)] = free_corners[(1, 1)] * (
                1 + free_corners[(3, 1)] + free_corners[(1, 3)]
            )
            weights[(3, 1)] = free_corners[(3, 1)] * (
                1 + free_corners[(1, 1)] + free_corners[(3, 3)]
            )
            weights[(1, 3)] = free_corners[(1, 3)] * (
                1 + free_corners[(1, 1)] + free_corners[(3, 3)]
            )
            max_value = max(weights.values())
            best_corner = list(weights.keys())[list(weights.values()).index(max_value)]
            return best_corner
        return self.get_move_random_position()

    def find_two_in_row(self, player):
        rows_and_cols_idx = (
            [[(i, j) for i in range(0, 3)] for j in range(0, 3)]
            + [[(j, i) for i in range(0, 3)] for j in range(0, 3)]
            + [[(i, i) for i in range(0, 3)]]
            + [[(2 - i, i) for i in range(0, 3)]]
        )

        for pairs in rows_and_cols_idx:
            row = [self.board[c[0]][c[1]] for c in pairs]
            if row.count(player) == 2 and (None in row):
                ret_val = pairs[row.index(None)]
                return ret_val[0] + 1, ret_val[1] + 1
        return None

    def get_move_heuristic_3(self, player):
        """
        Check if there is a winning move, then if there is a loosing move,
        finally choose a random move
        """
        if self.dim != 3:
            raise ValueError(
                "get_move_heuristic_3 not implemented for dimensions other than 3"
            )

        # check for winning move
        move = self.find_two_in_row(player)
        if move is not None:
            #            print("found winning: ", move)
            return move

        # check for losing move
        #        print("checking for losing")
        move = self.find_two_in_row(1 - player)
        if move is not None:
            #            print(move)
            return move
        return self.get_move_random_position(player)

    def get_move_heuristic_4(self, player):
        """
        Check if there is a winning move, then if there is a loosing move,
        finally use heuristic 2 as a fallback
        """
        if self.dim != 3:
            raise ValueError(
                "get_move_heuristic_3 not implemented for dimensions other than 3"
            )

        # check for winning move
        move = self.find_two_in_row(player)
        if move is not None:
            #            print("found winning: ", move)
            return move

        # check for losing move
        #        print("checking for losing")
        move = self.find_two_in_row(1 - player)
        if move is not None:
            #            print(move)
            return move
        return self.get_move_heuristic_2(player)

    def get_all_legal_moves(self):
        flt_board = self.flatten()
        none_count = flt_board.count(None)
        if none_count == 0:
            return None
        x_coord, y_coord = 1, 1
        # walk through the board, count None's and stop at pos-th None
        # to get its coordinate
        legal_moves = []
        for row in self.board:
            for item in row:
                if item is None:
                    legal_moves.append((x_coord, y_coord))
                y_coord = (y_coord % self.dim) + 1
            x_coord = (x_coord % self.dim) + 1
        return legal_moves

    def get_move_minmax(self, player):
#        moves = self.get_legal_moves()
#        scores = []
#        for move in moves:
#            saved_board = self.board
#            self.update(move, player)
#            winner = self.winner()
#            if winner is None:
#                return 0
#            if winner == player:
#                return 10
#            else:
#                return -10
#            
        return self.get_move_random_position(player)

def play_games(player_1, player_2, rounds=1):
    players = {0: player_1, 1: player_2}
    stats = {"X": 0, "O": 0, "Draw": 0}

    for _ in range(rounds):
        board = Board()
        # randomize which player starts
        active_player = randint(0, 1)
        #        active_player = 0
        while board.winner() is None:
#            print(board)
            coords = players[active_player](board, active_player)
            board.update(coords, active_player)
            active_player = 1 - active_player
        stats[board.winner()] += 1
#        print("Winner: ", board.winner())
    ratio = stats["X"] / sum(stats.values())
    return ratio


if __name__ == "__main__":
    result = play_games(Board.get_move_minmax, Board.get_move_minmax, rounds=100)
    print(f"{100*result:10.1f}", end="")

