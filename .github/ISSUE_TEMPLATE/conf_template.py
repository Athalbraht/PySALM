import numpy as np
import os
from typing import TypeVar


import pandas as pd
import seaborn as sns

from classificators import BMI_ranges, age_binding
from custom import fix_places

sns.set_theme(style="whitegrid", rc={"figure.figsize": (14, 8), "axes.labelsize": 15})
sns_api = {"height": 6, "aspect": 1.75}
pic_path = "report/assets"
pic_ext = ".pdf"
tab_path = "report/tabs"
pval = 0.05


templates_folder = "views/"


def template(x):
    abs_path = os.path.abspath(templates_folder)
    return os.path.join(abs_path, x)


tex_config = {
    "folder" : "output/report",
    "filename" : "report",
    "ext" : ".tex",
    "responses_file" : "responses.csv",
    "preload_alias" : "%%PRELOAD%%",
    "payload_alias" : "\\iffalse PAYLOAD \\fi",
    "postload_alias" : "%%POSTLOAD%%",
    "decorator" : [],
    "lock" : False,
    "watermark" : True,
    "assets_folder" : os.path.abspath("data/static"),
    "templates_folder" : os.path.abspath(templates_folder),
    "templates" : {
        "scheme" : template("document.tex"),
        "table" : template("table.tex"),
        "desctable" : template("desctable.tex"),
        "powertable" : template("desctable.tex"),
        "corrtable" : template("desctable.tex"),
        "autostatable" : template("desctable.tex"),
        "counttable" : template("desctable.tex"),
        "expandtable" : template("desctable.tex"),
        "crosstable" : template("desctable.tex"),
        "statcorr" : template("desctable.tex"),
        "stattest" : template("desctable.tex"),
        "plot" : template("graphic.tex"),
        "powerplot" : template("graphic.tex"),
        "text" : template("text.tex"),
        "desc" : template("text.tex"),
    },
    "constants" : {
        "%%LANGUAGE%%" : "polish",
        "%%DOCUMENT_CLASS%%" : "article",
        "%%MARIGIN_TOP%%" : "2cm",
        "%%MARIGIN_BOTTOM%%" : "2cm",
        "%%MARIGIN_LEFT%%" : "3cm",
        "%%MARIGIN_RIGHT%%" : "3cm",
        "%%FONT%%" : "lmodern",  # examples https://www.overleaf.com/learn/latex/Font_typefaces

        "%%TITLE%%" : "DOC TITLE",
        "%%AUTHOR%%" : "autorname",
    },
    "compile" : {
        "method" : "latex",
        "executable" : "pdflatex",
        "options" : "",
    },
    "ai" : {
        'mode' : 'safe',
        'model' : "gpt-3.5-turbo-0125",
        # 'system': "Jesteś statystykiem który pisze raport statystyczny na temat występowaniu bólu kręgosłupa u pielegniarek i jak to wpływa na ich życie, tworzysz opisy do tabel i wykresów, nie przekraczaj 300 słów, nie sugeruj nic, ma być ściśle, po prostu opisuj to co widzisz w tabeli, np. dostajesz informacje że tabela to odpowiedzi na jakies pytanie i twoim zadaniem jest tylko opisać tą tabele np. średni wzrost w grupie to X, odchylenie Y, najszęsciej występuje odpowiedz C itp. NIE zaczynaj zdania od przykładowo 'w badaniiu przeprowadzonym na grupie pielegniarek...' odrazu pisz o wartosciach z tabeli, bez żadnych wstępów",
        'system': "Udawaj, że jesteś naukowcem, postaraj się parafrazować wysyłane ci zdania w bardziej profesjonalny styl, Odmieniaj odpowienio nazwy zmiennych np. 'tabela krzyżowa między wartością (Kategoria wiekowa) a (Czy przerwy w pracy są wystarczające) zawiera X'  na 'w tabeli krzyżowej zawierającej kategorie wiekową respondentów w stosunku do pytania o wystarczające przerwy w pracy znajduje się X' itp. Jeśli chcesz coś wypnktować, używaj formatowania LaTex, czasem możesz dostać tabele w markdown, żeby opisać coś więcej co w niej widzisz. W odpowiedzi dawaj tylko tekst, bez prób dawania mi tablel."
    }

}

crv = {
    "Very weak": 0,
    "Weak": 0.05,
    "Moderate": 0.1,
    "Strong": 0.15,
    "Very Strong": 0.25,
}

columns = [
]
cl = columns.copy()


#########################################################################################

metric_col = [
]

quantitative_data = [
]
multiple_data = [
]

bool_col = [
]

bool2_col = [
]
nominal_data = [
]

ordinal_data = [
]


type_dict = {
    "n" : nominal_data,
    "o" : ordinal_data,
    "q" : quantitative_data,
    'multi' : multiple_data,
}

############################################

T = TypeVar("T")


def corr_tab(cr):
    try:
        cr = cr.pivot_table(index='group', columns='value', values=['corr', 'p'])
    except:
        print('Failed to gen corr')
        return pd.DataFrame()
    finally:
        return cr.stack(0).unstack(1)


def tests_tab(ddf):
    tests = list(ddf.value_counts('tname').index)
    groups = list(ddf.value_counts('groups').index)
    tables = []
    for test in tests:
        for group in groups:
            try:
                df = ddf[(ddf['tname'] == test) & (ddf['groups'] == group)].reset_index()
                cols = df['fixed_col'].iloc[0]
                v = [df['values'].to_list()] + list(np.array(df['headers'].to_list()).T)
                gr = ['grupy'] + df['data'].iloc[0]
                d1 = ', '.join(df['data'].iloc[0][:2])
                d2 = ', '.join(df['data'].iloc[0][-3:])

                tab = pd.DataFrame(dict(zip(gr, v)))
                caption = "Test {} dla grupy {}. {} to kolejno mediana oraz rozstęp międzykwartylowy, {} - Wartość statystyki, p-value oraz wskaźnik siły efektu".format(
                    test, group, d1, d2)
                tables.append(tab)
            except:
                print('failed to gen stats {} {}'.format(test, group))

    return tables


def auto_register(comm, tab, bool_tab : list = [], bool_tab2=[]):
    bools = []
    bools2 = []
    multi = []
    register = []
    if isinstance(tab, dict):
        pass
    if isinstance(tab, list):
        for i, question in enumerate(tab):
            register.append(comm.register('static', 'desc', '\\newpage'))
            if question in bool_tab:
                bools.append(question)
            elif question in bool_tab2:
                bools2.append(question)
            elif question in multiple_data:
                register.append(
                    comm.register('gen', 'expandtable', question, alias=question, mode='reload'),
                )
            else:
                register.append(
                    comm.register('gen', 'counttable', question, alias=question, mode='reload'),
                )
        if bools:
            register = [

                comm.register('static', 'desc', '\\newpage'),
                comm.register('gen', 'counttable', bools, alias=bools[0], mode='reload')] + register
        if bools2:
            register = [
                comm.register('static', 'desc', '\\newpage'),
                comm.register('gen', 'counttable', bools2, alias=bools[0], mode='reload')] + register
        return register


def structure(comm : T, df, make_stat, power):
    """Define report structure."""
    ff = "file"
    ll = "load"
    gg = "gen"
    gd = "gendesc"
    ss = "static"

    ta = "table"
    pl = "plot"
    de = "desc"
    det = "desctable"
    cot = "counttable"
    ext = "expandtable"
    crt = "crosstable"
    fp = 'prompt'

    xr = "reload"       # choice randomly from database
    xu = "uniqe"        # always regenerate description
    xg = "global"       # use global setting
    xs = "static"       # AI support disabled, using default values
    xp = "paraphrase"   # paraphrase existing description

    tex_structure = {
        "Metryka" : auto_register(comm,
                                  metric_col
                                  ),

        "Przegląd wyników ankiety" : {
            "Badania" : auto_register(comm,
                                      bad_self + bad_self + bad_usg + bad_mm + bad_gin + bad_cyt,
                                      bad_bool,
                                      ),
            "Nowotwór" : auto_register(comm,
                                       cancer_diag + cancer_fami,
                                       ),

            "Świadomość" : auto_register(comm,
                                         aware,
                                         ),

            "COVID-19" : auto_register(comm,
                                       covid,
                                       ),

            "Kwestionariusz MHLC" : [
                comm.register(gg, det, mhlc, alias='mhfs', mode=xr),
            ]
            # "Kwestionariusz MHLC" : auto_register(comm,
            #                                    mhlc,
            #                                   mhlc,
            #                                  ),
        },
        "Analiza" : [
            comm.register(ss, de, 'TODO'),
        ],
        "Wnioski" : [
            comm.register(ss, de, 'TODO'),
        ],
    }
    return tex_structure


def data_loader(data):
    """Load and prepare data."""
    df = pd.read_pickle(data)
    return df
