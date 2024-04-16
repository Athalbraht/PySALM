from texbuilder import Section


def document():

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
    metodyka = Section("Metodyka badań", config=tex_config, init=True)

    dane_metryczne = Section("Dane metryczne", config=metodyka.config)
    metryka = dane_metryczne.add_subsection("Metryka")
    plec = metryka.add_subsection("Płeć")
    plec.add_description("xadwa")
    plec.add_object("xaddwadwawa")
    plec.add_description("xadwa")
    plec.add_object("xaddwadwawa")
    plec.add_object("xaddwadwawa")
    plec.add_description("xadwa")
    plec.add_description("xadwa")

    wiek = metryka.add_subsection("Wiek")
    wiek.add_description("xadwa")
    wiek.add_object("xaddwadwawa")
    wiek.add_description("xadwa")

    return dane_metryczne
