import numpy as np
import scipy as sp
from click import style
from pandas import crosstab

from conf import crv, pval


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
