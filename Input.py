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
                self.raise_signal(command, user_input)

            user_input = input()


class Commands:
    def __init__(self):
        pass

    def check_command(self, user_input, command):
        if user_input.lower().split()[0] == command:
            return True
        return False

    def quit_command(self, user_input):
        commands = [
            "q", "exit", "esc", ":q", ":qa!"
        ]
        if user_input.lower() in commands:
            return True
        return False

    def valide_command(self, user_input):
        commands = [
            "undo",
            "redo",
            "create",
            "save"
        ]

        for command in commands:
            if self.check_command(user_input, command):
                return command
        return None
