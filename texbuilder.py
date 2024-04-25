import os
import shutil
import time
from typing import Protocol, TypeVar

from addons import fm, read_file, write_file
from commands import CommandTemplate

TeXbuilder = TypeVar('TeXbuilder')

class TeXbuilder():
    """Create review section."""

    def __init__(self, title, init=False, config=None, head="", depth=-1, commands=[]):
        """Create Review instance."""
        self.init = init
        self.head = head
        self.depth = depth
        self.title = title
        self.config = config
        if init:
            self._config_validator()
        self.tabulators = self.head.replace("sub", "\t")
        print("{}- {}".format(self.tabulators, title))
        self.sections = {}
        self.commands = []
        self.queue = []

        self.document : str = config["file_path"]
        self.preload_alias : str = config['preload_alias']
        self.payload_alias : str = config["payload_alias"]
        self.postload_alias : str = config["postload_alias"]
        self.payload : str = ""
        self.constants : dict = config["constants"]
        self.templates : dict = config["templates"]

    def add_section(self, title, commands, *args, **kwargs):
        """Create instance of yourself and add to dict."""
        new_head = self.head + "sub"
        self.sections[title] = TeXbuilder(title, head=new_head, commands=commands, depth=self.depth + 1, config=self.config, *args, **kwargs)
        return self.sections[title]

    def apply_payloads(self, queue={}, last_section=''):
        if not queue:
            queue = self.sections
        for section, subsections in queue.items():
            section_name = "\\{}section{{{}}}\n\n{}\n\quad\n{}".format('sub' * subsections.depth, section,
                                                                       "%%PRE{}".format(section),
                                                                       self.postload_alias)
            self._update_doc(section_name)
            if len(subsections.sections) > 0:  # isinstance(commands, list):
                self.apply_payloads(subsections.sections, last_section=section)
            else:
                for command in subsections.commands:
                    self._update_doc(command.get_payload(), kind=command.kind, last_section=last_section)

    def _update_doc(self, payload: str, kind : str = '', last_section : str = '') -> None:
        content = read_file(self.document)
        loc = self.postload_alias
        # Inserting constants
        for constant, _content in self.constants.items():
            content = content.replace(constant, _content)
        if kind:
            template = read_file(self.templates[kind])
            for constant, _content in payload.items():
                template = template.replace(constant, _content)
            # payload = "{}\n{}".format(self.preload_alias, template)
            if payload['%%LOC'] == 'pre':
                loc = "%%PRE{}".format(last_section)
            else:
                template += "\n\n {}".format(self.postload_alias)
            payload = template

        content = content.replace(loc, payload)
        write_file(self.document, content)

    def _config_validator(self):
        if self.init:
            if not os.path.exists(self.config["folder"]):
                # self.config["folder"] = self.config["folder"] + "_{}".format(int(time.time()))
                os.makedirs(self.config["folder"])
        self.config["folder_path"] = os.path.abspath(self.config["folder"])
        _file = self.config["filename"] + self.config["ext"]
        self.config["file"] = _file
        self.config["file_path"] = os.path.join(self.config["folder_path"], _file)
        print("- Creating file {} in {}".format(fm(_file, "green"), fm(self.config["folder"])))
        shutil.copy(self.config['templates']["scheme"], self.config["file_path"])

    def build(self, dic : dict, obj : TeXbuilder):
        """Build recurrent document structure."""
        for section, value in dic.items():
            _obj = obj.add_section(section, value)
            if isinstance(value, dict):
                self.build(value, _obj)
            else:
                _obj.commands = value
                self.queue.append([section, value])

    def __repr__(self):
        """Make self.sections readable."""
        return repr("{} d={}".format(self.sections, self.depth))
