import os
from typing import Protocol

from addons import read_file
from conf import tex_config


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
        """Return result in tex format."""
        if self.calculated:
            return self.payload
        else:
            print("\t\t\t- Cannot return payload, not calculated ")
            return None
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
        self.calculated = True
        self.payload = read_file(os.path.join(tex_config['assets_folder'], self.ctx))


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
