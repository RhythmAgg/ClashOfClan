import string
import sys
import termios
from random import choice
from select import select

from colorama import Back

from src.constants import SCREEN_WIDTH, GAME_ID_LEN


def getch():
    return sys.stdin.read(1)


def key_press():
    dr, dw, de = select([sys.stdin], [], [], 0)
    return dr != []


def flush():
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def check_collision(obj1, obj2):
    pos_x1, pos_y1 = obj1.get_position()
    width1, height1 = obj1.get_dim()

    pos_x2, pos_y2 = obj2.get_position()
    width2, height2 = obj2.get_dim()

    collision_x = pos_x1 + height1 > pos_x2 and pos_x2 + height2 > pos_x1
    collision_y = pos_y1 + width1 > pos_y2 and pos_y2 + width2 > pos_y1

    return collision_x and collision_y


def get_distance(obj1, obj2):
    pos_x1, pos_y1 = obj1.get_position()
    width1, height1 = obj1.get_dim()

    pos_x2, pos_y2 = obj2.get_position()
    width2, height2 = obj2.get_dim()

    dx = 0
    if pos_x1 + height1 < pos_x2:
        dx = pos_x2 - (pos_x1 + height1)
    if pos_x2 + height2 < pos_x1:
        dx = pos_x1 - (pos_x2 + height2)

    dy = 0
    if pos_y1 + width1 < pos_y2:
        dy = pos_y2 - (pos_y1 + width1)
    if pos_y2 + width2 < pos_y1:
        dy = pos_y1 - (pos_y2 + width2)

    return dx + dy

def progress_bar(val, max_val, num_div):
    num_filled = int((val / max_val) * num_div) + 1
    num_filled = min(num_filled, num_div)

    filled = ' ' * num_filled
    empty = ' ' * (num_div - num_filled)

    res = Back.LIGHTCYAN_EX + filled + Back.RESET + empty
    return res

def print_centered(text):
    num_space = int((SCREEN_WIDTH - len(text)) / 2)
    for _ in range(num_space):
        print(' ', end='')
    print(text)
    # for _ in range(num_space):
    #     print(' ', end='')

def gen_game_id():
    return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(GAME_ID_LEN))

def filename_by_id(id):
    return 'replay-' + id + ".txt"