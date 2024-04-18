from click import style
from pandas import DataFrame

from alias import c
from conf import nominal_data, ordinal_data, quantitative_data, tab_path


def write_file(path: str, content: str) -> None:
    with open(path, 'w') as file:
        file.write(content)


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def fm(txt, color='green'):
    return style(txt, fg=color)


def cc(name):
    """Convert column name to short alias."""
    return list(c.keys())[list(c.values()).index('aaa')]


def type_detector(*aliases):
    """Detect data set type, create type alias and filename."""
    _alias = ''
    filename = ''
    for alias in aliases:
        name = c[alias]
        if name in nominal_data:
            _type = "nominal_data"
        elif name in ordinal_data:
            _type = "ordinal_data"
        elif name in quantitative_data:
            _type = 'quantitative'
        else:
            print(style("\t\tUndefined column name in config file: {}".format(name), fg="red"))
        _alias += _type[0]
        filename += alias
    return _alias, filename, _type


def make_alias_cheetsheet():
    """Create cheet sheet for data. Relates aliases with long name columns."""
    df = DataFrame({'Pełna nazwa': c.values()}, index=c.keys())
    print("- Creating alias cheetsheet")
    print("\t- latex")
    with open("{}/aliases.tex".format(tab_path), "w") as file:
        file.write(fix_desc(df.to_latex(
            caption="Zestawienie aliasów kodujących kolumny danych",
            label="tab:aliases", position="h!"
        )))
    print("\t- html")
    df.to_html("{}/aliases.html".format(tab_path))
    print("\t- excel")
    df.to_excel("{}/aliases.xlsx".format(tab_path))


def resolve_values(entry):
    """xD."""
    pass


def fix_desc(s):
    """Format pandas latex return."""
    s = s.replace('h!]', 'h!]\n\\centering')
    s = s.replace('%', '\%')
    s = s.replace('All', 'Wszystkie')
    s = s.replace('count', 'N')
    s = s.replace('mean', '$\overline{x}$')
    s = s.replace('std', '$\sigma(x)$')
    s = s.replace('min', '$\min(x)$')
    s = s.replace('max', '$\max(x)$')
    s = s.replace('25\%', '$Q_1$')
    s = s.replace('50\%', '$Q_2$')
    s = s.replace('75\%', '$Q_3$')
    s = s.replace('proportion', 'Udział [\%]')
    return s
