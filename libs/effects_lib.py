class Effect:
    def __init__(self, owner):
        self.owner = owner
        self.start()

    def start(self):
        pass

    def at_turn(self):
        pass

    def at_attack(self):
        pass

    def at_defence(self):
        pass
