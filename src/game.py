from time import monotonic as clock

import colorama

from src.barbarian import Barbarian
from src.cannon import Cannon
from src.game_obj import GameObject
from src.keyboard import KeyBoard
from src.king import King
from src.screen import Screen
from src.constants import *
from src.utils import *


# TODO:
# Game speed
# Replays

class Game:
    def __init__(self):
        self._width = SCREEN_WIDTH
        self._height = SCREEN_HEIGHT
        self._screen = Screen(self._width, self._height)
        self._game_id = gen_game_id()

        # create game objects
        self._king = King(KING_POS_X, KING_POS_Y)

        townhall = GameObject(TOWNHALL_POS_X, TOWNHALL_POS_Y, TOWNHALL_WIDTH, TOWNHALL_HEIGHT, 'T', TOWNHALL_HITPOINTS)
        self._buildings = [townhall]
        for hut_pos in HUT_POS:
            hut = GameObject(hut_pos[0], hut_pos[1], HUT_WIDTH, HUT_HEIGHT, 'H', HUT_HITPOINTS)
            self._buildings.append(hut)

        self._walls = []
        for wall_pos in WALL_POS:
            wall = GameObject(wall_pos[0], wall_pos[1], 1, 1, '*', WALL_HITPOINTS)
            self._walls.append(wall)

        self._barbarians = []

        self._spawning_points = SPAWN_POINTS

        for i in range(len(SPAWN_POINTS)):
            self._screen.mark_point(SPAWN_POINTS[i][0], SPAWN_POINTS[i][1], MARK_SPAWN[i])

        self._cannons = []
        for cannon_pos in CANNON_POS:
            cannon = Cannon(cannon_pos[0], cannon_pos[1])
            self._cannons.append(cannon)

        self._kb = KeyBoard()

    def render(self):
        frame = 0
        while True:
            start_time = clock()

            self.handle_kb_input()
            self.troops_attack()
            self.cannons_fire()
            self.purge_game_objects()
            self.move_troops()
            self.handle_collisions()
            self._draw_objects()

            while clock() - start_time < TIME_BW_FRAMES:
                pass
            self._screen.display_map(self._king.get_health(), frame, self._game_id)
            # health_bar = progress_bar(self._king.get_health(), KING_MAX_HEALTH, 20)
            # print("Player health: " + health_bar)
            # print("Time played: ", frame)
            # print("Game ID: ", self._game_id)
            frame += 1

    def _draw_objects(self):
        self._screen.clear_map()

        self._screen.add_object(self._king)

        for wall in self._walls:
            self._screen.add_object(wall)

        for building in self._buildings:
            self._screen.add_object(building)

        for barb in self._barbarians:
            self._screen.add_object(barb)

        for cannon in self._cannons:
            self._screen.add_object(cannon)

    def handle_kb_input(self):
        if not key_press():
            return

        ch = getch()

        if ch == 'q':
            self.game_over(False)
        if ch == 'h':
            self.heal()
        if ch in self._king.controls:
            self._king.move(ch)
        if ch == ' ':
            self._king_attack()
        if ch in ['1', '2', '3']:
            ind = int(ch) - 1
            self.spawn_troops(self._spawning_points[ind][0], self._spawning_points[ind][1])

        flush()

    def game_over(self, win):
        print(CLEAR)
        print(RESET_CURSOR)
        for _ in range(int(self._height/2)):
            print('')


        if win:
            print(Fore.GREEN)
            print_centered("You win!")
            print(Fore.RESET)
        else:
            print(Fore.RED)
            print_centered("You Lose!")
            print(Fore.RESET)
        print_centered("Game ID: " + str(self._game_id))

        for _ in range(int(self._height / 2)):
            print('')

        colorama.deinit()
        raise SystemExit

    def handle_collisions(self):
        self._king_collisions()
        self._barbarian_collisions()

    def _king_collisions(self):
        for obj in self._walls:
            if check_collision(self._king, obj):
                self._king.undo_last_move()

        for obj in self._buildings:
            if check_collision(self._king, obj):
                self._king.undo_last_move()

        pos_x, pos_y = self._king.get_position()
        width, height = self._king.get_dim()

        new_pos_x = max(1, min(pos_x, self._height - height - 1))
        new_pos_y = max(1, min(pos_y, self._width - width - 1))
        self._king.set_position(new_pos_x, new_pos_y)

    def _barbarian_collisions(self):
        for barb in self._barbarians:
            for obj in self._walls:
                if check_collision(barb, obj):
                    barb.undo_last_move()
                    if clock() > barb.last_attack_time + BARB_ATTACK_TIMESTEP:
                        barb.last_attack_time = clock()
                        obj.deal_damage(barb.damage)

            for obj in self._buildings:
                if check_collision(barb, obj):
                    barb.undo_last_move()

    def _king_attack(self):
        for obj in self._walls:
            if get_distance(self._king, obj) <= self._king.attack_aoe:
                obj.deal_damage(self._king.damage)

        for obj in self._buildings:
            if get_distance(self._king, obj) <= self._king.attack_aoe:
                obj.deal_damage(self._king.damage)


    # def check_health(self,game_obj):
    #     temp = []
    #     for obj in game_obj:
    #         if obj.get_health() > 0:
    #             temp.append(obj)
    #     return temp
    def purge_game_objects(self):
        if self._king.get_health() <= 0:
            self._king = None

        new_barb = []
        for barb in self._barbarians:
            if barb.get_health() > 0:
                new_barb.append(barb)
        self._barbarians = new_barb

        new_walls = []
        for wall in self._walls:
            if wall.get_health() > 0:
                new_walls.append(wall)
        self._walls = new_walls

        new_buildings = []
        for building in self._buildings:
            if building.get_health() > 0:
                new_buildings.append(building)
        self._buildings = new_buildings

        # self._king = check_health(self._barbarians)

        if self._king is None and len(self._barbarians) == 0:
            self.game_over(False)
        elif len(self._buildings) == 0:
            self.game_over(True)

    def spawn_troops(self, pos_x, pos_y):
        for _ in range(TROOP_SIZE):
            new_barb = Barbarian(pos_x, pos_y)
            self._barbarians.append(new_barb)

    def move_troops(self):
        cur_time = clock()

        for barb in self._barbarians:
            if cur_time < barb.last_attack_time + BARB_ATTACK_TIMESTEP:
                continue

            closest = None
            for building in self._buildings:
                if closest is None:
                    closest = building
                elif get_distance(barb, building) < get_distance(barb, closest):
                    closest = building

            barb_pos_x, barb_pos_y = barb.get_position()
            build_pos_x, build_pos_y = closest.get_position()
            width, height = closest.get_dim()

            x = 0
            if barb_pos_x < build_pos_x:
                x = 1
            elif barb_pos_x > build_pos_x + height:
                x = -1

            y = 0
            if barb_pos_y < build_pos_y:
                y = 1
            elif barb_pos_y > build_pos_y + width:
                y = -1
            barb.move(x, y)

    def troops_attack(self):
        cur_time = clock()

        for barb in self._barbarians:
            if cur_time < barb.last_attack_time + BARB_ATTACK_TIMESTEP:
                continue
            for building in self._buildings:
                if get_distance(barb, building) < 1:
                    building.deal_damage(barb.damage)
                    barb.last_attack_time = cur_time
                    break

    def cannons_fire(self):
        for cannon in self._cannons:
            if clock() < cannon.last_fired + CANNON_COOL_OFF:
                continue

            target = self._king
            for barb in self._barbarians:
                if get_distance(barb, cannon) < get_distance(target, cannon):
                    target = barb
            if get_distance(target, cannon) <= cannon.range:
                target.deal_damage(cannon.damage)
                cannon.last_fired = clock()
                cannon.style = Style.BRIGHT

    def heal(self):
        self._king.heal(int(self._king.get_health()/2))
        for barb in self._barbarians:
            barb.heal(int(barb.get_health() / 2))

