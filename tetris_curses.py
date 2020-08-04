#!/usr/bin/env python3
import curses
from curses import wrapper
from time import time

from board import Board

screen = curses.initscr()
curses.start_color()


class Colors:
    # Background
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
    background = curses.color_pair(8)

    # Orange piece
    curses.init_pair(9, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    orange = curses.color_pair(9)

    # Green piece
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_GREEN)
    green = curses.color_pair(10)

    # Red piece
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_RED)
    red = curses.color_pair(11)

    # Purple piece
    curses.init_pair(12, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    purple = curses.color_pair(12)

    # White piece
    curses.init_pair(13, curses.COLOR_WHITE, curses.COLOR_WHITE)
    white = curses.color_pair(13)

    # Blue piece
    curses.init_pair(14, curses.COLOR_BLUE, curses.COLOR_BLUE)
    blue = curses.color_pair(14)

    # Cyan piece
    curses.init_pair(15, curses.COLOR_CYAN, curses.COLOR_CYAN)
    cyan = curses.color_pair(15)

    # Window border
    curses.init_pair(16, curses.COLOR_WHITE, curses.COLOR_BLACK)
    border = curses.color_pair(16)

    # Error
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    warn = curses.color_pair(1)


def main(screen, board_size=(20, 10)):
    # Create board object
    board = Board(board_size)

    # Update delay (gets 1% faster every 10 rows cleared)
    update_delay = 1

    # Debugging log
    log = []

    # Get terminal size
    num_rows, num_cols = screen.getmaxyx()

    # Define center of board
    board_center = (num_rows // 2, num_cols // 2)

    # Disable cursor
    curses.curs_set(0)

    # Set window timeout for keyboard input
    screen.nodelay(True)

    # Sides of the board border
    board_left = board_center[1] - board.width - 1
    board_right = board_center[1] + board.width + 1
    board_top = board_center[0] - (board.height // 2) - 1
    board_bottom = board_top + board.height + 1

    # Initial board update to summon first piece
    log_message = board.update()
    if len(log_message) > 0:
        log.insert(0, log_message)

    update_start_time = time()

    # Game loop
    while True:
        # Render board border
        screen.addstr(board_top, board_left, '╔' + 2 * board.width * '═' + '╗', Colors.border)
        for row in range(board_top + 1, board_bottom):
            screen.addstr(row, board_left, '║' + 2 * board.width * ' ' + '║', Colors.border)
        screen.addstr(board_bottom, board_left, '╚' + 2 * board.width * '═' + '╝', Colors.border)

        # Render board tiles
        for row in range(board.height):
            for col in range(board.width):
                screen.addstr(board_top + row + 1, board_left + (2 * col) + 1, 2 * '■', eval(f'Colors.{board.colors[board[row][col]]}'))

        # Render log
        for row in range(num_rows):
            screen.addstr(row, 0, (board_left - 1) * ' ', Colors.background)
        for i, message in enumerate(log):
            if i >= num_rows:
                break
            screen.addstr(i, 0, message[:board_left - 1])

        screen.refresh()

        # Process keypresses
        key = screen.getch()
        if key != -1:
            if key == ord('q'):
                break
            elif key in [97, 104, 260, 258, 259, 261, 100, 115, 119, 106, 107, 108]:
                log_message = board.move(key)
                log.insert(0, f'Key pressed: {key}')
                log.insert(0, log_message)
                screen.addstr(num_rows - 1, num_cols // 2, ((num_cols // 2) - 1) * ' ', Colors.background)
            else:
                warning = f'UNKOWN KEY: {key}'
                log.insert(0, warning)
                screen.addstr(num_rows - 1, num_cols - 1 - len(warning), warning, Colors.warn | curses.A_BOLD | curses.A_UNDERLINE | curses.A_BLINK)

            # Render board tiles
            for row in range(board.height):
                for col in range(board.width):
                    screen.addstr(board_top + row + 1, board_left + (2 * col) + 1, 2 * '■', eval(f'Colors.{board.colors[board[row][col]]}'))
            screen.refresh()

        # Update the board and lower piece if it's been long enough
        if time() - update_start_time >= update_delay:
            log_message = board.update()
            if len(log_message) > 0:
                log.insert(0, log_message)
            update_start_time = time()

        # Retry or quit when the game ends
        if board.game_over:
            log.insert(0, f'Game over, score {board.score}')
            # Render log
            for row in range(num_rows):
                screen.addstr(row, 0, (board_left - 1) * ' ', Colors.background)
            for i, message in enumerate(log):
                if i >= num_rows:
                    break
                screen.addstr(i, 0, message[:board_left - 1])

            # Wait for user to hit "r" (retry) or "q" (quit)
            screen.nodelay(False)
            key = screen.getch()
            if key == ord('q'):
                break
            elif key == ord('r'):
                board = Board(board_size)
                screen.nodelay(True)

    curses.endwin()


if __name__ == '__main__':
    wrapper(main)
