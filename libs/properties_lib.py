from libs import attack_lib, console_lib
import random


class Property:
    def __init__(self, item):
        self.item = item

    @property
    def status(self):
        return ""

    def pre_attack_build_up(self, attack):
        pass

    def attack_build_up(self, attack):
        pass

    def late_attack_build_up(self, attack):
        pass

    def pre_defence_build_up(self, attack):
        pass

    def defence_build_up(self, attack):
        pass

    def late_defence_build_up(self, attack):
        pass

    def pre_use(self):
        pass

    def use(self):
        pass

    def late_use(self):
        pass


class AttackProperty(Property):
    def use(self):
        self.item.owner.game.room.ask_enemy("Select an enemy to attack:", self.use_attack)

    def use_attack(self, enemy):
        attack = attack_lib.Attack(self.item, enemy)
        value = random.random()

        self.attack(value, attack)

        attack.do()

        if attack.total_damage:
            self.item.owner.game.console.clear_screen()
            self.item.owner.game.console.set_console(console_lib.QuickDismissBox,
                                                     text=f"Attacked {enemy}.\n"
                                                          f"Dealt {attack.total_damage} damage.",
                                                     event=self.item.owner.game.room.turn)

        else:
            self.item.owner.game.console.clear_screen()
            self.item.owner.game.console.set_console(console_lib.QuickDismissBox,
                                                     text=f"Tried to attack {enemy}.\n"
                                                          f"But missed.",
                                                     event=self.item.owner.game.room.turn)

    def attack(self, value, attack):
        pass


class TurnLoss(Property):
    """
    When used:
        Causes turn to be lost.
    """

    def use(self):
        self.item.owner.game.room.player_turn = False


class BasicSpell(AttackProperty):
    """
    When used:
        %16: miss
        %33: 1 mgc
        %16: 2 mgc
        %33: 3 mgc

        total: 1.66 mgc per use
        1.66 total damage
    """

    def attack(self, value, attack):
        if value < 5 / 6:
            attack.magical_damage += 1

        if value < 1 / 2:
            attack.magical_damage += 1

        if value < 1 / 3:
            attack.magical_damage += 1


class Freezer(Property):
    """
    When attacking:
        Adds turn loss.
    """

    def attack_build_up(self, attack):
        value = random.randint(0, attack.magical_damage)
        attack.turn_loss += value


class FrozenLayer(Property):
    """
    When defending:
        Adds turn loss.
    """

    def defence_build_up(self, attack):
        value = random.randint(0, attack.physical_damage)
        attack.inv_turn_loss += value


class WoodForce(AttackProperty):
    """
    When used:
        %16: miss
        %83: 1 dmg

        total: 0.83 dmg per use
        0.83 total dmg
    """

    def attack(self, value, attack):
        if value < 5 / 6:
            attack.physical_damage += 1


class SteelForce(AttackProperty):
    """
    When used:
        %16: miss
        %50: 1 dmg
        %16: 2 dmg
        %16: 2 dmg + 1 crt

        total: 1.16 dmg + 0.16 crt per use
        1.33 total dmg
    """

    def attack(self, value, attack):
        if value < 5 / 6:
            attack.physical_damage += 1

        if value < 2 / 6:
            attack.physical_damage += 1

        if value < 1 / 6:
            attack.critical_damage += 1


class KatanaBlade(AttackProperty):
    """
    When used:
        %33: 1 dmg
        %33: 2 dmg
        %16: 3 dmg
        %16: 5 dmg + 1 crt

        total: 2.33 dmg + 0.16 crt per use
        2.5 dmg total
    """

    def attack(self, value, attack):
        attack.physical_damage += 1

        if value < 4 / 6:
            attack.physical_damage += 1

        if value < 2 / 6:
            attack.physical_damage += 1

        if value < 1 / 6:
            attack.physical_damage += 2
            attack.critical_damage += 1


class DarkEdge(AttackProperty):
    """
    When used:
        %16: 1 dmg
        %16: 1 dmg + 1 mgc
        %16: 1 dmg + 2 mgc
        %16: 1 dmg + 3 mgc
        %16: 1 dmg + 3 mgc + 1 crt
        %16: 1 dmg + 3 mgc + 3 crt

        total: 1 dmg + 2 mgc + 0.66 crt per use
        3.66 total dmg
    """

    def attack(self, value, attack):
        attack.physical_damage += 1

        if value < 5 / 6:
            attack.magical_damage += 1

        if value < 4 / 6:
            attack.magical_damage += 1

        if value < 3 / 6:
            attack.magical_damage += 1

        if value < 2 / 6:
            attack.magical_damage += 1
            attack.critical_damage += 1

        if value < 1 / 6:
            attack.critical_damage += 2


class WoodenBowForce(AttackProperty):
    """
    When used:
        %50: miss
        %16: 1 dmg
        %16: 2 dmg + 1 crt
        %16: 3 dmg + 2 crt

        total: 1 dmg + 0.5 crt per use
        1.5 total dmg
    """

    def attack(self, value, attack):
        if value < 1 / 2:
            attack.physical_damage += 1

        if value < 1 / 3:
            attack.physical_damage += 1
            attack.critical_damage += 1

        if value < 1 / 6:
            attack.physical_damage += 1
            attack.critical_damage += 1


class SteelBowForce(AttackProperty):
    """
    When used:
        %33: miss
        %33: 1 dmg
        %16: 3 dmg + 1 crt
        %16: 4 dmg + 2 crt
        %16: 5 dmg + 3 crt

        total: 2.16 dmg + 1 crt per use
        3.16 total damage
    """

    def attack(self, value, attack):
        if value < 2 / 3:
            attack.physical_damage += 1

        if value < 1 / 2:
            attack.physical_damage += 2
            attack.critical_damage += 1

        if value < 1 / 3:
            attack.physical_damage += 1
            attack.critical_damage += 1

        if value < 1 / 6:
            attack.physical_damage += 1
            attack.critical_damage += 1


class DaggerBlade(AttackProperty):
    """
    When used:
        %16: 1 dmg
        %16: 1 dmg + 1 crt
        %16: 1 dmg + 2 crt
        %16: 1 dmg + 3 crt
        %16: 1 dmg + 4 crt
        %16: 1 dmg + 5 crt

        total: 1 dmg + 2.5 crt per use
        3.5 total damage
    """

    def attack(self, value, attack):
        attack.physical_damage += 1

        if value < 5 / 6:
            attack.critical_damage += 1

        if value < 2 / 3:
            attack.critical_damage += 1

        if value < 1 / 2:
            attack.critical_damage += 1

        if value < 1 / 3:
            attack.critical_damage += 1

        if value < 1 / 6:
            attack.critical_damage += 1


class ActiveUseTag(Property):
    """
    Causes item to be spent when used.
    """

    def late_use(self):
        self.item.kill()


class SmallExplosive(Property):
    """
    When used:
        Attacks all enemies.
        %16: miss
        %66: 1 dmg
        %16: 2 dmg
    """

    def use(self):
        for enemy in self.item.owner.game.room.enemies:
            attack = attack_lib.Attack(self.item, enemy)
            value = random.random()

            if value < 5 / 6:
                attack.physical_damage += 1

            if value < 1 / 6:
                attack.physical_damage += 1

            attack.do()


class SmallExplosiveFlash(Property):
    """
    When used:
        Attacks all enemies.
        %16: miss
        %50: 1 turn loss
        %16: 2 turn loss
        %16: 1 dmg + 3 turn loss

        total: 0.16 dmg + 1.33 turn loss
    """

    def use(self):
        for enemy in self.item.owner.game.enemies:
            attack = attack_lib.Attack(self.item, enemy)
            value = random.random()

            if value < 5 / 6:
                attack.turn_loss += 1

            if value < 2 / 6:
                attack.turn_loss += 1

            if value < 1 / 6:
                attack.physical_damage += 1
                attack.turn_loss += 1

            attack.do()
            self.item.kill()


class CriticDamageResistance(Property):
    """
    When defending:
        Sets critic damage to zero.
    """

    def defence_build_up(self, attack):
        attack.critical_damage = 0


class Thorniness(Property):
    """
    When defending:
        %33: Adds all of physical damage to thorn damage.
    """

    def defence_build_up(self, attack):
        value = random.random()

        if value < 1 / 3:
            attack.thorn_damage = attack.physical_damage


class LeatherProtection(Property):
    """
    When defending:
        %33: -1 dmg

        total: -0.33 dmg
    """

    def defence_build_up(self, attack):
        value = random.random()

        if value < 1 / 3:
            attack.physical_damage -= 1


class Cup(Property):
    """
    After getting physical damage, blood charges increase.
    Max charge amount is 25.
    When a weapon does critic damage, it causes blood charges to be spent and increase magic damage.
    """

    _blood_charge = 0

    @property
    def blood_charge(self):
        return self._blood_charge

    @blood_charge.setter
    def blood_charge(self, value):
        self._blood_charge = min(max(value, 0), 25)

    @property
    def status(self):
        return f"{self.blood_charge} drops"

    def defence_build_up(self, attack):
        value = random.randint(0, attack.physical_damage)

        self.blood_charge = min(self.blood_charge + value, 25)

    def late_attack_build_up(self, attack):
        value = min(attack.critical_damage, self.blood_charge)
        self.blood_charge -= value
        attack.magical_damage += value


class SteelProtection(Property):
    """
    When defending:
        %33: -1 dmg
        %16: -2 dmg

        total: -0.66 dmg
    """

    def defence_build_up(self, attack):
        value = random.random()

        if value < 1 / 2:
            attack.physical_damage -= 1

        if value < 1 / 6:
            attack.physical_damage -= 1


class OneMoreChance(Property):
    def late_defence_build_up(self, attack):
        if attack.total_damage > self.item.owner.health:
            attack.reset()

            self.item.owner.health = 10
            self.item.kill()


class HealthPotion(Property):
    @property
    def status(self):
        return f"+{self.item.heal_amount} HP"

    def use(self):
        self.item.owner.heal(self, self.item.heal_amount)

        self.item.owner.game.console.clear_screen()
        self.item.owner.game.console.set_console(console_lib.QuickDismissBox,
                                                 text=f"You drank {self.item}.\n"
                                                      f"It gave you {self.item.heal_amount} HP.\n"
                                                      f"Now you have {self.item.owner.health} HP",
                                                 event=self.item.owner.game.room.turn)


class MagicConverter(Property):
    def late_attack_build_up(self, attack):
        value = random.randint(0, attack.physical_damage)
        attack.magical_damage += value


class Bow(Property):
    pass


class Staff(Property):
    pass


class Dark(Property):
    pass


class Key(Property):
    pass


class Money(Property):
    pass


class Weapon(Property):
    pass


class RatSummoner(Property):
    summon_chance = 1 / 5

    def use(self):
        from libs import enemies_lib

        value = random.random()

        if value < self.summon_chance:
            enemy = enemies_lib.Rat(self.item.owner.game)
            self.item.owner.game.room.enemies.append(enemy)


class BatSummoner(Property):
    summon_chance = 1 / 4

    def use(self):
        from libs import enemies_lib

        value = random.random()

        if value < self.summon_chance:
            enemy = enemies_lib.Bat(self.item.owner.game)
            self.item.owner.game.room.enemies.append(enemy)


class EnemiesAttackProperty(Property):
    def use(self):
        attack = attack_lib.Attack(self.item, self.item.owner.game.player)
        value = random.random()
        self.attack(value, attack)
        attack.do()

    def attack(self, value, attack):
        pass


class Bite(EnemiesAttackProperty):
    def attack(self, value, attack):
        if value < 5 / 6:
            attack.physical_damage += 1


class Slimy(EnemiesAttackProperty):
    def attack(self, value, attack):
        if value < 3 / 6:
            attack.magical_damage += 1

        if value < 1 / 6:
            attack.turn_loss += 1


class VampireBite(EnemiesAttackProperty):
    def attack(self, value, attack):
        if value < 3 / 6:
            attack.physical_damage = 1

        if value < 1 / 6:
            attack.life_steal = 1
