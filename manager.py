from addons import fm
from texbuilder import Section
from conf import structure
from typing import Protocol


class FlagStrategy(Protocol):
    def 



class Order():

    def __init__(self, flg, kind, ctx, mode, loc):
        self.flg = flg
        self.kind = kind
        self.ctx = ctx
        self.mode = mode
        self.loc = loc


class Loader():
    """Loader class."""

    def __init__(self):
        self.instructions = []
        self.queue = []
        """Translate user instructions to func execute type."""

    def open_file(self, ctx):
        pass

    def generate(self, ctx):
        pass

    def load(self, ctx):
        pass

    def obj(self, flg, kind, ctx, mode='static', loc='inline', *a, **kwargs):
        """"""

        print("\t- Registering {} as {} for {} in {} mode".format(fm(kind), fm(flg, 'yellow'), fm(ctx, 'cyan'), fm(mode, 'red')))
        self.instructions.append()

        if flg == 'file':
            self.open_file(ctx)
        elif flg == 'load':
            self.load(ctx)
        elif flg == 'gen':
            self.generate(ctx)

        if kind == 'desc':
            pass
        elif kind == 'plot':
            pass
        elif kind == 'table':
            pass

        return tex_order
        nr = 'random'
        nu = 'uniqe'
        ng = 'global'
        ns = 'static'
        np = 'paraphrase'
        pass

    def organize(self):
        """Define priority of instructions."""
        print("\t- Sorting instructions list")
        high = []
        medium = []
        low = []
        for i in self.instructions:
            :
            pass
        high.extend(medium)
        high.extend(low)
        self.queue = high


class Session:
    """DOCssd."""

    def __init__(self, tex_config):
        """Session manager for analysis session."""
        self.loader = Loader()
        self.document = Section("Report", config=tex_config, init=True)
        self.structure = structure(self.loader)

    def create_table_of_content(self):
        """Wrap tex build."""
        self.document.build(self.structure, self.document)

    def boost_instructions(self):
        self.loader.organize()
        self.loader.execute_queue()

    def queue_organizer(self, queue):
        """Organize analysis instruction based on priority of funcions."""
