import matplotlib.pyplot as plt
from click import style

from addons import type_detector
from conf import pic_ext, pic_path, sns, sns_api


def plot(data, pset, labels=[False, False], **conf):
    """Auto print graphs."""
    # ordinal_data plot
    # 2D temp map for p val
    print("\t-creating {} graphics".format(pset))
    plt.clf()
    plt.cla()
    validator, name, _ = type_detector(*pset)

    if len(pset) == 1:
        x = pset
        if validator == 'q':
            kwargs = {
                "kde" : True,
                "bins" : 20,
                "multiple" : 'stack',
                "stat" : 'percent'
            }
            kwargs.update(conf)
            g = sns.histplot(data, x=x, **kwargs)
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
    else:
        print("\t\t{}".format(style("Unknown plot type {}".format(validator), fg="red")))
        return None
    if labels[0]:
        g.set_xlabel(labels[0])
    if labels[1]:
        g.set_ylabel(labels[1])
    plt.savefig("{}/{}.{}".format(pic_path, name, pic_ext))
    return None
