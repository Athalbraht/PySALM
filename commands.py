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

    def __repr__(self):
        return "{}:{}:{}:{}:{}".format(
            self.id,
            self.flg,
            self.kind,
            self.ctx,
            self.mode,
        )

    def get_payload(self):
        """Return result in tex format"""
        ...

    def execute(self):
        """Execute instructions and save to prepare payload later."""
        ...

    def description(self):
        ...

    def add_func_reference(self):
        ...

    def mode(self):
        ...


class UnsupportedCommand(CommandTemplate):
    def execute(*args, **kwargs) -> None:
        print("\t\t- Unsupported command, skipping...")
        raise Warning('Unsupported operation')
        return None


# available mode options
# - 'random'       # choice randomly from database
# - 'uniqe'        # always regenerate description
# - 'global'       # use global setting
# - 'static'       # AI support disabled, using default values
# - 'paraphrase'   # paraphrase existing description

class FileCommand(CommandTemplate):
    def execute(self):
        content = self.open_file()

    def open_file(self) -> str:
        with open(self.ctx, 'r') as file:
            return file.read()


class StatisticCommand(CommandTemplate):
    def execute(self):
        ...


class TableCommand(CommandTemplate):
    def execute(self):
        ...


class PlotCommand(CommandTemplate):
    def execute(self):
        ...


class AICommand(CommandTemplate):
    def execute(self):
        ...


class QueryCommand(CommandTemplate):
    def execute(self):
        ...
