
def BMI_ranges(bmi):
    ranges = {
        "1. Niedowaga": (0, 18.5),
        "2. Prawidłowa masa ciała": (18.5, 25),
        "3. Nadwaga": (25, 30),
        "4. Otyłość": (30, 100),
    }
    # bmi binding
    for key, value in ranges.items():
        if bmi >= value[0] and bmi < value[1]:
            return key
    return "Nieokreślone"


def age_binding(age):
    age_range = [
        [20, 30],
        [30, 40],
        [40, 50],
        [50, 60],
        [60, 70],
        [70, 80],
    ]
    for i in age_range:
        if age >= i[0] and age < i[1]:
            return "{}-{}".format(i[0], i[1])
    return "Nieokreślone"
