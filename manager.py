from typing import Protocol

from addons import fm
from conf import structure
from texbuilder import Section


class OrderObject():

    def __init__(self, id: int, flg: str, kind: str, ctx: str, mode: str, loc: str):
        self.id = id
        self.flg = flg
        self.kind = kind
        self.ctx = ctx
        self.mode = mode
        self.loc = loc

        self.calculated : bool = False

    def execute(self):
        pass

    def __repr__(self):
        return "{}:{}:{}:{}:{}".format(
            self.id,
            self.flg,
            self.kind,
            self.ctx,
            self.mode,
            self.calculated
        )


class Loader():
    """Loader class."""

    def __init__(self):
        self.instructions = []
        self.queue = []
        self.last_id = 0
        """Translate user instructions to func execute type."""

    def create_id(self):
        self.last_id += 1
        return self.last_id

    def obj(self, flg, kind, ctx, mode='static', loc='inline', *args, **kwargs):
        """"""

        print("\t- Registering {} as {} for {} in {} mode".format(
            fm(kind),
            fm(flg, 'yellow'),
            fm(ctx, 'cyan'),
            fm(mode, 'red')))
        orderID = self.create_id()
        params = {
            "id" : orderID,
            "flg" : flg,
            "kind" : kind,
            "ctx" : ctx,
            "mode" : mode,
            "loc" : loc,
        }
        _obj = OrderObject(**params)
        self.instructions.append(_obj)
        return _obj

    def organize(self):
        """Define priority of instructions."""
        print("\t- Sorting instructions list")
        high = []
        medium = []
        low = []
        for i in self.instructions:
            self.queue.append(i)
        high.extend(medium)
        high.extend(low)

    def execute_queue(self):
        print("\t- Executing analysis instructions")
        for instruction in self.queue:
            try:
                print("\t\t- Executing command: {}: ".format(instruction.id), end='')
                instruction.execute()
            except Exception as e:
                print(fm("Fail", 'red'))
                print("\t\t{}".format(e))
            else:
                print(fm("Pass", 'green'))


class Session:
    """DOCssd."""

    def __init__(self, tex_config: dict):
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
