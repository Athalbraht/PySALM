import pandas as pd

from addons import fix_desc
from conf import tab_path
from scipy.stats import shapiro


def desctable(data):
    tab = data.describe().round(1).astype(str)
    col = tab.columns
    shapiro_col = {}
    for c in col:
        shapiro_col[c] = str(round(shapiro(data[c])[1], 3))
    shapiro_df = pd.DataFrame(shapiro_col, index=(['$\\rho$']))
    tab = pd.concat([tab, shapiro_df]).transpose()
    content = fix_desc(tab.to_latex(
        caption="Statystyki opisowe danych metrycznych, $\overline{x}$ - średnia, $\sigma$ - odchylenie standardowe, min i max - wartości minimalne i maksymalne, $Q_1$, $Q_2$, $Q_3$ - kwartyl dolny, środkowy oraz górny, $N$ - liczba badanych. Shapiro $p$ jest wynikiem testu Shapiro-Wilka.",
        position='h!'))
    prompt = "powyższa tabela przedstawia statystyki opisowe dla kolumn {}. {}".format(list(tab.index), tab.to_markdown())
    return content, prompt


def powertable(powertab):
    content = fix_desc(powertab.to_latex(
        caption="Minimalna wielkość próby dla testu statystycznego o określonych stopniach swobody (kategorii).", position='h!'))
    prompt = "Tabela przedstawia minimalną wielkość próby dla testu o mocy powyżej 0.8 dla różnych ilości kategorii (stopni swobody)."
    return content, prompt


def crosstab(data, col):
    """Generate list of count table for specific entry and crosstables if crosstab specified."""
    if isinstance(col, list):
        pass
    else:
        tab = (pd.crosstab(data[col], data[col], margins=True, normalize=True) * 100).round(1)
    tables.append(tab)
    tab = (tab.astype(str) + "%").to_latex(
        caption="Tabela krzyżowa zależności {} między {}".format(col, crosstab), label="crosstab:{}-{}"
        .format(name, aliases[i]), position="h!")
    return content


def expandtable(data, col):
    tab1 = data[col].explode().value_counts()
    tab2 = (tab1 / len(data) * 100).round(1).astype(str) + "%"
    tab = pd.concat([tab1, tab2], axis=1, keys=['Liczba', "Częstość wyboru"])
    content = fix_desc(tab.to_latex(
        caption="Rozkład wyborów w pytaniu '{}'.".format(col), position='h!'))
    prompt = "Tabela wyborów w pytaniu: {}. Tabela:\n{}".format(col, tab.to_markdown())
    return content, prompt


def counttable(data, col):
    """Generate list of count table for specific entry and crosstables if crosstab specified."""
    if isinstance(col, list):
        tab1 = data[col].apply(pd.Series.value_counts).transpose()
        tab2 = "(" + (tab1 / len(data) * 100).round(1).astype(str) + "%)"
        tab = tab1.astype(str) + " " + tab2
    else:
        tab1 = data[col].value_counts()
        tab2 = (data[col].value_counts(normalize=True) * 100).round(3).astype(str) + "%"
        tab = pd.concat([tab1, tab2], axis=1, keys=['Liczebność', "Procent"]).sort_index()

    content = fix_desc(tab.to_latex(
        caption="Zestawienie ilościowe wartości w kolumnie {}".format(col), position='h!'))
    prompt = "Zliczenia w kolumnie {}. Tabela\n{}".format(col, tab.to_markdown())
    return content, prompt
