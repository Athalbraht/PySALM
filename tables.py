import pandas as pd
from scipy.stats import shapiro,chisquare
import numpy as np


from addons import fix_desc
from conf import tab_path

def chi3(values, v=False):
    chi, p = chisquare(values)
    if v:
        return chi, p, "$\\chi^2={};\\rho={}$".format(chi.round(2), p.round(2))
    else:
        return p

def eff(e, tp):
    if tp == 'chi2':
        crv = {
            "brak": 0.1,
            "słaba": 0.15,
            "umiarkowana": 0.25,
            "silna": 1,
        }
    elif tp == 'n':
        crv = {
            "brak": 0.3,
            "słaba": 0.5,
            "umiarkowana": 0.7,
            "silna": 1,
        }
    elif tp == 'corr':
        crv = {
            "brak": 0.3,
            "słaba": 0.5,
            "umiarkowana": 0.7,
            "silna": 1,
        }
    for i, j in crv.items():
        if j<e:
            continue
        else:
            return i
    return 'bardzo silna'


def corrtab(tab, ):
    tab = tab.round(3).astype(str)
    content = fix_desc(tab.to_latex(
        caption="Korelacja", position='h!'))
    prompt = " "
    return content, prompt,'aa'


def stattab(tab, ):
    tab = tab.round(3).astype(str)
    content = fix_desc(tab.to_latex(index=False,
                                    caption="Statystyka", position='h!'))
    prompt = " "
    return content, prompt,'to jest isidaiwfla'


def desctable(data):
    ttab = data.describe()
    tab = ttab.round(1).astype(str)
    col = tab.columns
    shapiro_col = {}
    for c in col:
        shapiro_col[c] = str(round(shapiro(data[c])[1], 3))
    shapiro_df = pd.DataFrame(shapiro_col, index=(['$\\rho$']))
    tab = pd.concat([tab, shapiro_df]).transpose()
    content = fix_desc(tab.to_latex(
        caption="Statystyki opisowe danych metrycznych, $\overline{x}$ - średnia, $\sigma$ - odchylenie standardowe, min i max - wartości minimalne i maksymalne, $Q_1$, $Q_2$, $Q_3$ - kwartyl dolny, środkowy oraz górny, $N$ - liczba badanych. $p$ jest wynikiem testu Shapiro-Wilka.",
        position='h!'))
    sel = ttab.loc[['mean', 'std', '50%']]
    prompt = ""
    for cl in sel:
        prompt += "Średnia wartość {}u wynosi {} z odchyleniem standardowym {} oraz medianą {}. ".format(cl, *sel[cl])
    return content, prompt, 'adw'


def powertable(powertab):
    powertab = powertab.loc[2:7].replace(np.nan, 0).astype(int).replace(0, '--').astype(str)
    content = fix_desc(powertab.to_latex(
        caption="Minimalna wielkość próby dla testu statystycznego Ti F o określonych stopniach swobody (ilości kategorii).", position='h!'))
    prompt = "Tabela przedstawia minimalną wielkość próby dla testu o mocy powyżej 0.8 dla różnych ilości kategorii (stopni swobody)."
    return content, prompt,'power'


def expandtable(data, col):
    tab1 = data[col].explode().value_counts()
    tab2 = (tab1 / len(data) * 100).round(1).astype(str) + "%"
    tab = pd.concat([tab1, tab2], axis=1, keys=['Liczba', "Częstość wyboru"])
    content = fix_desc(tab.to_latex(
        caption="Rozkład wyborów w pytaniu '{}'.".format(col), position='h!'))
    prompt = "Tabela wyborów w pytaniu: {}. Tabela:\n{}".format(col, tab.to_markdown())
    return content, prompt,'Et'


def counttable(data, col):
    """Generate list of count table for specific entry and crosstables if crosstab specified."""
    prompt = " "
    if isinstance(col, list):

        tab1 = data[col].apply(pd.Series.value_counts)
        chip = tab1.apply(chi3).round(3).astype(str)
        tab1 = tab1.transpose()
        tab2 = "(" + (tab1 / len(data) * 100).round(1).astype(str) + "\%)"
        tab = tab1.astype(str) + " " + tab2
        tab['$\\chi^2$'] = chip
        content = fix_desc(tab.to_latex(
            caption="Zestawienie ilościowe wartości w kolumnach", position='h!')
                           )
    else:
        tab1 = data[col].value_counts()
        tab2 = (data[col].value_counts(normalize=True) * 100).round(3).astype(str) + "\%"
        tab = pd.concat([tab1, tab2], axis=1, keys=['Liczebność', "Procent"]).sort_index()
        _mc = tab1.idxmax()
        mc = tab2.max()
        chi,p,ds = chi3(tab1,True)
        prompt = "Najczęsciej występującą wartością w tabeli {} jest '{}' ({}).".format(col, _mc, mc)
        if len(tab1.index) > 2:
            prompt += "Powmocnicza tabela:\n {}".format(tab.to_markdown())

        content = fix_desc(tab.to_latex(
            caption="Zestawienie ilościowe wartości w kolumnie {}. {}".format(col,ds), position='h!')
                           )
    return content, prompt,''
