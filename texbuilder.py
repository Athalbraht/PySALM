import os
import shutil
import time
from typing import Protocol, TypeVar

from addons import fm, read_file, write_file

Section = TypeVar('Section')


class TexObject(Protocol):
    """Tex Objext Interface."""

    def __init__(self, config):
        self.document : str = config["file_path"]
        self.preload_alias : str = config['preload_alias']
        self.payload_alias : str = config["payload_alias"]
        self.postload_alias : str = config["postload_alias"]
        self.payload : str = ""
        self.constants : dict = config["constants"]
        self.templates : dict = config["templates"]

    def get_payload(self, kind: str) -> str:
        template = read_file(self.templates[kind])
        return template.replace(self.payload_alias, )


class Description(TexObject):
    """Description class for tex files."""

    def __init__(self):
        """Create description area in tex file."""
        pass


class Graphic(TexObject):
    """Graphic class for tex files."""

    def __init__(self):
        """Create graphic object in tex file."""
        pass


class Table(TexObject):
    """Table class for tex files."""

    def __init__(self):
        """Create graphic object in tex file."""
        pass


class Section():
    """Create review section."""

    def __init__(self, title, init=False, config=None, head="", depth=0):
        """Create Review instance."""
        self.init = init
        self.head = head
        self.depth = depth
        self.title = title
        self.config = config
        if init:
            self._config_validator()
        self.tabulators = self.head.replace("sub", "\t")
        print("{}- Creating {}: {}".format(self.tabulators, self.head, title))
        self.sections = {}
        self.queue = []

        self.document : str = config["file_path"]
        self.preload_alias : str = config['preload_alias']
        self.payload_alias : str = config["payload_alias"]
        self.postload_alias : str = config["postload_alias"]
        self.payload : str = ""
        self.constants : dict = config["constants"]
        self.templates : dict = config["templates"]

    def add_section(self, title, *args, **kwargs):
        """Create instance of yourself and add to dict."""
        new_head = self.head + "sub"
        self.sections[title] = Section(title, head=new_head, depth=self.depth + 1, config=self.config, *args, **kwargs)
        return self.sections[title]


    def apply_payloads(self, queue=[]):
        if not queue:
            queue = self.queue

        for command in queue:
            if isinstance(command, list):
                self.apply_payloads(command)
            else: 
                content = read_file(self.document)
                # Inserting constants
                for constant, _content in self.constants.items():
                    content = content.replace(constant, _content)
                print('\t\t- Applying command: {}'.format(command.id))
                content = content.replace(self.postload_alias, "{}\n{}".format(self.preload_alias, command.get_payload()))
                write_file(self.document, content)

    def _config_validator(self):
        if self.init:
            if os.path.exists(self.config["folder"]):
                self.config["folder"] = self.config["folder"] + "_{}".format(int(time.time()))
            os.makedirs(self.config["folder"])
        self.config["folder_path"] = os.path.abspath(self.config["folder"])
        _file = self.config["filename"] + self.config["ext"]
        self.config["file"] = _file
        self.config["file_path"] = os.path.join(self.config["folder_path"], _file)
        print("- Creating file {} in {}".format(fm(_file, "green"), fm(self.config["folder"])))
        shutil.copy(self.config['templates']["scheme"], self.config["file_path"])

    def build(self, dic : dict, obj : Section):
        """Build recurrent document structure."""
        for section, value in dic.items():
            _obj = obj.add_section(section)
            if isinstance(value, dict):
                self.build(value, _obj)
            else:
                self.queue.append(value)

    def __repr__(self):
        """Make self.sections readable."""
        return repr(self.sections)
