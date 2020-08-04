#!/usr/bin/env python3
from random import randint

import numpy as np


class BoardSizeTooSmall(Exception):
    pass


class Board:
    def __init__(self, size=(20, 10)):
        """
        Params:
            size (tuple): (height, width)
        """
        self.size = (int(size[0]), int(size[1]))
        self.height, self.width = self.size

        if self.height < 4 or self.width < 4:
            raise BoardSizeTooSmall('Board needs to be 4x4 minimum')

        self.grid = np.zeros(self.size, dtype=np.uint8)
        self.colors = {0: 'background',
                       1: 'cyan',  # I piece
                       2: 'blue',  # J piece
                       3: 'orange',  # L piece
                       4: 'white',  # O piece
                       5: 'green',  # S piece
                       6: 'purple',  # T piece
                       7: 'red'}  # Z piece
        # self.current_piece = {'value': randint(1, 7),
        self.current_piece = {'value': 0,
                              'coords': []}
        self.held_piece = 0
        # self.next_piece = randint(1, 7)
        self.next_piece = 1
        self.score = 0
        self.game_over = False

        # for row in range(self.height):
        #     for col in range(self.width):
        #         self.grid[row][col] = randint(0, 7)

    def move(self, keycode):
        return_message = ''

        if not self.game_over:
            # Move left/right
            if keycode in [97, 104, 260, 100, 108, 261]:  # 'a', 'h', left, 'd', 'l', down
                # Generate next coords
                next_coords = [c.copy() for c in self.current_piece['coords']]
                for i in range(len(next_coords)):
                    # For moving left
                    if keycode in [97, 104, 260]:
                        next_coords[i][1] -= 1
                    # For moving right
                    else:
                        next_coords[i][1] += 1

                # Check if next coords are open
                next_coords_blocked = False
                for c in next_coords:
                    # Check if move is blocked by a wall
                    if c[1] < 0 or c[1] >= self.width:
                        next_coords_blocked = True
                        return_message = f'Move blocked by wall {self.current_piece["coords"]}'
                        break
                    # Only check new spaces, see if move is blocked by a piece
                    if [c[0], c[1]] not in self.current_piece['coords']:
                        if self.grid[c[0]][c[1]] != 0:
                            next_coords_blocked = True
                            return_message = 'Move blocked by piece'
                            break

                # If coords aren't blocked, move the piece left to next_coords
                if not next_coords_blocked:
                    # Delete old piece
                    for c in self.current_piece['coords']:
                        self.grid[c[0]][c[1]] = 0
                    # Overwrite coords
                    self.current_piece['coords'] = next_coords.copy()
                    # Place new piece
                    for c in self.current_piece['coords']:
                        self.grid[c[0]][c[1]] = self.current_piece['value']
                    return_message = f'Piece moved left to {self.current_piece["coords"]}'

        return return_message

    def update(self):
        return_message = ''

        if not self.game_over:
            # Bring up next next
            if self.current_piece['value'] == 0:
                self.current_piece = {'value': self.next_piece, 'coords': []}
                # self.next_piece = randint(1, 7)
                self.next_piece = 1

                # Generate spawn location for piece and check if open
                if self.current_piece['value'] == 1:
                    left = self.width // 2 - 2
                    right = self.width // 2 + 1
                    if sum(self.grid[0][left:right]) != 0:
                        self.game_over = True
                    else:
                        self.current_piece['coords'] = [[0, left], [0, left + 1], [0, left + 2], [0, left + 3]]

                # Summon the piece
                for coord in self.current_piece['coords']:
                    self.grid[coord[0]][coord[1]] = self.current_piece['value']
                return_message = f'Summoned piece {self.current_piece["value"]} at {self.current_piece["coords"]}'

            # If we didn't just summon a new piece, drop the current piece down 1 row
            else:
                # Generate next coords
                next_coords = [c.copy() for c in self.current_piece['coords']]
                for i in range(len(next_coords)):
                    next_coords[i][0] += 1

                # Check if next coords are open
                next_coords_blocked = False
                for c in next_coords:
                    # Only check new cells
                    if c not in self.current_piece['coords']:
                        if c[0] < self.height:
                            if self.grid[c[0]][c[1]] != 0:
                                next_coords_blocked = True
                                break
                        else:
                            next_coords_blocked = True

                # If coords aren't blocked, move the piece down to next_coords
                if not next_coords_blocked:
                    # Delete old piece
                    for c in self.current_piece['coords']:
                        self.grid[c[0]][c[1]] = 0
                    # Overwrite coords
                    self.current_piece['coords'] = next_coords.copy()
                    # Place new piece
                    for c in self.current_piece['coords']:
                        self.grid[c[0]][c[1]] = self.current_piece['value']
                    return_message = f'Piece moved down to {self.current_piece["coords"]}'

                # Otherwise, set current_piece to 0 to generate a new piece
                else:
                    self.current_piece = {'value': 0, 'coords': []}
                    return_message = 'Piece settled, summoning new piece'

        return return_message

    def __getitem__(self, key):
        return self.grid[key]

    def __str__(self):
        string_grid = ''
        for row in self.grid:
            for cell in row:
                string_grid += str(cell)
            string_grid += '\n'
        return string_grid


if __name__ == '__main__':
    board = Board((15.5, 12.3))

    print(board)
    print(board.update())
    print(board.move(104))
    print(board.move(104))
    print(board.move(104))
    print(board.move(104))
    print(board.move(104))
    print(board.move(104))
    print(board.move(104))
    print(board.move(104))
    print(board.move(104))
    print(board)
