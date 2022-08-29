class Attack:
    _physical_damage = 0
    _magical_damage = 0
    _real_damage = 0
    _critical_damage = 0
    _life_steal = 0
    _turn_loss = 0
    _health_loss = 0
    _thorn_damage = 0
    _inv_turn_loss = 0

    def __repr__(self):
        return f"{self.physical_damage} dmg + {self.magical_damage} mgc + {self.critical_damage} crt"

    def reset(self):
        self.physical_damage = 0
        self.magical_damage = 0
        self.real_damage = 0
        self.critical_damage = 0
        self.life_steal = 0
        self.turn_loss = 0
        self.health_loss = 0

    @property
    def physical_damage(self):
        return self._physical_damage

    @property
    def magical_damage(self):
        return self._magical_damage

    @property
    def real_damage(self):
        return self._real_damage

    @property
    def critical_damage(self):
        return self._critical_damage

    @property
    def life_steal(self):
        return self._life_steal

    @property
    def turn_loss(self):
        return self._turn_loss

    @property
    def health_loss(self):
        return self._health_loss

    @property
    def thorn_damage(self):
        return self._thorn_damage

    @property
    def inv_turn_loss(self):
        return self._inv_turn_loss

    @physical_damage.setter
    def physical_damage(self, value):
        self._physical_damage = max(value, 0)

    @magical_damage.setter
    def magical_damage(self, value):
        self._magical_damage = max(value, 0)

    @real_damage.setter
    def real_damage(self, value):
        self._real_damage = max(value, 0)

    @critical_damage.setter
    def critical_damage(self, value):
        self._critical_damage = max(value, 0)

    @life_steal.setter
    def life_steal(self, value):
        self._life_steal = max(value, 0)

    @turn_loss.setter
    def turn_loss(self, value):
        self._turn_loss = max(value, 0)

    @health_loss.setter
    def health_loss(self, value):
        self._health_loss = max(value, 0)

    @thorn_damage.setter
    def thorn_damage(self, value):
        self._thorn_damage = max(value, 0)

    @inv_turn_loss.setter
    def inv_turn_loss(self, value):
        self._inv_turn_loss = max(value, 0)

    def __init__(self, from_, to):
        self.from_ = from_
        self.to = to

    @property
    def total_damage(self):
        return self.physical_damage + self.magical_damage + self.real_damage + self.critical_damage + self.life_steal

    def do(self):
        self.from_.owner.attack_build_up(self)
        self.to.defence_build_up(self)

        self.to.damage(self, self.total_damage)
        self.from_.owner.heal(self, self.life_steal)
        self.from_.owner.damage(self, self.thorn_damage)

        self.to.turn_loss += self.turn_loss
        self.to.health_loss += self.health_loss

        self.from_.owner.turn_loss += self.inv_turn_loss
