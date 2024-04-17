from texbuilder import Section
import time
from loader import from_file


def tre(g, l):
    """Define report structure."""
    tex_structure = {
        "Metodyka Badań" : {
            "Pytania badawcze" : [
                g.add_description(
                    l.from_file("methods.tex"),
                    'pre',
                ),
                g.add_description(
                    l.from_file("questions.tex"),
                ),
            ],
            "Metoda statystyczna" : [
                g.add_description(
                    l.desc('stat-methods'),
                ),
            ],
        },
        "Dane metryczne" : {
            "Metryka" : {
                "Płeć" : [
                    g.add_description(
                        l.desc('metric'),
                        'prepre',
                    ),
                    g.add_table(
                        l.table('std', 'x', 'y')
                        ),
                ],
                "Wiek" : None,
                "BMI" : None,
            },
            "Warunki socjodemograficzne" : {
                "Miejsce zamieszkania" : None,
                "Stan cywilny" : None,
            },
            "Aktywność fizyczna" : None,
        },
        "Przegląd wyników ankieyty" : {
            "Występowanie bólu kręgosłupa" : None,
            "Zatrudnienie i warunki pracy" : None,
            "Wpływ bólu na fizyczne i psychiczne aspekty życia" : None,
        },
        "Analiza danych" : {
            "Znaczenie uwarunkowań socjo-demograficznych" : None,
            "Wpływ bólu kręgosłupa na jakość życia" : None,
            "Wpływ bólu kręgosłupa na upośledzenie funkcji fizycznych i psychicznych" : None,
            "Związek występowania bólu kręgosłupa z wskaźnikami antropometrycznymi" : None,
        },
        "Wnioski" : None,
    }


tex_config = {
    "filename" : 'report',
    "ext" : '.tex',
    "folder" : 'output',
    "template" : 'views/document.tex',
    "responses" : 'responses.csv',
    "TITLE" : 'Badanie wpływu bólu kręgosłupa na jakość życia wśród personelu pielęgniarskiego',
    "AUTHOR" : 'Aleksandra Żaba',
    "sections" : [
            "Metodyka badań",
            "Dane Metryczne",
            "Przegląd wyników ankiety",
            "Analiza danych",
            "Wnioski",
    ]
}


def builder():

    def expand(dic, obj):
        for section, value in dic.items():
            _obj = obj.add_section(section)
            if type(value) == dict:
                expand(value, _obj)

    document = Section("Report", config=tex_config, init=True)

    expand(tex_structure, document)

    return document
