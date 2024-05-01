import numpy as np
import scipy as sp
import statsmodels.stats.power as smp
from click import style
from pandas import DataFrame, crosstab

from conf import crv, pval

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
    return result


def pearson(ct1, ct2):
    stat, p = sp.stats.pearsonr(ct1, ct2)
    result = {
        "rPearson" : stat,
        "p" : p,
    }
    return result


def anova(*ct):
    stat, p = sp.stats.f_oneway(*ct)
    group_means = [np.mean(i) for i in ct]
    overall_mean = np.mean(np.concatenate(ct))
    ss_between = sum([len(group) * (mean - overall_mean)**2 for group, mean in zip(ct, group_means)])
    ss_total = sum((value - overall_mean)**2 for group in ct for value in group)

    result = {
        "F" : stat,
        "p" : p,
        "$\\eta^2$" : ss_between / ss_total
    }
    return result


def chi2(ct):
    ct = np.array(ct)
    stat, p = sp.stats.chi2_contingency(ct)
    cramerv = np.sqrt((stat / ct.sum()) / (min(ct.shape) - 1))
    result = {
        "$\\chi^2$" : stat,
        "p" : p,
        "$V_c$" : cramerv
    }
    return result


def ttest(ct1, ct2):
    stat, p, _ = sp.stats.ttest_ind(ct1, ct2)
    dm = ct1.mean() - ct2.mean90
    pooled_std = np.sqrt(((len(ct1) - 1) * np.var(ct1) + (len(ct2) - 1) * np.var(ct2)) / (len(ct1) + len(ct2) - 2))
    result = {
        "T" : stat,
        "p" : p,
        "dCohena" : dm / pooled_std,
    }
    return result


def mannwhitneyu(ct1, ct2):
    stat, p = sp.stats.mannwhitneyu(ct1, ct2)
    result = {
        "Z" : stat,
        "p" : p,
        "$\\eta^2$" : stat / (len(ct1 * ct2))
    }
    return result


def kruksal(*ct):
    stat, p = sp.stats.kruksal(*ct)
    n = sum([len(i) for i in ct])
    result = {
        "Z" : stat,
        "p" : p,
        "$\\eta^2$" : stat / ((n**2 - 1) / (n + 1))
    }
    return result


def get_power(cat=10, effect_size=[0.5, 0.99], a=0.05, lx=30, max_p=0.8):
    df = DataFrame({
        'Liczba kategorii' : [],
        'Siła efektu' : [],
        'Moc testu' : [],
        'Wielkość próby' : [],
        'Alfa' : [],
    })
    for c in range(1, cat):
        for e in np.linspace(effect_size[0], effect_size[1], 10):
            for xx in range(1, lx):
                df.loc[len(df) + 1] = [c, e, smp.GofChisquarePower().solve_power(effect_size=e, nobs=xx, alpha=a, n_bins=c), xx, a]
    df.dropna(inplace=True)
    df['Wielkość próby'] = df['Wielkość próby'].astype(int)
    df['Liczba kategorii'] = df['Liczba kategorii'].astype(int)

    c = df[(df['Moc testu'] > 0.79) & (df['Moc testu'] < 0.81)].groupby('Liczba kategorii').mean().astype(int)['Wielkość próby']
    return df, c


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
