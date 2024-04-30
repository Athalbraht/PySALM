import numpy as np
import scipy as sp
from click import style
from pandas import crosstab, DataFrame

from conf import crv, pval

import statsmodels.stats.power as smp


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


def chi_ind(data, question, group):
    """Chi2 test of indepedence."""
    ps = ''
    cramerv = ''
    ct = crosstab(data[question], data[group]).to_numpy()
    chi, p, dof, expected = sp.stats.chi2_contingency(ct)
    if p < pval:
        cramerv = np.sqrt((chi / ct.sum()) / (min(ct.shape) - 1))
        for k, v in crv.items():
            if cramerv > v:
                ps = style(k + " ", fg="green")
        cramerv = "cV={}".format(np.sqrt((chi / ct.sum()) / (min(ct.shape) - 1)))
    else:
        ps = style('Fail ', fg="red")
    print("\t'\t- chi2 contingency test for:\n\t\t ->{}\n\t\t ->{}\n\t\t{}chi={}, p={}, dof={}, {}"
          .format(question, group, ps, chi, p, dof, cramerv))
