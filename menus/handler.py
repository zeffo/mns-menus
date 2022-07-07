from functools import wraps
from .command import Command, Context, HelpCommand, MenuCommand


class MissingRequiredArguments(Exception):
    """Raised when arguments are missing"""


class Handler:

    """Base class to handle commands and events"""

    commands = {"help": HelpCommand(), "menu": MenuCommand()}

    def error_handler(self, func):
        self._error_handler = func

    def _error_handler(self, ctx, exc):
        raise exc

    def __init__(self, *, prompt):
        self.prompt = prompt

    def add_command(self, command):
        self.commands[command.name] = command

    def command(self, usage=None):
        def wrapper(func):
            func.usage = usage
            self.add_command(Command(func, usage))
        return wrapper

    def handle(self, ctx, args):
        try:
            ctx.command(ctx, *args)
        except Exception as e:
            self._error_handler(ctx, e)

    def start(self):
        """Starts a loop to listen for commands"""
        while True:
            main = input(self.prompt)
            args = main.split()
            command = self.commands.get(args[0])
            if command:
                ctx = Context(self, command)
                self.handle(ctx, args[1:])
            else:
                self.commands['menu'](ctx)
