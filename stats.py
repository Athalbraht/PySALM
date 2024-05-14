import numpy as np
import scipy as sp
import statsmodels.stats.power as smp
from addons import fm
from click import style
from pandas import DataFrame, crosstab

from tables import eff
from conf import crv, pval, tests_tab, corr_tab, tex_config, type_dict


def make_stat(comm, df, c1, c2, power, mode='safe', passed=True,verb=True):
    ddf, cr = auto_test(df, c1, c2, type_dict, power)
    if passed:
        ddf = ddf[(ddf['p'] < 0.05)]

    tables,pm = tests_tab(ddf)
    corr = corr_tab(cr)
    commands = []
    id = "{}-{}".format(c1[0], c2[0])
    for i,tab in enumerate(tables):
        if len(tab) > 0:
            commands.append(comm.register('gen', 'autostatable', [tab,pm[i]], mode='reload', alias=id + "A"))
            if verb:
                commands.append(comm.register('gendesc', 'desc', id + "A", mode=mode, alias=id + "B"))

    if len(corr) > 0:
        commands.append(comm.register('gen', 'corrtable', corr, mode='reload', alias=id + "C"))
        if verb:
            commands.append(comm.register('gendesc', 'desc', id + "C", mode=mode, alias=id + "CC"))
    return commands


def auto_test(data : DataFrame, groups: list, values: list, type_dict: dict, min_n: DataFrame, dep : str = 'ind', debug=False, debug_corr=False) -> DataFrame:
    group_q, group_o = [], []
    values_q, values_o = [], []
    test_map = {
        'n' : {
            'ind': {
                '2' : {
                    'n': {
                        'norm' : [chi2, 'chi2', '$\\chi^2$', 'chi2'],
                    },
                    'o': {
                        'norm' : [mannwhitneyu, "F", "Manna-Whitneya", 'n'],
                    },
                    'q': {
                        'norm': [ttest, "F", 'T', 'n'],
                        'rm': [mannwhitneyu, "F", "Manna-Whitneya", 'n'],
                    },
                },
                '3': {
                    'n': {
                        'norm' : [chi2, "chi2", "$\\chi^2$", 'chi2'],
                    },
                    'o': {
                        'norm' : [kruskal, "F", 'Kruskal-Wallis', 'n'],
                    },
                    'q': {
                        'norm': [anova, "F", "ANOVA", 'n'],
                        'rm': [kruskal, "F", "Kruskala-Wallisa", 'n'],
                    },
                },
            },
            'dep' : {
                '2': {
                    'n' : [],
                    'o' : [],
                    'q' : {
                        'norm' : [],
                        'rm' : [],
                    },
                },
                '3': {
                    'n' : [],
                    'o' : [],
                    'q' : {
                        'norm' : [],
                        'rm' : [],
                    },
                },
            }
        },
        'o' : {
            'o' : [spearman, 'Rs', 'R Spearman'],
            'q' : [spearman, 'Rs', "R Spearman"],
        },
        'q' : {
            'o' : [spearman, "Rs", "R Spearman"],
            'q' : [pearson, "Rp", "R Pearson"],
        },
    }

    df_struct = {
        'groups' : [],
        'values' : [],
        'ttype' : [],
        'headers' : [],
        'data' : [],
        'fixed_col' : [],
        'pass' : [],
        'e_size' : [],
        'p' : [],
        'tname' : [],
        'stat' : [],
        'efekt' : [],
    }

    def type_detect(x):
        for i in type_dict:
            if x in type_dict[i]:
                return i

    def fix_size(gsize, test_type='chi2'):  # change alg.
        prelen = len(gsize)
        _min = min_n[test_type][prelen]
        gsize = gsize[gsize > _min]
        gsize.dropna(inplace=True)
        if len(gsize) != prelen:
            print('Usunięto kategorie: {} - {}'.format(_groups, _values))
        return list(gsize.index)

    df = DataFrame(df_struct, dtype='object')
    corr_groups = []
    corr_values = []
    for _groups in groups:
        corr_groups.append(_groups)
        for _values in values:
            try:
                if debug:
                    import pdb
                    pdb.set_trace()
                print("- Calculating stat for  {} - {}".format(fm(_groups), fm(_values)))
                gtype = type_detect(_groups)
                vtype = type_detect(_values)
                tdata = data[[_groups, _values]]
                sub = 'norm'
                if gtype == 'n' or gtype == 'o':
                    if vtype in ['q', 'o']:
                        gsize = tdata.groupby(_groups).count()
                        fixed_col = fix_size(gsize, test_type='F')
                        tdata = tdata[tdata[_groups].isin(fixed_col)]
                        data_list = [tdata[tdata[_groups] == cat][_values] for cat in fixed_col]
                        if vtype == 'q':
                            flat = []
                            for i in data_list:
                                flat += i.to_list()
                            _, p = sp.stats.shapiro(flat)
                            if p < 0.05:
                                sub = 'rm'
                            values_q.append(vtype)
                        elif vtype == 'o':
                            values_o.append(vtype)
                    elif vtype == 'n':
                        tdata = crosstab(tdata[_groups], tdata[_values])
                        tdata[tdata > 5].dropna(inplace=True)
                        fixed_col = list(tdata.columns)
                        data_list = [tdata]

                    else:
                        print("Nieznany typ {} - {} ".format(_groups, _values))
                    if len(fixed_col) < 2:
                        print('Za mało danych: {} - {}'.format(_groups, _values))
                        continue

                    if len(fixed_col) == 2:
                        struct = test_map['n'][dep]['2'][vtype]
                    else:
                        struct = test_map['n'][dep]['3'][vtype]

                    ttype = struct[sub][1]
                    tname = struct[sub][2]
                    result, dd, stat, p, ef = struct[sub][0](*data_list)
                    eff_type = struct[sub][3]
                    _pass = False
                    if p < 0.05:
                        _pass = True

                    df.loc[len(df) + 1] = [_groups, _values, ttype, result, dd, fixed_col, _pass, ef, p, tname, stat, eff(ef, eff_type)]
                    corr_values.append(_values)
                elif gtype == 'q':
                    group_q.append(gtype)
                elif gtype == 'o':
                    group_o.append(gtype)

            except Exception as e:
                print("- {} in {} {}\n{}".format(fm('Error', "red"), _groups, _values, e))
    print('- Calculating correlations')
    df_corr = DataFrame({
        "X" : [],
        'Y' : [],
        '$\\rho$' : [],
        'p' : [],
        'method' : [],
        'result' : [],
        'Skala efektu' : [],
    })

    if debug_corr:
        import pdb
        pdb.set_trace()
    for group in corr_groups:
        for value in values:
            try:

                gtype = type_detect(group)
                vtype = type_detect(value)
                gr = data[group]
                vl = data[value]
                if gtype == 'q' and vtype == 'q':
                    corr, p = pearson(gr, vl)
                    print('calc pearson')
                    df_corr.loc[len(df_corr) + 1] = [group, value, corr['rPearson'], p, 'R-Pearson', corr, eff(corr['rPearson'], 'corr')]
                elif gtype != 'n' and vtype != 'n' and gtype != 'multi' and vtype != 'multi':
                    if vtype == 'o':
                        vl = vl.apply(lambda x: int(str(x).split('.')[0]))
                    if gtype == 'o':
                        gr = gr.apply(lambda x: int(str(x).split('.')[0]))
                    print('calc spearman')
                    corr, p = spearman(gr, vl)
                    df_corr.loc[len(df_corr) + 1] = [group, value, corr['rSpearman'], p, 'R-Spearman', corr, eff(corr['rSpearman'], 'corr')]
            except Exception as e:
                print('Error {} {}'.format(group, value))
                print(e)
                import pdb
                pdb.set_trace()

    return df, df_corr

# relation
# reg params B-wsp niestandarysow, se-bladstd, beta-wsp stand., t-wyiktestu

# q q rperson

# o o sperman

# n n niezaleznosc chi V Cramera

# o q rhosperman

# n q sprawdzic zwiazek

# n o z chi2 niezaleznosc

# tests

# 2x ind
# nn chi2
# oo t U Manna-Whitneya + n
# qq T + dCohenen/Test U Manna-Whitneya + n
# 3x ind
# nn chi
# oo t Kruskala-Wallisa + n
# qq 1cz ANOVA +n /  Kruskala-Wallisaa +n

# 2x dep
# nn t Cochrana
# oo t Wilcoxona + r
# qq Tdep + dCoh / Wilcoxona
# 3x dep
# nn Test Cochrana
# oo  Friedemana + w
# qq analiza wariacji wew /  Friedemana


def chi3(values, v=False):
    chi, p = sp.stats.chisquare(values)
    if v:
        return chi, p, "$\\chi^2={};\\rho={}$".format(chi.round(2), p.round(2))
    else:
        return p


def spearman(ct1, ct2):
    stat, p = sp.stats.pearsonr(ct1, ct2)
    result = {
        "rSpearman" : stat,
        "p" : p,
    }
    return result, p


def pearson(ct1, ct2):
    stat, p = sp.stats.pearsonr(ct1, ct2)
    result = {
        "rPearson" : stat,
        "p" : p,
    }
    return result, p


def anova(*ct):
    stat, p = sp.stats.f_oneway(*ct)
    group_means = [np.mean(i) for i in ct]
    overall_mean = np.mean(np.concatenate(ct))
    ss_between = sum([len(group) * (mean - overall_mean)**2 for group, mean in zip(ct, group_means)])
    ss_total = sum((value - overall_mean)**2 for group in ct for value in group)

    data = []
    headers = []
    for i, _set in enumerate(ct):
        headers.append("$\\overline{{x_{}}}$".format(i + 1))
        data.append(np.mean(_set))
        headers.append("$\\sigma_{}$".format(i + 1))
        data.append(np.std(_set))

    es = abs(ss_between / ss_total)
    headers += ['F', 'p', "$\\eta^2$"]
    data += [stat, p , es]
    return data, headers, stat, p, es


def chi2(ct):
    ct = np.array(ct)
    stat, p, dff, exp = sp.stats.chi2_contingency(ct)
    cramerv = abs(np.sqrt((stat / ct.sum()) / (min(ct.shape) - 1)))
    headers = [
        "$\\chi^2$",
        "p",
        "$V_c$",
    ]
    data = [
        stat,
        p,
        cramerv
    ]
    return data, headers, stat, p, cramerv


def ttest(ct1, ct2):
    stat, p = sp.stats.ttest_ind(ct1, ct2)
    dm = ct1.mean() - ct2.mean()
    pooled_std = np.sqrt(((len(ct1) - 1) * np.var(ct1) + (len(ct2) - 1) * np.var(ct2)) / (len(ct1) + len(ct2) - 2))
    es = abs(dm / pooled_std)
    headers = [
        "$\\overline{x_1}$",
        "$\\sigma_1$",
        "$\\overline{x_2}$",
        "$\\sigma_2$",
        "T",
        "p",
        "dCohena",
    ]
    data = [
        np.mean(ct1),
        np.std(ct1),
        np.mean(ct2),
        np.std(ct2),
        stat,
        p,
        es,
    ]
    return data, headers, stat, p, es


def mannwhitneyu(ct1, ct2):
    ct1 = ct1.apply(lambda x: int(str(x).split('.')[0]))
    ct2 = ct2.apply(lambda x: int(str(x).split('.')[0]))
    stat, p = sp.stats.mannwhitneyu(ct1, ct2)
    # es = stat / (len(ct1 * ct2))
    es = abs((2 * stat) / (len(ct1) * len(ct2)) - 1)  # cliff delta d
    headers = [
        "$Q_1$",
        "$IRQ_1$",
        "$Q_2$",
        "$IRQ_2$",
        "Z",
        "p",
        "$\\eta^2$",
    ]
    data = [
        np.median(ct1),
        np.percentile(ct1, 75) - np.percentile(ct1, 25),
        np.median(ct2),
        np.percentile(ct2, 75) - np.percentile(ct2, 25),
        stat,
        p,
        es,
    ]
    return data, headers, stat, p, es


def kruskal(*ct):
    for i, ii in enumerate(ct):
        ct[i] = ii.apply(lambda x: int(str(x).split('.')[0]))
    stat, p = sp.stats.kruskal(*ct)
    n = sum([len(i) for i in ct])

    data = []
    headers = []
    for i, _set in enumerate(ct):

        headers.append("$Q_{}$".format(i + 1))
        data.append(np.median(_set))
        headers.append("$IRQ_{}$".format(i + 1))
        data.append(np.percentile(_set, 75) - np.percentile(_set, 25))

    es = abs(stat / ((n**2 - 1) / (n + 1)))
    headers += ['Z', 'p', "$\\eta^2$"]
    data += [stat, p, es]

    return data, headers, stat, p, es


def get_power(cat=10, effect_scale=0.01, a=0.05, lx=30, max_p=0.8):
    df = DataFrame({
        'Typ testu' : [],
        'Liczba kategorii' : [],
        'Siła efektu' : [],
        'Moc testu' : [],
        'Wielkość próby' : [],
        'Alfa' : [],
    })
    for c in range(1, cat):
        for e in np.linspace(max_p - effect_scale, max_p + effect_scale, 10):
            for xx in range(1, lx):
                df.loc[len(df) + 1] = ['chi2', c, e, 0.8, 5, a]
                df.loc[len(df) + 1] = ['F', c, e, smp.FTestAnovaPower().solve_power(effect_size=e, nobs=xx, alpha=a, k_groups=c), xx, a]
                if c <= 2:
                    df.loc[len(df) + 1] = ['T', c, e, smp.TTestPower().solve_power(effect_size=e, nobs=xx, alpha=a), xx, a]
                else:
                    df.loc[len(df) + 1] = ['T', c, e, 0, xx, a]

    df.dropna(inplace=True)
    df['Wielkość próby'] = df['Wielkość próby'].astype(int)
    df['Liczba kategorii'] = df['Liczba kategorii'].astype(int)
    df = df[(df['Moc testu'] > max_p - 0.01) & (df['Moc testu'] < max_p + 0.01)]
    c = crosstab(df['Liczba kategorii'], df['Typ testu'], aggfunc='mean', values=df['Wielkość próby'])
    return c


def cramer_V(ct, chi2):
    cramerv = np.sqrt((chi2 / ct.sum()) / (min(ct.shape) - 1))
    return cramerv


def r2(X, y):
    y_mean = np.mean(y)
    m, c = np.polyfit(X, y, 1)
    y_pred = m * X + c
    SSE = np.sum((y - y_pred) ** 2)
    SST = np.sum((y - y_mean) ** 2)
    return 1 - (SSE / SST)


def chi_ind(data, question, group):
    """Chi2 test of indepedence."""
    ps = ''
    cramerv = ''
    ct = crosstab(data[question], data[group]).to_numpy()
    chi, p, dof, expected = sp.stats.chi2_contingency(ct)
    if p < pval:
        cramerv = cramer_V(ct, chi)
        for k, v in crv.items():
            if cramerv > v:
                ps = style(k + " ", fg="green")
        cramerv = "cV={}".format(np.sqrt((chi / ct.sum()) / (min(ct.shape) - 1)))
    else:
        ps = style('Fail ', fg="red")
    print("\t'\t- chi2 contingency test for:\n\t\t ->{}\n\t\t ->{}\n\t\t{}chi={}, p={}, dof={}, {}"
          .format(question, group, ps, chi, p, dof, cramerv))
