from src.constants import *
from src.game_obj import GameObject


class Cannon(GameObject):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 1, 1, 'C', 0)
        self.damage = CANNON_DAMAGE
        self.last_fired = 0
        self.range = CANNON_RANGE
        self.fore = Fore.RESET
