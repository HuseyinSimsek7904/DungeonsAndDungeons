import random

# Preset colors
WARNING_COLOR = 255, 0, 0
TITLE_COLOR = 100, 100, 100
UNAVAILABLE_COLOR = 150, 150, 150
DEAD_COLOR = 255, 0, 0
NORMAL_COLOR = 255, 255, 255

# Surprise rooms can not be found before level 3.
SURPRISE_ROOM_FIRST = 3

# Chance of finding a surprise room has a horizontal asymptote at 0.2.
SURPRISE_ROOM_MAX_PROBABILITY = 0.2

# Changes how finding the next level enemy is harder.
# For example a level 2 item can be found with 1/2 the chance of finding a level 1 item.
ENEMY_GENERATION_CONSTANT = 1 / 2
TREASURE_GENERATION_CONSTANT = 1 / 2

# Minimum and maximum amount of gold nuggets that can be found in a big chest at level 1.
GOLD_COUNT_MINIMUM = 1
GOLD_COUNT_MAXIMUM = 3

GOLD_COUNT_LEVEL_POWER = 1 / 3


def probability_function(n, p):
    return p ** (n + 1)


def surprise_room(level):
    return random.random() < SURPRISE_ROOM_MAX_PROBABILITY * (1 - SURPRISE_ROOM_FIRST / level)


def big_treasure_room_gold_count(level):
    score = level ** GOLD_COUNT_LEVEL_POWER
    return random.randint(int(score * GOLD_COUNT_MINIMUM), int(score * GOLD_COUNT_MAXIMUM))
