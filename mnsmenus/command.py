from inspect import signature
from typing import Callable


class Command:
    """Base class to represent a command"""

    def __init__(self, func: Callable, usage: str) -> None:
        self.func = func
        self.usage = usage

    @property
    def desc(self):
        return self.func.__doc__

    @property
    def name(self):
        return self.func.__name__

    def __str__(self):
        return self.func.__name__

    def __call__(self, *args):
        self.func(*args)

    @property
    def args(self):
        return len(signature(self.func).parameters) - 1

class HelpCommand(Command):
    """Default Help Command"""

    def __init__(self):
        self.func = self.help
        self.usage = "help (command)"

    @staticmethod
    def help(ctx, command):
        """Shows the help string for a command"""
        command = ctx.handler.commands.get(command)
        if command:
            print(f"{command.usage}\n{command.desc}")
        else:
            print("Could not find that command.")


class MenuCommand(Command):
    """Default Menu Command"""

    def __init__(self):
        self.func = self.menu
        self.usage = "menu"

    @staticmethod
    def menu(ctx):
        """Shows the command menu"""
        print(
            "\n".join(
                [
                    f"{i+1}. {c.name}: {c.desc}"
                    for i, c in enumerate(ctx.handler.commands.values())
                ]
            )
        )


class Context:
    """Command Context"""

    def __init__(self, handler, command):
        self.handler = handler
        self.command = command
