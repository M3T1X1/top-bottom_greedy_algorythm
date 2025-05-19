import pandas as pd
import os
import numpy as np

def discretize_csv_file(csv_path: str):
    # Wczytaj dane z pliku CSV
    df = pd.read_csv(csv_path)
    attributes = df.columns[:-1]  # wszystkie kolumny oprócz ostatniej
    decision_col = df.columns[-1]  # ostatnia kolumna jako decyzja

    cuts = {attr: [] for attr in attributes}

    for attr in attributes:
        sorted_df = df[[attr, decision_col]].sort_values(by=attr).reset_index(drop=True)
        intervals = [(0, len(sorted_df))]
        attr_cuts = []

        while intervals:
            start, end = intervals.pop(0)
            best_cut = None
            best_score = float('inf')

            for i in range(start + 1, end):
                if sorted_df[attr][i] == sorted_df[attr][i - 1]:
                    continue

                left_classes = sorted_df[decision_col][start:i]
                right_classes = sorted_df[decision_col][i:end]
                score = len(set(left_classes)) + len(set(right_classes))

                if score < best_score:
                    best_score = score
                    best_cut = (i, (sorted_df[attr][i - 1] + sorted_df[attr][i]) / 2)

            if best_cut:
                idx, cut_val = best_cut
                attr_cuts.append(cut_val)
                intervals.append((start, idx))
                intervals.append((idx, end))

        cuts[attr] = sorted(attr_cuts)

    def get_interval(val, cut_list):
        if not cut_list:
            return "(-inf; inf)"
        for cut in cut_list:
            if val <= cut:
                idx = cut_list.index(cut)
                left = -float('inf') if idx == 0 else cut_list[idx - 1]
                return f"({left}; {cut}]"
        return f"({cut_list[-1]}; inf)"

    discretized_rows = []
    for _, row in df.iterrows():
        row_data = [get_interval(row[attr], cuts[attr]) for attr in attributes]
        row_data.append(str(row[decision_col]))
        discretized_rows.append(row_data)

    # Utwórz nazwę wynikową w folderze `data/` jako DISCdata1.csv itd.
    folder = os.path.dirname(csv_path)
    original_name = os.path.basename(csv_path)
    output_name = f"DISC{original_name}"
    output_path = os.path.join(folder, output_name)

    # Zapis do pliku
    try:
        with open(output_path, 'w') as f:
            for row in discretized_rows:
                f.write(','.join(row) + '\n')
        print(f"Zapisano: {output_path}")
    except Exception as e:
        print(f"Błąd zapisu: {e}")
