import pandas as pd
from conf import tab_path
from addons import fix_desc


def table_gen(data, name, col, crosstabs=[], aliases=[]):
    """Generate list of count table for specific entry and crosstables if crosstab specified."""
    print('\t - Generating {} tables'.format(name))
    tables = []
    tab1 = data[col].value_counts()
    tab2 = (data[col].value_counts(normalize=True) * 100).round(2)
    tab = pd.concat([tab1, tab2], axis=1).sort_index()
    tables.append(tab)
    tab = tab.astype(str).to_latex(
        caption="Zestawienie ilościowe wartości w kolumnie {}".format(col), position='h!')
    with open('{}/{}.tex'.format(tab_path, name), 'w') as file:
        file.write(fix_desc(tab))
    if len(crosstabs) > 0:
        for i, crosstab in enumerate(crosstabs):
            tab = (pd.crosstab(data[col], data[crosstab], margins=False, normalize=True) * 100).round(1)
            tables.append(tab)
            tab = (tab.astype(str) + "%").to_latex(
                caption="Tabela krzyżowa zależności {} między {}".format(col, crosstab), label="crosstab:{}-{}"
                .format(name, aliases[i]), position="h!")
            with open('{}/crosstab-{}-{}.tex'.format(tab_path, name, aliases[i]), 'w') as file:
                file.write(fix_desc(tab))
