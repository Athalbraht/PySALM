import numpy as np
import scipy as sp
import statsmodels.stats.power as smp
from addons import fm
from click import style
from pandas import DataFrame, crosstab

from conf import crv, pval


def auto_test(data : DataFrame, groups: list, values: list, type_dict: dict, min_n: DataFrame, dep : str = 'ind', debug = False) -> DataFrame:
    test_map = {
        'n' : {
            'ind': {
                '2' : {
                    'n': {
                        'norm' : [chi2, 'chi2', '$\\chi^2$'],
                    },
                    'o': {
                        'norm' : [mannwhitneyu, "T", "Manna-Whitneya"],
                    },
                    'q': {
                        'norm': [ttest, "T", 'T'],
                        'rm': [mannwhitneyu, "T", "Manna-Whitneya"],
                    },
                },
                '3': {
                    'n': {
                        'norm' : [chi2, "chi2", "$\\chi^2$"],
                    },
                    'o': {
                        'norm' : [kruskal, "T", 'Kruskal-Wallis'],
                    },
                    'q': {
                        'norm': [anova, "F", "ANOVA"],
                        'rm': [kruskal, "T", "Kruskala-Wallisa"],
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
        'o' : [spearman],
        'q' : [pearson],
    }
    df_struct = {
        'groups' : [],
        'values' : [],
        'ttype' : [],
        'result' : [],
        'fixed_col' : [],
        'pass' : [],
        'e_size' : [],
        'p' : [],
        'tname' : [],
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
    for _groups in groups:
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
                if gtype == 'n':
                    if vtype in ['q', 'o']:
                        gsize = tdata.groupby(_groups).count()
                        fixed_col = fix_size(gsize)
                        tdata = tdata[tdata[_groups].isin(fixed_col)]
                        data_list = [tdata[tdata[_groups] == cat][_values] for cat in fixed_col]
                        if vtype == 'q':
                            flat = []
                            for i in data_list:
                                flat += i.to_list()
                            _, p = sp.stats.shapiro(flat)
                            if p < 0.05:
                                sub = 'rm'
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
                    result, p, ef = struct[sub][0](*data_list)
                    _pass = False
                    if p < 0.05:
                        _pass = True

                    df.loc[len(df) + 1] = [_groups, _values, ttype, result, fixed_col, _pass, ef, p, tname]

                elif gtype == 'q':
                    pass
                elif gtype == 'p':
                    pass
            except Exception as e:
                print("- {} in {} {}\n{}".format(fm('Error', "red"), _groups, _values, e))
    return df


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

    result = {}
    for i, _set in enumerate(ct):
        result["$\\overline{{x_{}}}$".format(i + 1)] = np.mean(_set)
        result["$\\sigma_{}$".format(i + 1)] = np.std(_set)

    es = abs(ss_between / ss_total)
    _result = {
        "F" : stat,
        "p" : p,
        "$\\eta^2$" : es,
    }
    result.update(_result)
    return result, p, es


def chi2(ct):
    ct = np.array(ct)
    stat, p, dff, exp = sp.stats.chi2_contingency(ct)
    cramerv = abs(np.sqrt((stat / ct.sum()) / (min(ct.shape) - 1)))
    result = {
        "$\\chi^2$" : stat,
        "p" : p,
        "$V_c$" : cramerv
    }
    return result, p, cramerv


def ttest(ct1, ct2):
    stat, p = sp.stats.ttest_ind(ct1, ct2)
    dm = ct1.mean() - ct2.mean()
    pooled_std = np.sqrt(((len(ct1) - 1) * np.var(ct1) + (len(ct2) - 1) * np.var(ct2)) / (len(ct1) + len(ct2) - 2))
    es = abs(dm / pooled_std)
    result = {
        "$\\overline{x_1}$" : np.mean(ct1),
        "$\\sigma_1$" : np.std(ct1),
        "$\\overline{x_2}$" : np.mean(ct2),
        "$\\sigma_2$" : np.std(ct2),
        "T" : stat,
        "p" : p,
        "dCohena" : es,
    }
    return result, p, es


def mannwhitneyu(ct1, ct2):
    ct1 = ct1.apply(lambda x: int(str(x).split('.')[0]))
    ct2 = ct2.apply(lambda x: int(str(x).split('.')[0]))
    stat, p = sp.stats.mannwhitneyu(ct1, ct2)
    # es = stat / (len(ct1 * ct2))
    es = abs((2 * stat) / (len(ct1) * len(ct2)) - 1)  # cliff delta d
    result = {
        "$Q_1$" : np.median(ct1),
        "$IRQ_1$" : np.percentile(ct1, 75) - np.percentile(ct1, 25),
        "$Q_2$" : np.median(ct2),
        "$IRQ_2$" : np.percentile(ct2, 75) - np.percentile(ct2, 25),
        "Z" : stat,
        "p" : p,
        "$\\eta^2$" : es,
    }
    return result, p , es


def kruskal(*ct):
    for i,ii in enumerate(ct):
        ct[i] = ii.apply(lambda x: int(str(x).split('.')[0]))
    stat, p = sp.stats.kruskal(*ct)
    n = sum([len(i) for i in ct])

    result = {}
    for i, _set in enumerate(ct):
        result["$Q_{}$".format(i + 1)] = np.median(_set)
        result["$IRQ_{}$".format(i + 1)] = np.percentile(_set, 75) - np.percentile(_set, 25)

    es = abs(stat / ((n**2 - 1) / (n + 1)))
    _result = {
        "Z" : stat,
        "p" : p,
        "$\\eta^2$" : es,
    }
    result.update(_result)
    return result, p, es


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
                df.loc[len(df) + 1] = ['chi2', c, e, smp.GofChisquarePower().solve_power(effect_size=e, nobs=xx, alpha=a, n_bins=c), xx, a]
                df.loc[len(df) + 1] = ['F', c, e, smp.GofChisquarePower().solve_power(effect_size=e, nobs=xx, alpha=a, n_bins=c), xx, a]
    df.dropna(inplace=True)
    df['Wielkość próby'] = df['Wielkość próby'].astype(int)
    df['Liczba kategorii'] = df['Liczba kategorii'].astype(int)
    df = df[(df['Moc testu'] > max_p - 0.01) & (df['Moc testu'] < max_p + 0.01)]
    c = crosstab(df['Liczba kategorii'], df['Typ testu'], aggfunc='mean', values=df['Wielkość próby'])
    return c


def cramer_V(ct, chi2):
    cramerv = np.sqrt((chi2 / ct.sum()) / (min(ct.shape) - 1))
    return cramerv


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
