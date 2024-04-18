from typing import Protocol


class CommandTemplate(Protocol):
    def __init__(self, id: int, flg: str, kind: str, ctx: str, mode: str, loc: str):
        self.id = id
        self.flg = flg
        self.kind = kind
        self.ctx = ctx
        self.mode = mode
        self.loc = loc
        self.calculated : bool = False

    def execute(self):
        print("\t\t- Executing")

    def description(self):
        ...

    def add_func_reference(self):
        ...

    def mode(self):
        ...

    def __repr__(self):
        return "{}:{}:{}:{}:{}".format(
            self.id,
            self.flg,
            self.kind,
            self.ctx,
            self.mode,
        )


class UnsupportedCommand(CommandTemplate):
    def unsupported(*args, **kwargs):
        raise Warning('Unsupported operation')


class FileCommand(CommandTemplate):
    def openfile(_file):
        with open(_file, 'r') as file:
            return file.read()


class StatisticCommand(CommandTemplate):
    ...


class TableCommand(CommandTemplate):
    ...


class PlotCommand(CommandTemplate):
    ...


class AICommand(CommandTemplate):
    ...


class QueryCommand(CommandTemplate):
    ...
