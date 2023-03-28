from src.constants import *
from src.game_obj import GameObject


class Barbarian(GameObject):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 1, 1, 'B', BARB_MAX_HEALTH)
        self.damage = BARB_DAMAGE
        self.last_attack_time = 0

    def move(self, x, y):
        self._pos_x += x
        self._pos_y += y
        self.set_last_move(x, y)
