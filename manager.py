from texbuilder import Section
from conf import structure


class Loader():
    """Loader class."""

    def __init__(self):
        """Translate user instructions to func execute type."""

    def obj(self, flg, kind, ctx, mode, loc, *a, **kwargs):
        """"""
        f = 'file'
        l = 'load'
        g = 'gen'

        t = 'table'
        p = 'plot'
        d = 'plot'

        nr = 'random'
        nu = 'uniqe'
        ng = 'global'
        ns = 'static'
        np = 'paraphrase'
        pass



class Session:
    """DOCssd."""

    def __init__(self, tex_config):
        """Session manager for analysis session."""
        self.loader = Loader()
        self.document = Section("Report", config=tex_config, init=True)
        self.structure = structure(self.document, self.loader)

    def create_table_of_content(self):
        """Wrap tex build."""
        self.document.build(self.structure, self.document)

    def queue_organizer(self, queue):
        """Organize analysis instruction based on priority of funcions."""
