from libs import console_lib, items_lib, entity_lib, constants_lib, enemies_lib
import random


# Super classes of rooms
class Room:
    def __init__(self, game):
        self.game = game

    @property
    def console(self):
        return self.game.console

    @property
    def player(self):
        return self.game.player

    def start(self):
        pass

    def wait(self):
        pass


class ShopRoom(Room):
    shopkeeper = None

    @property
    def score(self):
        return 1

    def start(self):
        self.shopkeeper = entity_lib.Shopkeeper(self.game)
        self.shopkeeper.generate_items(self.score)

        self.game.console.clear_screen()
        self.game.console.set_console(
            console_lib.StoryDismissBox,
            items=(
                "You enter a room.",
                "In the room, there is a shop.",
                "You go towards the shopkeeper."
            ),
            event=self.update
        )

    def update(self):
        money = self.player.count_item(items_lib.GoldNugget)

        self.console.set_console(
            console_lib.SelectionEventSystem
        )

        self.console.print(5, 3, "Market contents:")

        for item_no, item in enumerate(self.shopkeeper.inventory):
            if money >= item.buy_price:
                self.console.event_system.add_item(
                    console_lib.Button(5, 5 + item_no, f"{item.buy_price}$ - {item}", self.buy,
                                       constants_lib.NORMAL_COLOR, 0, self.player, item))

            else:
                self.console.print(5, 5 + item_no, f"{item.buy_price}$ - {item}", constants_lib.UNAVAILABLE_COLOR,
                                   pivot=0)

        self.console.print(self.game.width - 5, 3, "Inventory:", pivot=1)

        for item_no, item in enumerate(self.player.inventory):
            if item.sell_price is None:
                self.console.print(self.game.width - 5, 5 + item_no, item, constants_lib.UNAVAILABLE_COLOR, pivot=1)

            else:
                self.console.event_system.add_item(
                    console_lib.Button(self.game.width - 5, 5 + item_no, f"{item} - {item.sell_price}$",
                                       self.sell, constants_lib.NORMAL_COLOR, 1, self.player, item))

        self.player.check_over_carrying(self.end)
        self.console.update()

    def buy(self, to, item):
        to.remove_item_type(items_lib.GoldNugget, item.buy_price)
        self.shopkeeper.give(to, item)
        self.update()

    def sell(self, to, item):
        to.give(self.shopkeeper, item)
        to.add_item_type(items_lib.GoldNugget, item.sell_price)
        self.update()

    def end(self):
        self.game.jump_room(LadderRoom)


class TreasureRoom(Room):
    chest = None
    story = None

    @property
    def score(self):
        raise SyntaxError("'score' property must be updated when made a class inherit TreasureRoom.")

    def start(self):
        if self.story is None:
            raise ValueError("'story' property should be updated when made a class inherit TreasureRoom.")

        self.chest = entity_lib.Chest(self.game)
        items_lib.generate_items(self.chest, self.score)

        self.at_start()

        self.game.console.clear_screen()
        self.game.console.set_console(console_lib.StoryDismissBox, items=self.story, event=self.update)

    def at_start(self):
        pass

    def update(self):
        self.console.set_console(console_lib.SelectionEventSystem)

        self.console.print(5, 3, "Chest contents:")

        for item_no, item in enumerate(self.chest.inventory):
            self.console.event_system.add_item(
                console_lib.Button(5, 5 + item_no, item, self.take_item, constants_lib.NORMAL_COLOR, 0, item))

        self.console.print(self.game.width - 5, 3, "Inventory:", pivot=1)

        self.player.print_inventory(self.game.console.event_system, self.game.width - 5, 5, self.put_item, 1)

        self.player.check_over_carrying(self.end)
        self.console.update()

    def take_item(self, item):
        self.chest.remove_item(item)
        self.player.add_item(item)
        self.update()

    def put_item(self, item):
        self.player.remove_item(item)
        self.chest.add_item(item)
        self.update()

    def end(self):
        raise SyntaxError("'end' property should be updated when made a class inherit TreasureRoom.")


# Game rooms
class MainMenu(Room):
    def start(self):
        self.console.set_console(console_lib.SelectionEventSystem,
                                 quit_event=quit,
                                 back_event=quit)
        self.console.print(10, 3, "Dungeons and Dungeons")

        self.console.event_system.add_items(
            (
                console_lib.Button(5, 6, "New game", self.new_game),
                console_lib.Button(5, 7, "Continue", self.continue_game),
                console_lib.Button(5, 8, "About", self.about),
                console_lib.Button(5, 9, "Quit", quit)
            )
        )
        self.console.update()

    def new_game(self):
        self.console.set_console(console_lib.SelectionEventSystem)
        self.game.username.reset()
        self.game.difficulty.reset()
        self.console.event_system.back_item = self.start

        self.console.print(10, 3, "Creating new game")

        self.console.event_system.add_items(
            (
                console_lib.Input(5, 6, 10, "name", self.game.username, lambda: (), limit=False),
                console_lib.RadioButton(5, 8, "easy", self.game.difficulty, 1),
                console_lib.RadioButton(5, 9, "medium", self.game.difficulty, 2),
                console_lib.RadioButton(5, 10, "hard", self.game.difficulty, 3),
                console_lib.Button(5, 12, "create game", self.create_new_game),
                console_lib.Button(5, 13, "back", self.start)
            )
        )

        self.console.update()

    def continue_game(self):
        pass

    def about(self):
        pass

    def create_new_game(self):
        if len(self.game.username.value) < 4:
            return

        self.game.username = self.game.username.value
        self.game.difficulty = self.game.difficulty.value

        self.game.player = entity_lib.Player(self.game)
        self.game.jump_room(ChaosRoom)


class Dead(Room):
    def start(self):
        self.console.set_console(
            console_lib.QuickDismissBox,
            text=(f"GAME OVER\n"
                  f"level: {self.player.level}"),
            event=lambda: self.game.jump_room(MainMenu)
        )


class ChaosRoom(Room):
    player_turn = True
    enemies = None

    def start(self):
        self.enemies = []

        enemies_lib.generate_enemies(self,
                                     self.player.level + self.player.chaos_room_hardness + self.game.difficulty - 1)
        self.turn()

    def ask_enemy(self, title, function):
        self.console.set_console(console_lib.SelectionEventSystem,
                                 back_event=self.check_inventory)
        self.console.print(10, 3, title)

        for enemy_no, enemy in enumerate(self.enemies):
            if enemy.dead:
                self.console.print(5, 5 + enemy_no, enemy)

            else:
                button = console_lib.Button(5, 5 + enemy_no, enemy, function, constants_lib.NORMAL_COLOR, 0, enemy)
                self.console.event_system.add_item(button)

        self.console.update()

    def check_inventory(self):
        self.console.set_console(console_lib.SelectionEventSystem,
                                 back_event=self.turn)

        self.console.print(10, 5, "Inventory", constants_lib.TITLE_COLOR)

        self.player.print_inventory(self.game.console.event_system, 5, 7, items_lib.Item.menu, 0)

        self.console.update()

    def print_enemies(self):
        self.console.print(10, 3, "Enemies", constants_lib.TITLE_COLOR)

        for enemy_no, enemy in enumerate(self.enemies):
            self.console.print(5, 5 + enemy_no, enemy)

    def turn(self):
        if self.player_turn:
            self.console.event_system.back_item = self.wait

            if self.player.dead:
                self.game.jump_room(Dead)
                return

            if self.all_enemies_dead:
                self.game.jump_room(AfterChaosRoom)
                return

            if self.player.turn_loss:
                self.player.turn_loss -= 1
                self.lost_turn()
                return

            self.console.set_console(console_lib.SelectionEventSystem)

            self.print_enemies()

            self.console.print(50, 5, f"{self.player.health} HP")
            self.console.event_system.add_items((
                console_lib.Button(5, 15, "Check inventory", self.check_inventory),
                console_lib.Button(5, 16, "Try to escape", self.escape)
            )
            )

        else:
            for enemy in self.enemies.copy():
                if enemy.dead:
                    continue

                if enemy.turn_loss:
                    enemy.turn_loss -= 1
                    continue

                enemy.turn()

            self.player_turn = True
            self.turn()

    def lost_turn(self):
        self.player_turn = False

        self.console.set_console(
            console_lib.QuickDismissBox,
            text="Lost your turn.",
            event=self.turn
        )

    def escape(self):
        pass

    def end(self):
        self.game.jump_room(AfterChaosRoom)

    @property
    def all_enemies_dead(self):
        for enemy in self.enemies:
            if not enemy.dead:
                return False

        return True


class AfterChaosRoom(Room):
    required_key = None

    def start(self):
        self.player.clear_effects()
        self.player.chaos_room_treasure_score += 1

        value = random.randint(1, self.player.chaos_room_treasure_score + 2)

        if value <= 3:
            self.required_key = items_lib.SilverKey

        else:
            self.required_key = items_lib.GoldKey

        self.console.set_console(console_lib.SelectionEventSystem)

        self.console.print(5, 5, "A door opened and you passed through it.")
        self.console.print(5, 6, "In the room, you see two doors.")
        self.console.print(5, 7, "One is open and has a chest behind.")
        self.console.print(5, 8, f"Other one has a lock that requires a {self.required_key.name}.")

        self.console.event_system.add_item(console_lib.Button(5, 10, "Go through open door.", self.open_room))

        if self.player.has_item(self.required_key):
            self.console.event_system.add_item(
                console_lib.Button(5, 11, f"Unlock locked door using a {self.required_key.name}.", self.side_room)
            )

        else:
            self.console.print(5, 11, f"You don't have a {self.required_key.name}.", constants_lib.UNAVAILABLE_COLOR)

        self.console.update()

    def open_room(self):
        # There is a small chance for the chest to be a decoy.
        # If that is true, player enters to a surprise room.
        # That chance increase when the player's level increase.
        if constants_lib.surprise_room(self.player.level):
            self.player.chaos_room_treasure_score += 1
            self.game.jump_room(SurpriseRoom)

        else:
            self.game.jump_room(BasicTreasureRoom)

    def side_room(self):
        self.player.remove_item_type(self.required_key, 1)
        self.player.chaos_room_hardness += 1
        self.player.chaos_room_treasure_score += 1

        if self.required_key is items_lib.GoldKey:
            # If used a golden key to unlock the door, treasure score and hardness increase more.
            self.player.chaos_room_hardness += 1
            self.player.chaos_room_treasure_score += 3

        self.game.jump_room(ChaosRoom)


class SurpriseRoom(Room):
    def start(self):
        self.game.console.set_console(
            console_lib.StoryDismissBox,
            items=(
                "You passed the opening and a door slammed behind you.",
                "You tried to open the chest; but when you got close, the chest disappeared.",
                "You realize that the chest was a trap.",
                "There are monsters around you."
            ),
            event=self.end
        )

    def end(self):
        self.game.jump_room(ChaosRoom)


class BasicShopRoom(ShopRoom):
    @property
    def score(self):
        return self.player.level + self.player.room_score + 2


class DarkShopRoom(ShopRoom):
    @property
    def score(self):
        return self.player.level * 2 + self.player.room_score + 2


class LadderRoom(Room):
    def start(self):
        self.player.level += 1
        self.player.room_score = 0

        self.game.console.clear_screen()
        self.game.console.set_console(
            console_lib.StoryDismissBox,
            items=(
                "You go down the ladder.",
                f"You are now at level {self.player.level}."
            ),
            event=lambda: self.game.jump_room(ChaosRoom)
        )


class BasicTreasureRoom(TreasureRoom):
    story = (
        "You passed the opening and a door slammed behind you.",
        "You open the chest."
    )

    @property
    def score(self):
        return self.player.chaos_room_treasure_score + self.player.level - 1

    def at_start(self):
        self.player.room_score += 1
        self.player.chaos_room_treasure_score = 0
        self.player.chaos_room_hardness = 0

    def end(self):
        # After treasure rooms, there is either a chaos room or the level ends.
        # A random integer between 1 and 6 is selected and compared to player's room score.
        # If random value is less than player's room score, a new level starts.
        # Otherwise, a chaos room starts.

        # When a new level is going to start, player finds a room and a ladder.
        # At even levels, player finds a shop.
        # At odd levels, player finds a big treasure chest.
        # After two regular shops, there is a dark shop room.

        value = random.randint(1, 6)

        if value >= self.player.room_score:
            self.game.jump_room(ChaosRoom)
            return

        if self.player.level % 2:
            self.game.jump_room(BigTreasureRoom)
            return

        elif self.player.level % 6:
            self.game.jump_room(BasicShopRoom)
            return

        self.game.jump_room(DarkShopRoom)


class BigTreasureRoom(TreasureRoom):
    story = (
        "You enter a room.",
        "In the room, there is a chest."
        "You walk to and open the chest."
    )

    @property
    def score(self):
        return self.player.level + 2

    def at_start(self):
        self.chest.add_item_type(items_lib.GoldNugget, constants_lib.big_treasure_room_gold_count(self.player.level))

    def end(self):
        self.game.jump_room(LadderRoom)
