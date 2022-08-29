import pygame

pygame.init()


class ConsoleItem:
    console = None

    def key(self, key):
        pass

    def start(self):
        pass

    def selected(self):
        pass

    def deselected(self):
        pass


class Button(ConsoleItem):
    def __init__(self, x, y, text, function, color=(255, 255, 255), pivot=0, *args, **kwargs):
        self.x = x
        self.y = y

        self.color = color

        self.pivot = pivot

        self.text = text
        if type(self.text) is not str:
            self.text = repr(self.text)

        self.selected_color = 50, 50, 50
        self.deselected_color = 0, 0, 0

        self.function = function
        self.args = args
        self.kwargs = kwargs

        self.select_function = lambda *args_: ()
        self.select_args = ()

        self.deselect_function = lambda *args_: ()
        self.deselect_args = ()

    def key(self, event):
        if event.key is pygame.K_RETURN:
            self.function(*self.args, **self.kwargs)

    def start(self):
        self.console.print(self.x, self.y, self.text, self.color, self.deselected_color, pivot=self.pivot)

    def selected(self):
        self.console.set_background(self.x, self.y, len(self.text), 1, self.selected_color, self.pivot)

        self.select_function(*self.select_args)
        self.console.update()

    def deselected(self):
        self.console.set_background(self.x, self.y, len(self.text), 1, self.deselected_color, self.pivot)

        self.deselect_function(*self.deselect_args)
        self.console.update()


class Input(ConsoleItem):
    def __init__(self, x, y, width, hint, variable, function, color=(255, 255, 255), hint_color=(150, 150, 150),
                 limit=True, *args, **kwargs):
        self.x = x
        self.y = y
        self.width = width

        self.hint = hint
        if type(self.hint) is not str:
            self.text = repr(self.hint)

        self.value = ""
        self.variable = variable

        self.function = function
        self.args = args
        self.kwargs = kwargs

        self.color = color
        self.hint_color = hint_color
        self.limit = limit

        self.variable.object = self

    def update(self):
        if self.value:
            if self.console.event_system.selection is self:
                self.console.print(self.x, self.y, self.value[max(len(self.value) - self.width, 0):], self.color,
                                   clear_width=self.width)

            else:
                self.console.print(self.x, self.y, self.value[:self.width], self.color, clear_width=self.width)

        else:
            self.console.print(self.x, self.y, self.hint, self.hint_color, clear_width=self.width)

        self.console.update()

    def key(self, event):
        if event.key == pygame.K_RETURN:
            self.function(*self.args, **self.kwargs)

        elif event.key == pygame.K_BACKSPACE:
            if not self.value:
                return

            self.value = self.value[:-1]
            self.update()

        else:
            if (not event.unicode.isprintable()) or self.limit and len(self.value) >= self.width:
                return

            self.value += event.unicode
            self.update()

    def start(self):
        self.update()

    def selected(self):
        self.console.set_background(self.x, self.y, self.width, 1, (50, 50, 50))
        self.update()

    def deselected(self):
        self.console.set_background(self.x, self.y, self.width, 1, (0, 0, 0))
        self.update()


class Variable:
    object = None

    def set(self, new):
        old = self.object
        self.object = new
        old.update()
        self.object.update()
        self.object.console.update()

    @property
    def value(self):
        return self.object.value

    @property
    def available(self):
        return self.object is not None

    def reset(self):
        self.object = None


class RadioButton(ConsoleItem):
    def __init__(self, x, y, text, variable, value):
        self.x = x
        self.y = y

        self.text = text
        if type(self.text) is not str:
            self.text = repr(self.text)

        self.variable = variable
        self.value = value

        if self.variable.object is None:
            self.variable.object = self

    def key(self, event):
        if event.key == pygame.K_RETURN:
            self.variable.set(self)

    def start(self):
        self.update()

    def update(self):
        self.console.print(self.x - 2, self.y, (">" if self.variable.object is self else " ") + " " + self.text)

    def selected(self):
        self.console.set_background(self.x, self.y, len(self.text), 1, (50, 50, 50))

    def deselected(self):
        self.console.set_background(self.x, self.y, len(self.text), 1, (0, 0, 0))


class Console:
    def __init__(self, size: int, width: int = None, height: int = None, flags: int = 0):
        self.font = pygame.font.SysFont("Courier New", size, True)

        desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]
        self.char_width, self.char_height = self.font.render("a", True, (0, 0, 0)).get_size()

        if width is None:
            width = desktop_width // self.char_width

        if height is None:
            height = desktop_height // self.char_height

        self.width = width
        self.height = height

        self.window = pygame.display.set_mode(self.real_size, flags)

        self.background_layer = pygame.Surface(self.real_size)
        self.front_layer = pygame.Surface(self.real_size, pygame.SRCALPHA)

        self.event_system = None

    def set_console(self, console_type, **kwargs):
        console = console_type(self, **kwargs)
        self.event_system = console

    @property
    def real_width(self):
        return self.width * self.char_width

    @property
    def real_height(self):
        return self.height * self.char_height

    @property
    def real_size(self):
        return self.real_width, self.real_height

    @property
    def size(self):
        return self.width, self.height

    def real_x(self, x):
        return x * self.char_width

    def real_y(self, y):
        return y * self.char_height

    def real_rect(self, x, y, width, height):
        return self.real_x(x), self.real_y(y), self.real_x(width), self.real_y(height)

    def clear_front_layer(self, x=0, y=0, width=None, height=None):
        if width is None:
            width = self.width

        if height is None:
            height = self.height

        self.front_layer.fill((0, 0, 0, 0), self.real_rect(x, y, width, height))

    def clear_back_layer(self, x=0, y=0, width=None, height=None):
        if width is None:
            width = self.width

        if height is None:
            height = self.height

        self.background_layer.fill((0, 0, 0), self.real_rect(x, y, width, height))

    def set_background(self, x, y, width, height, color, pivot=0):
        self.background_layer.fill(color, self.real_rect(x - int(pivot * width), y, width, height))

    def clear_screen(self, x=0, y=0, width=None, height=None):
        if width is None:
            width = self.width

        if height is None:
            height = self.height

        self.clear_front_layer(x, y, width, height)
        self.clear_back_layer(x, y, width, height)

    def update(self):
        self.window.blit(self.background_layer, (0, 0))
        self.window.blit(self.front_layer, (0, 0))

        pygame.display.update()

    def print(self, x, y, text, text_color=(255, 255, 255), background_color=None, clear_width=None,
              pivot: float | int = 0):
        if type(text) is not str:
            text = repr(text)

        x -= int(pivot * len(text))

        rect = x, y, len(text), 1
        if background_color is not None:
            self.set_background(*rect, background_color)

        surface = self.font.render(text, True, text_color)
        if clear_width is None:
            self.clear_front_layer(*rect)
        else:
            self.clear_front_layer(x, y, clear_width, 1)

        self.front_layer.blit(surface, (self.real_x(x), self.real_y(y)))

    def better_print(self, x, y, text, text_color=(255, 255, 255), background_color=None, clear_width=None, pivot=0):
        for item_no, item in enumerate(text.split("\n")):
            self.print(x, y + item_no, item, text_color, background_color, clear_width, pivot)

    def check_events(self):
        for event in pygame.event.get():
            self.event_system.check_event(event)


class EventSystem:
    console: Console = None

    def __init__(self, console, **kwargs):
        for name, value in kwargs.items():
            self.__setattr__(name, value)

        self.console = console
        self.start()

    def start(self):
        pass

    def check_event(self, event):
        pass


class SelectionEventSystem(EventSystem):
    selection_no = None
    items = None

    def quit_event(self):
        pass

    def back_event(self):
        pass

    def start(self):
        self.items = []
        self.console.clear_screen()

    def clear_items(self):
        self.items.clear()
        self.selection_no = None

    def add_item(self, item):
        item.console = self.console
        item.start()
        self.items.append(item)

        if self.selection_no is None:
            self.selection_no = 0
            item.selected()

    def add_items(self, items: list[ConsoleItem]):
        for item in items:
            self.add_item(item)

    @property
    def selection(self):
        return self.items[self.selection_no]

    def check_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_event()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back_event()
                return

            if event.key == pygame.K_DOWN:
                old = self.selection
                self.selection_no += 1

                if self.selection_no >= len(self.items):
                    self.selection_no = 0

                old.deselected()
                self.selection.selected()
                self.console.update()

            elif event.key == pygame.K_UP:
                old = self.selection
                self.selection_no -= 1

                if self.selection_no < 0:
                    self.selection_no = len(self.items) - 1

                old.deselected()
                self.selection.selected()
                self.console.update()

            else:
                self.selection.key(event)


class QuickDismissBox(EventSystem):
    event = None
    text = None
    x = 5
    y = 5

    text_color = 255, 255, 255
    background_color = 0, 0, 0

    press_key_text = "Press any key..."
    press_key_color = 150, 150, 150
    press_key_background_color = 0, 0, 0

    def start(self):
        if self.event is None:
            raise ValueError("event must be set when __init__ is called.")

        if self.text is None:
            raise ValueError("text must be set when __init__ is called.")

        self.console.clear_screen()
        self.console.set_console(SelectionEventSystem)
        self.console.better_print(self.x, self.y, self.text, self.text_color, self.background_color)

        self.console.print(self.console.width // 2, self.console.height - self.y, self.press_key_text,
                           self.press_key_color, self.press_key_background_color, pivot=0.5)
        self.console.update()

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.event()


class StoryDismissBox(EventSystem):
    event = None
    items = None
    x = 5
    y = 5
    item_no = 0

    text_color = 255, 255, 255
    text_background_color = 0, 0, 0

    press_key_text = "Press any key..."
    press_key_color = 150, 150, 150
    press_key_background_color = 0, 0, 0

    def start(self):
        if self.event is None:
            raise ValueError("event must be set when __init__ is called.")

        if self.items is None:
            raise ValueError("items must be set when __init__ is called.")

        self.console.clear_screen()
        self.print_next()

    def print_next(self):
        if self.item_no > len(self.items):
            raise ValueError("That should be impossible.")

        if self.item_no == len(self.items):
            self.event()
            return

        self.console.print(self.x, self.y + self.item_no, self.items[self.item_no],
                           self.text_color, self.text_background_color)

        self.item_no += 1

        self.console.print(self.x, self.y + self.item_no, self.press_key_text,
                           self.press_key_color, self.press_key_background_color)
        self.console.update()

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.print_next()
