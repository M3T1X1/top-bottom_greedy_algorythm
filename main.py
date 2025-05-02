import csv

# Funkcja do wczytywania danych z pliku CSV
def load_csv(filename):
    with open(filename, newline='') as f:  # Otwieramy plik CSV
        reader = csv.DictReader(f)  # Tworzymy obiekt do czytania wierszy jako słowniki
        data = []
        for row in reader:
            # Zamieniamy wartości atrybutów na float, a decyzję "d" na int
            obj = {k: float(v) if k != "d" else int(v) for k, v in row.items()}
            data.append(obj)  # Dodajemy przetworzony obiekt do listy
        # Zwracamy dane oraz listę atrybutów (wszystkie kolumny oprócz "d")
        return data, [k for k in data[0] if k != "d"]


# Generowanie możliwych cięć między parami klas decyzyjnych
def generate_cuts(S, attributes):
    cuts = {attr: set() for attr in attributes}  # Tworzymy pusty zbiór cięć dla każdego atrybutu
    for attr in attributes:
        values_by_decision = {}  # Grupujemy wartości atrybutów wg decyzji
        for obj in S:
            d = obj["d"]  # Wartość decyzji
            values_by_decision.setdefault(d, []).append(obj[attr])

        decision_classes = list(values_by_decision.keys())  # Lista klas decyzyjnych
        for i in range(len(decision_classes)):
            for j in range(i + 1, len(decision_classes)):
                # Porównujemy pary klas decyzyjnych
                vi_list = values_by_decision[decision_classes[i]]
                vj_list = values_by_decision[decision_classes[j]]
                for v1 in vi_list:
                    for v2 in vj_list:
                        if v1 != v2:
                            cut = (v1 + v2) / 2  # Środek między wartościami
                            cuts[attr].add(cut)  # Dodajemy cięcie
    return cuts  # Zwracamy wszystkie możliwe cięcia