from typing import Callable

from addons import fm
from commands import (AICommand, CommandTemplate, FileCommand, PlotCommand,
                      QueryCommand, StatisticCommand, TableCommand,
                      UnsupportedCommand)
from conf import structure
from texbuilder import Section


class CommandManager():
    """Loader class."""

    def __init__(self):
        self.commands : list[CommandTemplate] = []
        self.queue : list[CommandTemplate] = []
        self.last_id : int = 0
        self.mapping = {
            'file' : {
                'desc' : FileCommand,
                'table': FileCommand,
                'plot': UnsupportedCommand,
                'stat': UnsupportedCommand,
            },
            'gen' : {
                'desc' : AICommand,
                'table': TableCommand,
                'plot': PlotCommand,
                'stat': StatisticCommand,
            },
            'load' : {
                'desc' : QueryCommand,
                'table': QueryCommand,
                'plot': QueryCommand,
                'stat': QueryCommand,
            },
        }

    def create_id(self):
        self.last_id += 1
        return self.last_id

    def register(self, flg: str, kind: str, ctx: str, mode: str = 'static', loc: str = 'inline', *args, **kwargs) -> None:
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

        # SET METHOD

        command : CommandTemplate = FileCommand(**params)
        self.commands.append(command)

    def create_queue(self):
        """Define priority of instructions."""
        print("\t- Sorting instructions list")
        high = []
        medium = []
        low = []
        for i in self.commands:
            self.queue.append(i)
        high.extend(medium)
        high.extend(low)

    def execute_queue(self):
        print("\t- Executing analysis command")
        for command in self.queue:
            try:
                print("\t\t- Executing command: {}: ".format(command.id), end='')
                command.execute()
            except Exception as e:
                print(fm("Fail", 'red'))
                print("\t\t{}".format(e))
            else:
                print(fm("Pass", 'green'))


class Analysis:
    """Session analysis builder."""

    def __init__(self, tex_config: dict):
        """Session manager for analysis session."""
        self.structure : Callable
        self.command_manager : CommandManager = CommandManager()
        self.document : Section = Section("Report", config=tex_config, init=True)

    def register_commands(self):
        self.structure = structure(self.command_manager)

    def create_table_of_content(self):
        """Wrap tex build."""
        self.document.build(self.structure, self.document)

    def boost_commands(self):
        self.command_manager.create_queue()
        self.command_manager.execute_queue()

    def build_document(self):
        print('\t- Applying payloads & building document')
        self.document.apply_payloads(self.command_manager.commands)

    def queue_organizer(self, queue):
        """Organize analysis instruction based on priority of funcions."""
