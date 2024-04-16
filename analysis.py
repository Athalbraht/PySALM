import click

from conf import *
from stats import *
from addons import *
from filters import *
from plotting import plot
from tables import *
from custom import *


# TODO
##################
# Generators
#       fix plot generator
#       multitab
# Layout
#     @ layout macro
#       latex templating
# Statistic
#     @ Autodetect
#       ANOVA test
#       Post-hoc test
#       reg model
#       multi anal
#       T test
# AI
#       make it answer
#       saving output to file
#     @ data loader


# @click.command()
# @click.option('-d', '--data', help='data file .csv')
def data_loader(data):
    """Load and prepare data."""
    df = pd.read_excel(data)
    pre_n = len(df)
    print("Loaded {} entries".format(pre_n))
    print("- Clearing nan values")
    df.dropna(inplace=True)
    df.reset_index()
    df["Ból VAS"] = df["Ból VAS"].astype(int)
    n = pre_n - len(df)
    print("\t - Droped {} entries {}%".format(n, round(len(df) / pre_n * 100)))
    print("- fixing duty column")
    #   df['Godziny przepracowane w tygodniu'] = df['Godziny przepracowane w tygodniu'].apply(duty_clear)
    print("- Converting multiple choice columns to list")
    for col in multiple_col:
        df[col] = df[col].apply(lambda x: x.split(';')[:-1])
    print("- Calc BMI values")
    df["Wartość BMI"] = df["Masa ciała [kg]"] / (df["Wzrost [cm]"] / 100) ** 2
    df["BMI"] = df["Wartość BMI"].apply(BMI_ranges)
    df["Kategoria wiekowa"] = df["Wiek"].apply(age_binding)
    print("- Cleared, numerical values description:")
    print("- Fixing places")
    df['Rodzaj oddziału'] = df['Oddział'].apply(fix_places)

    df[["Wiek", "Masa ciała [kg]", "Wzrost [cm]", "Wartość BMI"]].describe().round()

    return df


def generate_metric(df):
    print('- Generating metric data')
    data = df[metric_col]

    print('\t - Desc tables')
    tab = data.describe().round(1).astype(str)
    col = tab.columns
    shapiro = {}
    for c in col:
        shapiro[c] = str(round(sp.stats.shapiro(data[c])[1], 3))
    shapiro_df = pd.DataFrame(shapiro, index=(['$\\rho$']))
    tab = pd.concat([tab, shapiro_df]).transpose().to_latex()
    with open('{}/metric.tex'.format(tab_path), 'w') as file:
        file.write(fix_desc(tab))
    print('- Generating tables')
    # table_gen(data, 'sex', 'Płeć')
    # table_gen(data, 'age', 'Kategoria wiekowa')
    # table_gen(data, 'bmi', 'BMI', ['Kategoria wiekowa'], ['age'])
    # table_gen(data, 'place', 'Miejsce zamieszkania', ['Kategoria wiekowa', 'BMI', "Stan cywilny"], ['age', 'bmi', 'martial'])
    # table_gen(data, 'martial', 'Stan cywilny', ['Kategoria wiekowa', 'BMI', 'Miejsce zamieszkania'], ['age', 'bmi', 'place'])
    print("- Generating graphs")
    # print('\t - Age plots')
    # g = sns.histplot(data, x="Wiek", kde=True, bins=20, hue="Płeć", multiple='stack', stat='percent')
    # print('\t - BMI plots')
    # g = sns.histplot(data, x='Wartość BMI', stat='percent', kde=True, kde_kws={'bw_method': 0.6})
    # g = sns.catplot(data, x="BMI", y='Wiek', kind='box', **sns_api)
    # print('\t - Mass vs Height')
    # g = sns.jointplot(data, x="Wzrost [cm]", y="Masa ciała [kg]", marker='+', color='black', marginal_kws=dict(bins=15), kind='reg')
    return data


if __name__ == "__main__":
    print("\n\n Starting analysis for Aleksandra Zaba\n=====================================")
    df = data_loader("data/data.xlsx")
    data = generate_metric(df)
