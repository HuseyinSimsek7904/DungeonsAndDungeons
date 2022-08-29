from libs import items_lib, effects_lib, console_lib, properties_lib


class Entity:
    name: str = "none"
    dead: bool = False
    inventory: list = None

    health: int = 0
    turn_loss: int = 0
    health_loss: int = 0

    effects: list[effects_lib] = None

    def __init__(self, game):
        self.inventory = []
        self.effects = []

        self.game = game

        self.pre_start()
        self.start()

    def __repr__(self):
        if self.dead:
            return f"{self.name.capitalize()} (DEAD)"

        if self.turn_loss:
            return f"{self.name.capitalize()} ({self.health} HP) ({self.turn_loss} stun)"

        return f"{self.name.capitalize()} ({self.health} HP)"

    def clear_inventory(self):
        self.inventory.clear()

    def check_effects(self):
        if self.dead:
            return

        for effect in self.effects:
            effect.at_turn()

            if self.dead:
                return

    def clear_effects(self):
        self.health_loss = 0
        self.turn_loss = 0
        self.effects.clear()

    def pre_start(self):
        pass

    def start(self):
        pass

    def heal(self, from_, amount):
        self.health += amount

    def add_item_type(self, item_type, count=1):
        for _ in range(count):
            item = item_type(self)
            self.inventory.append(item)

    def add_item(self, item):
        if item.owner is not None:
            raise ValueError(f"{item} already has an owner ({item.owner}).")

        item.owner = self
        self.inventory.append(item)

    def remove_item(self, item):
        if item not in self.inventory:
            raise ValueError(f"{self} doesn't have {item} so can not remove it.")

        if item.owner is not self:
            raise ValueError(f"{self} doesn't own {item} so can not remove it.")

        self.inventory.remove(item)
        item.owner = None

    def remove_item_type(self, item_type, count=1):
        has = self.count_item(item_type)

        if has < count:
            raise ValueError(f"{self} doesn't have enough {item_type.name} so can not remove them.")

        for item in self.inventory.copy():
            if type(item) is item_type:
                self.remove_item(item)
                count -= 1

            if count == 0:
                return

        raise SyntaxError("That error should have been impossible to get.")

    def give(self, to, item):
        self.remove_item(item)
        to.add_item(item)

    def damage(self, from_, amount):
        self.health = max(self.health - amount, 0)

        if self.health == 0:
            self.dead = True
            self.died(from_)

    def attack_build_up(self, attack):
        for item in self.inventory:
            item.attack_build_up(attack)

    def defence_build_up(self, attack):
        for item in self.inventory:
            item.defence_build_up(attack)

    def count_item(self, item_type):
        count = 0

        for item in self.inventory:
            if type(item) is item_type:
                count += item.count

        return count

    def has_item(self, item_type):
        for item in self.inventory:
            if type(item) is item_type:
                return True

        return False

    def has_item_with_tag(self, tag_type):
        for item in self.inventory:
            if item.has_tag(tag_type):
                return True

        return False

    @property
    def inventory_capacity(self):
        capacity = 0
        buff = 0
        extra = 0

        for item in self.inventory:
            buff = max(item.extra_space, buff)
            extra += item.extra_space_

        return capacity + buff + extra

    @property
    def inventory_size(self):
        size = 0
        for item in self.inventory:
            size += item.item_size

        return round_to(size, 0.01)

    @property
    def over_carrying(self):
        return self.inventory_size > self.game.player.inventory_capacity

    def died(self, from_):
        for item in self.inventory:
            item.died(from_)

    @property
    def money(self):
        return self.count_item(items_lib.GoldNugget)

    def turn(self):
        self.game.room.turn()


class Player(Entity):
    name = "player"
    health = 10
    level = 1

    room_score = 0

    chaos_room_hardness = 0
    chaos_room_treasure_score = 0

    def start(self):
        from libs import items_lib

        self.clear_inventory()
        self.add_item_type(items_lib.WoodenSword)
        self.add_item_type(items_lib.BluePotion)
        self.add_item_type(items_lib.LittlePack)

    def check_over_carrying(self, function):
        if self.game.player.over_carrying:
            self.game.console.print(self.game.width // 2, 8, "I am carrying too much.", (150, 150, 150), pivot=0.5)

        elif not self.game.player.has_item_with_tag(properties_lib.Weapon):
            self.game.console.print(self.game.width // 2, 8, "You have no weapon.", (150, 150, 150), pivot=0.5)

        else:
            self.game.console.event_system.add_item(console_lib.Button(self.game.width // 2, 8, "Ready!", function,
                                                                       pivot=0.5))

    def print_inventory(self, event_system: console_lib.SelectionEventSystem, x, y, function, pivot=0):
        items = []

        for item in self.inventory:
            rep = repr(item)

            for old in items:
                if old[1] == rep:
                    old[0] = item
                    old[2] += 1
                    break

            else:
                items.append([item, rep, 1])

        for no, (item, rep, count) in enumerate(items):
            if count > 1:
                rep += f" x{count}"

            if count * item.item_size != 1:
                rep += f" ({round_to(count * item.item_size, 0.01)} space)"

            button = console_lib.Button(x, y + no, rep, function, (255, 255, 255), pivot, item)
            button.select_function = item.print_description
            button.deselect_function = item.clear_description
            event_system.add_item(button)

        self.game.console.update()


class Shopkeeper(Entity):
    name = "shopkeeper"
    health = 20

    def generate_items(self, score):
        self.clear_inventory()

        while len(self.inventory) < 3:
            items_lib.generate_items(self, score, True)


class Chest(Entity):
    name = "chest"
    health = 1

    def generate_items(self, score):
        self.clear_inventory()

        while len(self.inventory) < 3:
            items_lib.generate_items(self.inventory, score, True)


def round_to(number, to):
    return int(number / to) * to
