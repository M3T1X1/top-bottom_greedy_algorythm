import csv

# Funkcja do wczytywania danych z pliku CSV
def load_csv(filename):
    with open(filename, newline='') as f:  # Otwieramy plik CSV
        reader = csv.DictReader(f, delimiter=',')  # Tworzymy obiekt do czytania wierszy jako słowniki
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

        d_classes = list(values_by_decision.keys())  # Lista klas decyzyjnych
        for i in range(len(d_classes)):
            for j in range(i + 1, len(d_classes)):
                # Porównujemy pary klas decyzyjnych
                vi_list = values_by_decision[d_classes[i]]
                vj_list = values_by_decision[d_classes[j]]
                for v1 in vi_list:
                    for v2 in vj_list:
                        if v1 != v2:
                            cut = (v1 + v2) / 2  # Środek między wartościami
                            cuts[attr].add(cut)  # Dodajemy cięcie
    return cuts  # Zwracamy wszystkie możliwe cięcia

def discretize(S, selectedCuts):
    for obj in S:
        for attr, cuts in selectedCuts.items():
            value = obj[attr]  # Wartość oryginalna
            bins = sorted(cuts)  # Posortowane cięcia
            label = 0  # Numer przedziału
            for cut in bins:
                if value > cut:
                    label += 1
                else:
                    break  # Przerywamy jeśli wartość nie przekracza kolejnego cięcia
            obj[attr] = f"{attr}_bin{label}"  # Zamieniamy wartość na etykietę przedziału
    return S  # Zwracamy zmodyfikowane dane

def save_csv(filename, data):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())  # Tworzymy writer z nagłówkami
        writer.writeheader()  # Zapisujemy nagłówki
        writer.writerows(data)  # Zapisujemy wszystkie dane


# Zachłanny wybór najlepszych cięć
def greedy_cut_selection(S, all_cuts):
    selected = {attr: set() for attr in all_cuts}  # Wybrane cięcia
    rest = {attr: set(cuts) for attr, cuts in all_cuts.items()}  # Pozostałe cięcia do rozważenia
    while True:
        best_attr, best_cut, _ = best_cut_fn(S, rest)  # Szukamy najlepszego cięcia
        if best_cut is None:
            break  # Kończymy jeśli nie ma więcej cięć
        selected[best_attr].add(best_cut)  # Dodajemy najlepsze cięcie
    return selected  # Zwracamy wybrane cięcia

def count_separated_pairs(S, attr, cut):
    count = 0
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            if S[i]["d"] != S[j]["d"]:  # Rozważamy tylko pary z różnymi decyzjami
                vi, vj = S[i][attr], S[j][attr]
                # Sprawdzamy, czy cięcie rozdziela wartości
                if (vi <= cut < vj) or (vj <= cut < vi):
                    count += 1
    return count  # Zwracamy liczbę separowanych par

# Znalezienie najlepszego cięcia wg liczby separowanych par
def best_cut_fn(S, cuts):
    best_gain = -1  # Największy zysk (liczba rozdzielonych par)
    best_cut = None
    best_attr = None

    # Przejdź przez wszystkie dostępne cięcia
    for attr in cuts:
        for cut in cuts[attr]:
            gain = count_separated_pairs(S, attr, cut)  # Liczymy zysk
            if gain > best_gain:
                best_gain = gain
                best_cut = cut
                best_attr = attr

    # Jeśli znaleziono najlepsze cięcie, usuń je z pozostałych cięć
    if best_attr is not None and best_cut is not None:
        cuts[best_attr].remove(best_cut)
        # Jeśli lista cięć dla danego atrybutu jest pusta, usuń cały atrybut
        if not cuts[best_attr]:
            del cuts[best_attr]

    return best_attr, best_cut, best_gain

if __name__ == "__main__":
    input_file = "ewal.csv"  # Nazwa pliku wejściowego
    output_file = "DISCdata.csv"  # Nazwa pliku wyjściowego

    data, attributes = load_csv(input_file)  # Wczytujemy dane i listę atrybutów
    cuts = generate_cuts(data, attributes)  # Generujemy możliwe cięcia
    selected = greedy_cut_selection(data, cuts)  # Wybieramy najlepsze cięcia
    discretized = discretize(data, selected)  # Dyskretyzujemy dane

    # Wyświetlamy wybrane cięcia
    print("\nWybrane cięcia:")
    for attr, cut_list in selected.items():
        print(f"{attr}: {sorted(cut_list)}")

    # Wyświetlamy zdyskretyzowany system
    print("\nZdyskretyzowany system decyzyjny:")
    for obj in discretized:
        print(obj)

    save_csv(output_file, discretized)  # Zapisujemy dane do pliku