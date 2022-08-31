from threading import Thread

import Signal


class Input(Signal.Signal):
    def __init__(self):
        super().__init__()
        self.c_manager = Commands()
        Thread(target=self.update, args=()).start()

    def update(self):
        user_input = input()

        while not self.c_manager.quit_command(user_input):
            command = self.c_manager.valide_command(user_input)
            if type(command) == str:
                self.raise_signal(command)

            user_input = input()


class Commands:
    def __init__(self):
        pass

    def check_commands(self, user_input, commands):
        if user_input.lower() in commands:
            return True
        return False

    def quit_command(self, user_input):
        commands = [
            "q", "exit", "esc", ":q", ":qa!"
        ]
        return self.check_commands(user_input, commands)

    def valide_command(self, user_input):
        commands = [
            ["undo", self.undo_command],
            ["redo", self.redo_commands]
        ]

        for c in commands:
            if self.check_commands(user_input, c[1]()):
                return c[0]
        return None

    def undo_command(self):
        commands = [
            "undo", "un"
        ]
        return commands

    def redo_commands(self):
        commands = [
            "redo", "re"
        ]
        return commands
