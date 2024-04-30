import os
import matplotlib.pyplot as plt
from click import style

from addons import type_detector
from conf import pic_ext, sns, sns_api, tex_config


def plot(data, pset, alias, labels=[False, False], **conf):
    """Auto print graphs."""
    # ordinal_data plot
    # 2D temp map for p val
    plt.clf()
    plt.cla()
    caption = ''
    types = type_detector(pset)
    validator = types

    if len(pset) == 1:
        x = pset[0]
        if validator == 'q':
            kwargs = {
                # "kde" : True,
                "bins" : 20,
                "multiple" : 'stack',
                "stat" : 'percent'
            }
            kwargs.update(conf)
            g = sns.histplot(data, x=x, **kwargs)
            caption = 'Histogram dla kolumny {}'.format(x)
            labels[1] = "Procent"
    elif len(pset) == 2:
        x, y = pset
        if validator == 'oq' or validator == 'nq':
            kwargs = {
                "kind" : "box",
            }
            kwargs.update(sns_api)
            g = sns.catplot(data, x=x, y=y, **kwargs)
        elif validator == 'qq':
            kwargs = {
                "marker" : '+',
                "color" : 'black',
                "marginal_kws" : dict(bins=15),
                "kind" : 'reg',
            }
            kwargs.update(conf)
            g = sns.jointplot(data, x=x, y=y, **kwargs)
            caption = 'Rozkład zmiennych "{}" i "{}"'.format(x, y)
    else:
        print("\t\t{}".format(style("Unknown plot type {}".format(validator), fg="red")))
        return None
    if labels[0] and validator != 'qq':
        g.set_xlabel(labels[0])
    if labels[1] and validator != 'qq':
        g.set_ylabel(labels[1])
    filename = alias + pic_ext
    path = os.path.join(tex_config['folder'], 'pics', filename)
    plt.savefig(path)
    desc = ''
    return path, desc, caption
