import os
import time


class TexObject():
    """Tex Objext Interface."""

    def __init__(self):
        """Desc."""
        pass


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
        """Create table object in tex file."""
        pass


class Section():
    """Create review section."""

    def __init__(self, title, init=False, config=None, head=''):
        """Create Review instance."""
        self.init = init
        self.head = head
        self.title = title
        if config:
            self.config = config
            self._config_validator()
        if init:
            self._make_file()
        self.tabulators = self.head.replace('sub', '\t')
        print("{}- Creating {}section: {}".format(self.tabulators, self.head, title))
        self.subsections = {}
        self.queue = []

    def add_subsection(self, title, *args, **kwargs):
        """Create instance of yourself."""
        new_head = self.head + "sub"
        print("{}\t- {}section {} added".format(self.tabulators, new_head, title))
        self.subsections[title] = Section(title, head=new_head, config=self.config, *args, **kwargs)
        return self.subsections[title]

    def add_description(self, content):
        """Add section or object describtion."""
        print("{}\t\t - description added".format(self.tabulators))

    def add_object(self, content, caption=False):
        """Add object with caption."""
        print("{}\t\t - object added".format(self.tabulators))
        pass

    def _config_validator(self):
        if self.init:
            if os.path.exists(self.config['folder']):
                self.config['folder'] = self.config['folder'] + "_{}".format(int(time.time()))
            os.mkdir(self.config['folder'])
        self.config['abspath'] = os.path.abspath(self.config['folder'])
        self.config['file'] = os.path.join(self.config['folder'], self.config["filename"])

    def _make_file(self):
        with open('views/document.tex', 'r') as file:
            content = file.read()
            replaces = [
                "AUTHOR",
                "TITLE"
            ]
            for rp in replaces:
                content = content.replace(rp, self.config[rp])
        with open(self.config['file'], 'w') as report:
            report.write(content)

    def __repr__(self):
        """Make self.sections readable."""
        return repr(self.subsections)
