import pandas as pd
from scipy.stats import shapiro, chisquare
import numpy as np


from addons import fix_desc, split_sentence
from conf import tab_path


def chi3(values, v=False):
    chi, p = chisquare(values)
    if v:
        pp = str(p.round(2))
        if pp == '0.0':
            pp = '$p\\ll\\alpha$'
        else:
            pp = f'p={pp}'
        ds = "$\\chi^2={};{}$".format(chi.round(2), pp)
        return chi, p, ds
    else:
        return p


def eff_t(x, con):
    trans = {
        "słaba": 'W',
        "umiarkowana": "M",
        "silna": "S",
        "b. silna": "SS",
    }
    if con:
        return trans[x]
    return x


def eff(e, tp, short=False):
    if tp == 'chi2':
        crv = {
            "słaba": 0.3,
            "umiarkowana": 0.5,
            "silna": 0.7,
        }
    elif tp == 'n':
        crv = {
            "słaba": 0.3,
            "umiarkowana": 0.5,
            "silna": 0.7,
        }
    elif tp == 'corr':
        crv = {
            "słaba": 0.3,
            "umiarkowana": 0.5,
            "silna": 0.7,
        }
    for i, j in crv.items():
        if j < e:
            continue
        else:
            return eff_t(i, short)
    return eff_t('b. silna', short)


def corrtab(tab):
    tab = tab.round(3).astype(str)
    # col = [ (split_sentence(c[0], 25), c[1]) for c in list(tab.columns) ]
    # tab.columns = pd.MultiIndex.from_tuples(col)
    content = fix_desc(tab.to_latex(
        caption="Macierz korelacji", position='h!'))
    prompt = " "
    return content, prompt, 'aa'


def stattab(tab):
    # tab struct: tab [data/info] info: (ttype, [colname, [colsub]], ...)
    # adding APA-like headers
    ttype = 'chi2'
    columns = list(tab[0].columns)
    header = [[split_sentence(tab[1][1][0], n=25), columns[0]]]
    gcolumns = []

    if 'chi' not in tab[1][0]:
        gcolumns = list(tab[1][1][1])
        ttype = 'n'

    underline = "} \\\\\n  "  # fake end row } \\ -> newline -> cmidrule
    for cmid in range(len(gcolumns)):
        underline += f"\\cmidrule(r){{{2 + cmid * 2}-{3 + cmid * 2}}} "  # add cmidrule(r){colsub_pos}a
    underline += f"\\cmidrule(r){{{4 + (len(gcolumns) - 1) * 2}-{6 + (len(gcolumns) - 1) * 2}}}%X%"  # cmidrule for tests (3x) & mark4f&r

    for gc, gcolumn in enumerate(gcolumns):
        header.append([gcolumn, columns[1 + gc * 2]])  # create MultiIndex entry 4 subcol, gc*step (mean,std)
        header.append([gcolumn, columns[1 + gc * 2 + 1]])

    for column in columns[1 + (len(gcolumns) - 1) * 2 + 2::]:  # same by for the rest of cols (tests)
        header.append([tab[1][0] + underline, column])  # entry for test + fake endline4cmidrule

    header = pd.MultiIndex.from_tuples(header)
    tab[0].columns = header
    tab[0][header[0]] = tab[0][header[0]].apply(split_sentence, args=[25])

    tab[0] = tab[0].round(3).astype(str)
    tab[0][header[-1]] = tab[0][header[-1]].apply(lambda x: f'({eff(float(x), ttype, True)}) {x}')  # add eff_size mark (W)0.2
    tab[0] = tab[0].apply(lambda x: '\\centered{' + x + '}')  # center cells
    content = fix_desc(tab[0].to_latex(index=False,
                                       caption="Testy statystyczne dla {} hipoteza N".format(tab[1][1][0]), position='h!'))
    prompt = " "
    return content, prompt, 'to jest isidaiwfla'


def desctable(data):
    ttab = data.describe()
    tab = ttab.round(1).astype(str)
    col = tab.columns
    shapiro_col = {}
    for c in col:
        shapiro_col[c] = str(round(shapiro(data[c])[1], 3))
    shapiro_df = pd.DataFrame(shapiro_col, index=(['$\\rho$']))
    tab = pd.concat([tab, shapiro_df]).transpose()
    tab.index = [split_sentence(idx, 35) for idx in list(tab.index)]
    tab['count'] = tab['count'].astype(float).astype(int)
    content = fix_desc(tab.to_latex(
        caption=("Statystyki opisowe, $\overline{x}$ - średnia, $\sigma$ - odchylenie standardowe, min i max - wartości minimalne i maksymalne, $Q_1$, $Q_2$, $Q_3$ - kwartyl dolny, środkowy oraz górny, $N$ - liczba badanych. $p$ jest wynikiem testu Shapiro-Wilka.", "Statystyki opisowe"),
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
    return content, prompt, 'power'


def expandtable(data, col):
    try:
        data[col] = data[col].dropna().apply(lambda x: eval(x))
    except:
        pass
    n = len(data[col].dropna())
    tab1 = data[col].explode().value_counts()
    tab_s = (data[col].explode().value_counts(normalize=True).cumsum() * 100).round(1).astype(str) + "%"
    tab2 = (tab1 / len(data) * 100).round(1).astype(str) + "%"
    tab = pd.concat([tab1, tab2, tab_s], axis=1, keys=[f'Ilość ($n={n}$)', "Częstość wyboru", "Suma"])
    resp = [split_sentence(idx) for idx in list(tab.index)]
    _col = split_sentence(col)
    tab[_col] = resp
    cols = list(tab.columns)
    tab = tab[[cols[-1]] + cols[:-1]]
    tab = tab.astype(str).apply(lambda x: '\\centered{' + x + '}')  # center cells
    content = fix_desc(tab.to_latex(index=False,
                                    caption="Rozkład wyborów w pytaniu '{}'.".format(col), position='h!'))
    prompt = "Tabela wyborów w pytaniu: {}. Tabela:\n{}".format(col, tab.to_markdown())
    return content, prompt, 'Et'


def crosstable(data, col, margins=True, **kwargs):
    x = [data[c] for c in col[0]]
    y = [data[c] for c in col[1]]
    tab1 = pd.crosstab(x, y, margins=margins, **kwargs).astype(str)
    tab2 = (pd.crosstab(x, y, margins=margins, normalize=True, **kwargs) * 100).round(1).astype(str)
    tab = tab1 + " (" + tab2 + "%)"

    index_name = split_sentence(tab.index.name)
    tab.index = [split_sentence(idx) for idx in list(tab.index)]
    tab.index.name = index_name
    tab.columns.name = split_sentence(tab.columns.name)

    tab = tab.apply(lambda x: '\\centered{' + x + '}')  # center cells
    content = fix_desc(tab.to_latex(
        caption=f'Tabela krzyżowa: {col[0][0]} względem {col[1][0]}', position='h!'))
    prompt = "Tabela krzyżowa"
    return content, prompt, ''


def pivottable(data, col):
    return "", "", ""


def counttable(data, col):
    """Generate list of count table for specific entry and crosstables if crosstab specified."""
    prompt = " "
    if isinstance(col, list):
        tab1 = data[col].dropna().apply(pd.Series.value_counts)
        _tab1 = tab1.copy()
        chip = tab1.apply(chi3).round(3).astype(str)
        chip2 = tab1.transpose().apply(chi3).round(3).astype(str)
        chip2['p'] = '-'
        # tab1['p ($\\chi^2$)'] = chip2
        tab1 = tab1.transpose()
        tab2 = "(" + (_tab1 / len(data) * 100).round(1).astype(str) + "%)"
        tab = tab1.astype(str) + " " + tab2.transpose()
        tab['p ($\\chi^2$)'] = chip
        _col = list(tab.columns)
        tab['N'] = [str(len(data[c].dropna())) for c in col]
        tab = tab.transpose()
        tab['p ($\\chi^2$)'] = chip2
        tab = tab.transpose()
        tab = tab.replace(np.nan, '-')
        tab = tab[['N'] + _col]
        tab.index = [split_sentence(idx) for idx in list(tab.index)]
        tab = tab.astype(str).apply(lambda x: '\\centered{' + x + '}')  # center cells
        content = fix_desc(tab.to_latex(
            caption=("Zestawienie ilościowe w wybranych kolumnach ", f"Liczebność: {col[0]}"), position='h!')
        )
    else:
        n = len(data[col].dropna())
        tab1 = data[col].dropna().value_counts()
        tab2 = (data[col].value_counts(normalize=True) * 100).round(1).astype(str) + "%"
        tab = pd.concat([tab1, tab2], axis=1, keys=[f'Ilość ($n={n}$)', "Procent"]).sort_index()
        _mc = tab1.idxmax()
        mc = tab2.max()
        chi, p, ds = chi3(tab1, True)
        prompt = "Najczęsciej występującą wartością w tabeli {} jest '{}' ({}).".format(col, _mc, mc)
        if len(tab1.index) > 2:
            prompt += "Powmocnicza tabela:\n {}".format(tab.to_markdown())

        _index_name = split_sentence(tab.index.name) + f"\\\\{ds}"
        resp = [split_sentence(idx) for idx in list(tab.index)]
        # tab.index.name = _index_name
        tab[_index_name] = resp
        cols = list(tab.columns)
        tab = tab[[cols[-1]] + cols[:-1]]
        tab = tab.astype(str).apply(lambda x: '\\centered{' + x + '}')  # center cells
        content = fix_desc(tab.to_latex(index=False,
                                        caption=(f"Zestawienie ilościowe wartości w kolumnie {col}", f"Liczebność: {col}"), position='h!')

                           )
    return content, prompt, ''
