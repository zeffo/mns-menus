from inspect import signature, Parameter
from typing import Callable, Optional

class ConversionFailure(Exception):
    """ Raised when a parameter could not be converted """

class Command:
    """Base class to represent a command"""

    def __init__(self, func: Callable, usage: Optional[str]=None) -> None:
        self.func = func
        self.usage = usage or f"{func.__name__}: {func.__doc__}"

    @property
    def desc(self):
        return self.func.__doc__

    @property
    def name(self):
        return self.func.__name__

    def __str__(self):
        return self.func.__name__

    def convert(self, args):
        c_args = []
        for given, anno in zip(args, signature(self.func).parameters.values()):
            if anno.kind == Parameter.VAR_POSITIONAL:
                return [anno.annotation(arg) for arg in args] if anno.annotation is not anno.empty else args
            conv = given
            if anno.annotation is not anno.empty:
                try:
                    conv = anno.annotation(given)
                except Exception:
                    raise ConversionFailure(str(anno.annotation))
            c_args.append(conv)
                
        return c_args
        

    def __call__(self, *args):
        self.func(*self.convert(args))

    @property
    def args(self):
        return len(signature(self.func).parameters) - 1


class HelpCommand(Command):
    """Default Help Command"""

    def __init__(self):
        self.func = self.help
        self.usage = "help (command)"

    @staticmethod
    def help(ctx, command=None):
        """Shows the help string for a command"""
        if not command:
            return ctx.handler.commands.get("menu")(ctx)
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
