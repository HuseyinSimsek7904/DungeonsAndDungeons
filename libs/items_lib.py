from libs import properties_lib, constants_lib, console_lib
import random


class Item:
    name = ""

    owner = None
    count = 1

    # Shows how much space that item is taking.
    item_size = 1

    buy_price = None
    sell_price = None

    tags = ()

    extra_space = 0
    extra_space_ = 0

    menu_options = None

    def copy(self):
        return type(self)(self.owner)

    def __repr__(self):
        text = self.name.capitalize()
        status = []

        for tag in self.tags:
            if tag.status:
                status.append(tag.status)

        if len(status):
            text += f" ({status[0]}"

            for item in status[1:]:
                text += f", {item}"

            text += ")"

        return text

    def __init__(self, owner):
        self.owner = owner
        self.menu_options = {}

        self.add_menu_options({"Back": self.owner.turn, "Drop": self.drop})

        self.start()

    @property
    def description(self):
        return "You were not supposed to see this."

    def print_description(self):
        self.owner.game.console.print(10, self.owner.game.console.height - 8, self.name.capitalize())
        self.owner.game.console.better_print(5, self.owner.game.console.height - 6, self.description)

    def clear_description(self):
        self.owner.game.console.clear_screen(0, self.owner.game.console.height - 8, self.owner.game.console.width, 10)

    def start(self):
        pass

    def add_property(self, tag_type):
        tag = tag_type(self)
        self.tags += tag,

    def kill(self):
        self.owner.remove_item(self)

    def drop(self):
        old = self.owner
        self.kill()
        old.game.room.turn()

    def use(self):
        for tag in self.tags:
            tag.pre_use()

        for tag in self.tags:
            tag.use()

        for tag in self.tags:
            tag.late_use()

    def attack_build_up(self, attack):
        for tag in self.tags:
            tag.pre_attack_build_up(attack)

        for tag in self.tags:
            tag.attack_build_up(attack)

        for tag in self.tags:
            tag.late_attack_build_up(attack)

    def defence_build_up(self, attack):
        for tag in self.tags:
            tag.pre_defence_build_up(attack)

        for tag in self.tags:
            tag.defence_build_up(attack)

        for tag in self.tags:
            tag.late_defence_build_up(attack)

    def died(self, from_):
        pass

    def has_tag(self, tag_type):
        for tag in self.tags:
            if type(tag) is tag_type:
                return True

        return False

    def menu(self):
        self.owner.game.console.event_system.clear_items()
        self.owner.game.console.clear_screen(0, self.owner.game.console.height - 8, self.owner.game.console.width, 10)

        for no, (option, function) in enumerate(self.menu_options.items()):
            self.owner.game.console.event_system.add_item(
                console_lib.Button(5, self.owner.game.console.height - 8 + no, option, function))

        self.owner.game.console.update()

    def add_menu_options(self, args: dict):
        args.update(self.menu_options)
        self.menu_options = args


class HealthPotion(Item):
    heal_amount = 0

    def start(self):
        self.add_property(properties_lib.HealthPotion)
        self.add_property(properties_lib.ActiveUseTag)
        self.add_property(properties_lib.TurnLoss)

        self.add_menu_options({"Drink": self.use})

    @property
    def description(self):
        return f"A potion that restores {self.heal_amount} HP."


class Key(Item):
    def start(self):
        self.add_property(properties_lib.Key)

    @property
    def description(self):
        return "A key that might be used to unlock stuff."


# Unobtainable
###############################################################
class SlimyBall(Item):
    name = "slimy ball"
    buy_price = 5
    sell_price = 2

    def start(self):
        self.add_property(properties_lib.Slimy)


class VampireTeeth(Item):
    name = "vampire teeth"
    buy_price = 7
    sell_price = 3

    def start(self):
        self.add_property(properties_lib.VampireBite)


class SharpTeeth(Item):
    name = "sharp teeth"
    buy_price = 3
    sell_price = 1

    def start(self):
        self.add_property(properties_lib.Bite)


class RatKingsStaff(Item):
    name = "rat king's staff"
    buy_price = 15
    sell_price = 7

    def start(self):
        self.add_property(properties_lib.RatSummoner)
        self.add_property(properties_lib.Bite)


class BatQueensCrown(Item):
    name = "bat queen's crown"
    buy_price = 23
    sell_price = 12

    def start(self):
        self.add_property(properties_lib.BatSummoner)
        self.add_property(properties_lib.Bite)


# not treasure
###############################################################
class WoodenSword(Item):
    name = "wooden sword"
    buy_price = 1
    sell_price = 1

    def start(self):
        self.add_property(properties_lib.WoodForce)
        self.add_property(properties_lib.TurnLoss)
        self.add_property(properties_lib.Weapon)

        self.add_menu_options({"Attack": self.use})

    @property
    def description(self):
        return "A sword I found before entering the dungeon.\nDoes little damage."


class LittlePack(Item):
    name = "little pack"
    buy_price = None
    sell_price = 1
    extra_space = 5

    @property
    def description(self):
        return "The backpack I brought to the dungeon.\nI can carry 4 items with it."


class GoldNugget(Item):
    name = "gold nugget"
    item_size = 0.1

    def start(self):
        self.add_property(properties_lib.Money)

    @property
    def description(self):
        return "A piece of gold with symbols on it.\nProbably used in some markets."


# level 1
###############################################################
class SteelSword(Item):
    name = "steel sword"
    buy_price = 3
    sell_price = 1

    def start(self):
        self.add_property(properties_lib.SteelForce)
        self.add_property(properties_lib.TurnLoss)
        self.add_property(properties_lib.Weapon)

        self.add_menu_options({"Attack": self.use})

    @property
    def description(self):
        return "A steel sword that is made poorly.\nDoes little damage but definitely better than what I came with."


class WoodenBow(Item):
    name = "wooden bow"
    buy_price = 3
    sell_price = 1

    def start(self):
        self.add_property(properties_lib.WoodenBowForce)
        self.add_property(properties_lib.TurnLoss)
        self.add_property(properties_lib.Weapon)

        self.add_menu_options({"Attack": self.use})

    @property
    def description(self):
        return "A poorly made bow.\nLow accuracy but can be used against high HP enemies."


class BluePotion(HealthPotion):
    name = "blue potion"
    buy_price = 2
    sell_price = 1
    heal_amount = 4
    item_size = 0.25


class SilverKey(Key):
    name = "silver key"
    buy_price = 3
    sell_price = 1
    item_size = 0.25


class Backpack(Item):
    name = "backpack"
    buy_price = 8
    sell_price = 3
    extra_space = 6

    @property
    def description(self):
        return "I can carry 5 items at the same time with this."


# level 2
###############################################################
class RedPotion(HealthPotion):
    name = "red potion"
    buy_price = 5
    sell_price = 2
    heal_amount = 9
    item_size = 0.25


class Katana(Item):
    name = "katana"
    buy_price = 6
    sell_price = 3

    def start(self):
        self.add_property(properties_lib.KatanaBlade)
        self.add_property(properties_lib.TurnLoss)
        self.add_property(properties_lib.Weapon)

        self.add_menu_options({"Attack": self.use})

    @property
    def description(self):
        return "A Japanese weapon.\nSomehow you found it in the dungeon.\nDoes good damage against."


class SteelBow(Item):
    name = "steel bow"
    buy_price = 7
    sell_price = 3

    def start(self):
        self.add_property(properties_lib.SteelBowForce)
        self.add_property(properties_lib.TurnLoss)
        self.add_property(properties_lib.Weapon)

        self.add_menu_options({"Attack": self.use})

    @property
    def description(self):
        return "A bow.\nHas low accuracy but can be used against high HP enemies."


class GoldKey(Key):
    name = "gold key"
    buy_price = 8
    sell_price = 3
    item_size = 0.5


class SteelChestplate(Item):
    name = "steel chestplate"
    buy_price = 8
    sell_price = 4

    def start(self):
        self.add_property(properties_lib.SteelProtection)

    @property
    def description(self):
        return "A piece of armor that can protect me from enemy attacks."


class IceStaff(Item):
    name = "ice staff"
    buy_price = 9
    sell_price = 4

    def start(self):
        self.add_property(properties_lib.Freezer)
        self.add_property(properties_lib.BasicSpell)
        self.add_property(properties_lib.TurnLoss)
        self.add_property(properties_lib.Weapon)

        self.add_menu_options({"Attack": self.use})

    @property
    def description(self):
        return "A staff that can cause enemies to freeze.\nCan be useful against high HP and high damage enemies."


class Bigpack(Item):
    name = "big pack"
    buy_price = 15
    sell_price = 7
    extra_space = 7

    @property
    def description(self):
        return "A big backpack.\nI can carry 6 items at the same time with this."


# level 3
###############################################################
class FrozenBoots(Item):
    name = "frozen boots"
    buy_price = 17
    sell_price = 9

    def start(self):
        self.add_property(properties_lib.SteelProtection)
        self.add_property(properties_lib.FrozenLayer)

    @property
    def description(self):
        return "Some cool looking boots. Can cause enemies to freeze when they hit me."


class GoldenPotion(HealthPotion):
    name = "golden potion"
    buy_price = 16
    sell_price = 8
    heal_amount = 19


class NightSword(Item):
    name = "night sword"
    buy_price = 17
    sell_price = 9

    def start(self):
        self.add_property(properties_lib.DarkEdge)
        self.add_property(properties_lib.TurnLoss)
        self.add_property(properties_lib.Weapon)

        self.add_menu_options({"Attack": self.use})

    @property
    def description(self):
        return "A sword that sure has mysteries.\nDoes great amounts of damage."


class HugePack(Item):
    name = "huge pack"
    buy_price = 30
    sell_price = 16
    extra_space = 8

    @property
    def description(self):
        return "A backpack that is stupidly big.\nI can carry 7 items at the same time with this."


# level 4
###############################################################
class ThornyChestplate(Item):
    name = "thorny chestplate"
    buy_price = 23
    sell_price = 12

    def start(self):
        self.add_property(properties_lib.Thorniness)
        self.add_property(properties_lib.SteelProtection)

    @property
    def description(self):
        return "A piece of armor that can hurt enemies that attack me."


class Dagger(Item):
    name = "dagger"
    buy_price = 21
    sell_price = 12

    def start(self):
        self.add_property(properties_lib.DaggerBlade)
        self.add_property(properties_lib.TurnLoss)
        self.add_property(properties_lib.Weapon)

        self.add_menu_options({"Attack": self.use})

    @property
    def description(self):
        return "A weapon that can do great amounts of critical damage."


class DarkAmulet(Item):
    name = "dark amulet"
    buy_price = 27
    sell_price = 15

    def start(self):
        self.add_property(properties_lib.MagicConverter)

    @property
    def description(self):
        return "An amulet that can increase my damage."


class GigaPack(Item):
    name = "giga pack"
    buy_price = 49
    sell_price = 26
    extra_space = 9

    @property
    def description(self):
        return "An enormous backpack.\nSomehow I can take it.\nI can carry 8 items with this."


# level 5
###############################################################
class BloodCup(Item):
    name = "blood cup"
    buy_price = 34
    sell_price = 17

    @property
    def blood_charge(self):
        return self.tags[0].blood_charge

    def drink(self):
        pass

    def start(self):
        self.add_property(properties_lib.Cup)
        self.add_property(properties_lib.LeatherProtection)

        self.add_menu_options({"Attack": self.use, "Drink": self.drink})

    @property
    def description(self):
        return "A cup that has weird symbols on it.\n" \
               "If I drop my blood on it, can increase my damage.\n" \
               "I can also drink my blood back."


# should be fixed
###############################################################
class FlashBomb(Item):
    name = "flash bomb"
    buy_price = 6
    sell_price = 4

    def start(self):
        self.add_property(properties_lib.SmallExplosiveFlash)
        self.add_property(properties_lib.TurnLoss)


class KeyHolder(Item):
    name = "key holder"
    buy_price = 18
    sell_price = 9

    @property
    def extra_space_(self):
        extra = 0

        for item in self.owner.inventory:
            if item.has_tag(properties_lib.Key):
                extra += 1

                if extra == 3:
                    break

        return extra


class Purse(Item):
    name = "purse"
    buy_price = 16
    sell_price = 9

    @property
    def extra_space_(self):
        extra = 0

        for item in self.owner.inventory:
            if item.has_tag(properties_lib.Money):
                extra += 1

                if extra == 2:
                    break

        return extra


class RebirthTotem(Item):
    name = "rebirth totem"
    buy_price = 52
    sell_price = 27

    def start(self):
        self.add_property(properties_lib.OneMoreChance)


class CursedSword(Item):
    name = "cursed_sword"
    buy_price = 25
    sell_price = 14

    def start(self):
        self.add_property(properties_lib.KatanaBlade)
        self.add_property(properties_lib.OneMoreChance)
        self.add_property(properties_lib.TurnLoss)
        self.add_property(properties_lib.Weapon)


class Bomb(Item):
    name = "bomb"
    buy_price = 7
    sell_price = 3

    def start(self):
        self.add_property(properties_lib.SmallExplosive)
        self.add_property(properties_lib.ActiveUseTag)
        self.add_property(properties_lib.TurnLoss)


treasures = (
    # level 1
    (BluePotion, SteelSword, WoodenBow, SilverKey, Backpack),

    # level 2
    (RedPotion, SteelChestplate, GoldKey, IceStaff, SteelBow, Katana, Bigpack),

    # level 3
    (FrozenBoots, GoldenPotion, NightSword, BloodCup, HugePack),

    # level 4
    (ThornyChestplate, DarkAmulet, Dagger, GigaPack),
)


def generate_items(entity, score, must_have_price=False):
    entity.clear_inventory()

    while score:
        if score < 0:
            raise SyntaxError

        value = random.random()

        for group_no, group in enumerate(treasures):
            if score > group_no and value >= constants_lib.probability_function(group_no,
                                                                                constants_lib.TREASURE_GENERATION_CONSTANT):
                score -= group_no + 1
                break

        else:
            continue

        treasure_type = random.choice(group)

        while must_have_price:
            if treasure_type.buy_price:
                break

            treasure_type = random.choice(group)

        entity.add_item_type(treasure_type)
