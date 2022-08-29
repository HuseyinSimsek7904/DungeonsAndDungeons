from libs import console_lib, rooms_lib, entity_lib
import pygame


class Game:
    room = None

    def __init__(self):
        self.font_size = 40

        self.console = console_lib.Console(self.font_size, flags=pygame.FULLSCREEN)
        self.width, self.height = self.console.size

        self.player: entity_lib.Player | None = None

        self.jump_room(rooms_lib.MainMenu)

        self.username = console_lib.Variable()
        self.difficulty = console_lib.Variable()

    def jump_room(self, room_type):
        room = room_type(self)
        self.room = room
        self.room.start()

    def mainloop(self):
        while True:
            try:
                self.console.check_events()

            except KeyboardInterrupt:
                quit()
