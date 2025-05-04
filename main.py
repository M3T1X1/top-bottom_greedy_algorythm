




















































































































































































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
















































if __name__ == "__main__":
    input_file = "data.csv"  # Nazwa pliku wejściowego
    output_file = "data_discretized.csv"  # Nazwa pliku wyjściowego

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