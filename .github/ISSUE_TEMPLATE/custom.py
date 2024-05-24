
def fix_places(place):
    places = {
        "Chirurgia": [
            "chirurgia",
            "blok operacyjny",
            "neurochirurgia",
            "intensywna terapia chirurgiczna",
        ],
        "POZ": [
            "zol",
            "opieka długoterminowa domowa",
            "dps",
            "opieka paliatywna"
        ],
        "Ambulatoryjna i Ratunkowa": [
            "poz",
            "sor",
            "oit",
        ],
        "Oddziały Kardiologiczne": [
            "kardiologia"
        ],
        "Psychologiczne": [
            "oddział leczenia uzależnień",
            "psychiatria"
        ],
        "Dziecięce": [
            "medycyna szkolna",
            "onkologia dziecięca",
            "pediatria"
        ],
        "Zachowawcze": [
            "Oddział wewnętrzny",
            "wewnętrzny",
            "pulmonologia",
            "geriatria",
            "neurologia",
        ],
        "Oddziały zabiegowe": [
            "oaiit",
            "ginekologia",
            "hematologia",
            "neonatologia",
            "onkologia",
            "ortopedia",
            "ośrodek dializ",
            "tramatologia narządu ruchu",
            "udarowy",
        ],
    }
    for key, value in places.items():
        for var in value:
            if var in place:
                return key
    return "nieokreślone"


def duty_clear(_str):
    parts = _str.split("(")
    return parts[0] + parts[1][:-1]
