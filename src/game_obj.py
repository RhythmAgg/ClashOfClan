import numpy as np
from colorama import Fore, Back, Style

from src.constants import HEALTH_RANGE, OBJECT_COLOUR


class GameObject:
    def __init__(self, pos_x, pos_y, width, height, ch, health):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._height = height
        self._width = width
        self._object = np.array([[ch for j in range(width)] for i in range(height)], dtype='object')
        self._health = health
        self._max_health = health
        self._last_move = [0, 0]
        self.fore = Fore.GREEN
        self.back = Back.RESET
        self.style = Style.NORMAL


    def get_position(self):
        return self._pos_x, self._pos_y

    def set_position(self, pos_x, pos_y):
        self._pos_x, self._pos_y = pos_x, pos_y

    def get_dim(self):
        return self._width, self._height

    def get_health(self):
        return self._health

    def deal_damage(self, damage):
        self._health -= damage
        for i in range(len(HEALTH_RANGE)):                     
            if self._health <= HEALTH_RANGE[i]:
                self.fore = OBJECT_COLOUR[i]
                break

    def set_last_move(self, move_x=0, move_y=0):
        self._last_move = [move_x, move_y]

    def undo_last_move(self):
        self._pos_x -= self._last_move[0]
        self._pos_y -= self._last_move[1]

    def heal(self, inc):
        self._health = min(self._health + inc, self._max_health)
