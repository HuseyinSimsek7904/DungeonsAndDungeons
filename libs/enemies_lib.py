from libs import entity_lib, items_lib, constants_lib
import random


class Enemy(entity_lib.Entity):
    name: str = None
    starting_items = ()

    def pre_start(self):
        self.health += self.game.difficulty - 1

        for item_type in self.starting_items:
            self.add_item_type(item_type)

    def turn(self):
        pass


# level 1
###############################################################
class Bat(Enemy):
    name = "bat"
    health = 2
    starting_items = items_lib.SharpTeeth,

    def turn(self):
        self.inventory[0].use()


class Rat(Enemy):
    name = "rat"
    health = 1
    starting_items = items_lib.SharpTeeth,

    def turn(self):
        self.inventory[0].use()


# level 2
###############################################################
class Slime(Enemy):
    name = "slime"
    health = 3
    starting_items = items_lib.SlimyBall,

    def turn(self):
        self.inventory[0].use()


# level 3
################################################################
class Vampire(Enemy):
    name = "vampire"
    health = 4
    starting_items = items_lib.VampireTeeth,

    def turn(self):
        self.inventory[0].use()


# level 4
###############################################################
class RatKing(Enemy):
    name = "rat king"
    health = 9
    starting_items = items_lib.RatKingsStaff,

    def turn(self):
        self.inventory[0].use()


# level 5
###############################################################
class BatQueen(Enemy):
    name = "bat queen"
    health = 14
    starting_items = items_lib.BatQueensCrown,

    def turn(self):
        self.inventory[0].use()


enemies = (
    (Bat, Rat),  # level 1
    (Slime,),  # level 2
    (Vampire,),  # level 3
    (RatKing,),  # level 4
    (BatQueen,)  # level 5
)


def generate_enemies(room, score):
    room.enemies.clear()

    while score:
        if score < 0:
            raise SyntaxError

        value = random.random()

        for group_no, group in enumerate(enemies):
            if score > group_no and value >= constants_lib.probability_function(group_no, constants_lib.ENEMY_GENERATION_CONSTANT):
                score -= group_no + 1
                break

        else:
            continue

        enemy_type = random.choice(group)
        enemy = enemy_type(room.game)
        room.enemies.append(enemy)
