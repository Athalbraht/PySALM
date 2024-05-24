import numpy as np
from click import style
from pandas import DataFrame

from alias import c
from conf import nominal_data, ordinal_data, quantitative_data, tab_path

def split_sentence(text, n=40):
    lines = []
    curr_line = []
    for char in text:
        curr_line.append(char)
        if len(curr_line) >= n and char == ' ':
            lines.append(''.join(curr_line))
            curr_line = []

    if curr_line:
        lines.append(''.join(curr_line))
    return '\\\\\hspace{0.4cm}'.join(lines)

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


def type_detector(names, alias=False):
    """Detect data set type, create type alias and filename."""
    types = []
    for name in names:
        if alias:
            name = c[name]
        if name in nominal_data:
            _type = "n"
        elif name in ordinal_data:
            _type = "o"
        elif name in quantitative_data:
            _type = 'q'
        else:
            print("Undefined column name in config file: {}".format(fm(name, 'red')))
            exit()
        types.append(_type)
    return "".join(types)


def make_poll_tab(df, cols):
    # types[value_counts][explode][types]
    types = {
            'Wielokrotny wybór:' : (True, True, [list]),
            'Wybór:' :(True, False, [str]),
            'Wartość liczbowa' : (False, False, [np.int64, np.float64]),
            }
    print("- Creating poll table (apx)", end='')
    columns, values = [], []
    for col in cols:
        added = False
        for k,v  in types.items():
            for tp in v[2]:
                if isinstance(df[col].dropna().iloc[0], tp):
                    columns.append(col)
                    values.append(k)
                    added = True
                    if v[0]:
                        if v[1]:
                            val_count = list(df[col].dropna().explode().value_counts().index)
                        else:
                            val_count = list(df[col].dropna().value_counts().index)
                        for choice in val_count:
                            columns.append('')
                            values.append(f'- {choice}')
        if not added:
            columns.append(col)
            values.append('Nieznany')
    poll = DataFrame({'Pytanie':columns, "Typ odpowiedzi":values})
    print(fm('Done'))
    #return poll.to_latex(index=False, longtable=True)
    return poll.to_html('poll.html')


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
    df.to_html("aliases.html".format(tab_path))
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
    s = s.replace('min ', '$\min(x)$ ')
    s = s.replace('max ', '$\max(x)$ ')
    s = s.replace('25\%', '$Q_1$')
    s = s.replace('50\%', '$Q_2$')
    s = s.replace('75\%', '$Q_3$')
    s = s.replace('proportion', 'Udział [\%]')
    return s
