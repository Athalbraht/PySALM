import os

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.stats.power as smp
from stats import r2
import scipy as sp
from click import style
from pandas import DataFrame

from addons import type_detector
from conf import pic_ext, sns, sns_api, tex_config


def plot_power(cat=10, effect_size=[0.5, 0.99], a=0.05, lx=30, max_p=0.8, alias='chipower'):
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

    g = sns.relplot(data=df, x='Wielkość próby', y="Moc testu", kind='line', hue='Liczba kategorii')
    g.axes[0][0].axhline(max_p, df['Wielkość próby'].min(), df['Wielkość próby'].max(), alpha=0.3, linestyle='--', c='black')
    g.fig.set_figwidth(14)
    g.fig.set_figheight(8)
    c = df[(df['Moc testu'] > 0.79) & (df['Moc testu'] < 0.81)].groupby('Liczba kategorii').mean().astype(int)['Wielkość próby']
    for cc in c.index:
        g.axes[0][0].axvline(c[cc], 0, 1, alpha=0.3, linestyle='--', c='black')
    filename = alias + pic_ext
    path = os.path.join(tex_config['folder'], 'pics', filename)
    plt.savefig(path)
    # caption = "Minimalna wielkość próby dla ustalonej mocy testu (czarne linie) o ustalonel licznie kategorii. Rozmycie zawiera siłę efektu > 0.7"
    caption = "Wykres przedstawia minimalną wielkość próby dla testu o mocy powyżej 0.8 dla różnych ilości kategorii (stopni swobody). W kolorowym tle zawierają się siły efektu powyżej 0.7"
    return path, " ", caption


def plot(data, pset, alias, labels=[False, False], **conf):
    """Auto print graphs."""
    # ordinal_data plot
    # 2D temp map for p val
    plt.clf()
    plt.cla()
    caption = ''
    types = type_detector(pset)
    validator = types
    #####################################################################
    if len(pset) == 1:
        x = pset[0]
        if validator == 'n' or validator == 'o':
            kwargs = {
                # "kde" : True,
                "kind" : 'count',
                "stat" : 'percent'
            }
            kwargs.update(conf)
            g = sns.catplot(data, x=x, **kwargs)
            g.fig.set_figwidth(14)
            g.fig.set_figheight(8)
            caption = 'Histogram dla kolumny {}'.format(x)
            labels[1] = "Procent"
        elif validator == 'q':
            kwargs = {
                # "kde" : True,
                #a"bins" : 20,
                "multiple" : 'stack',
                "stat" : 'percent'
            }
            kwargs.update(conf)
            g = sns.displot(data, x=x, **kwargs)
            g.fig.set_figwidth(14)
            g.fig.set_figheight(8)
            caption = 'Histogram dla kolumny {}'.format(x)
            labels[1] = "Procent"
    #####################################################################
    elif len(pset) == 2:
        x, y = pset
        if validator == 'oq' or validator == 'nq':
            kwargs = {
                "kind" : "box",
            }
            kwargs.update(sns_api)
            g = sns.catplot(data, x=x, y=y, **kwargs)
            caption = 'Rozkład zmiennych {} i {}'.format(x, y)
            g.fig.set_figwidth(14)
            g.fig.set_figheight(8)
        elif validator == 'qq':
            kwargs = {
                "marker" : '+',
                #"color" : 'black',
                "marginal_kws" : dict(bins=15),
                "kind" : 'reg',
            }
            kwargs.update(conf)
            g = sns.jointplot(data, x=x, y=y, **kwargs)
            r, p = sp.stats.pearsonr(data[x], data[y])
            rr = round(r2(data[x], data[y]), 3)
            g.ax_joint.annotate('$R^2 = {}$'.format(rr),
                                xy=(0.1, 0.7), xycoords='axes fraction',
                                ha='left', va='center',
                                bbox={'boxstyle': 'round', 'fc': 'white', 'ec': 'navy'})
            # bbox={'boxstyle': 'round', 'fc': 'powderblue', 'ec': 'navy'})
            g.ax_joint.annotate(f'$\\rho = {r:.3f}, p = {p:.3f}$',
                                xy=(0.1, 0.9), xycoords='axes fraction',
                                ha='left', va='center',
                                bbox={'boxstyle': 'round', 'fc': 'white', 'ec': 'navy'})
            # bbox={'boxstyle': 'round', 'fc': 'powderblue', 'ec': 'navy'})
            g.fig.set_figwidth(14)
            g.fig.set_figheight(8)

            caption = 'Rozkład zmiennych {} i {}'.format(x, y)
            # TODO REGRESSION PARAMS
    else:
        print("\t\t{}".format(style("Unknown plot type {}".format(validator), fg="red")))
        return None
    # if labels[0] and validator != 'qq':
     #   g.set_xlabel(labels[0])
    # if labels[1] and validator != 'qq':
    #    g.set_ylabel(labels[1])
    filename = alias + pic_ext
    path = os.path.join(tex_config['folder'], 'pics', filename)
    plt.savefig(path)
    desc = ''
    return path, desc, caption
