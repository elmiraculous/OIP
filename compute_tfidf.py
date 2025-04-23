import os
import math
from collections import defaultdict

TOTAL_DOCS = 192

def calculate_df(directory, is_lemma=False):
    df_counts = defaultdict(int)
    
    for i in range(1, TOTAL_DOCS + 1):
        filename = f'lemmas_{i}.txt' if is_lemma else f'token_{i}.txt'
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            if is_lemma:
                terms = set(line.strip().split()[0] for line in f)
            else:
                terms = set(line.strip() for line in f)
            for term in terms:
                df_counts[term] += 1

    return df_counts


def compute_tfidf(df_counts, input_dir, output_dir, is_lemma=False):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, TOTAL_DOCS + 1):
        input_file = f'lemmas_{i}.txt' if is_lemma else f'token_{i}.txt'
        output_file = f'tfidf_{i}.txt'
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, output_file)

        if not os.path.exists(input_path):
            continue

        term_freq = defaultdict(int)
        total_terms = 0

        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                if is_lemma:
                    term = line.strip().split()[0]
                else:
                    term = line.strip()
                term_freq[term] += 1
                total_terms += 1

        with open(output_path, 'w', encoding='utf-8') as f_out:
            for term, freq in term_freq.items():
                tf = freq / total_terms
                df = df_counts.get(term, 1)
                idf = math.log(TOTAL_DOCS / df)
                tfidf = tf * idf
                f_out.write(f'{term} {idf:.6f} {tfidf:.6f}\n')


if __name__ == '__main__':
    print("Подсчитываем df для токенов...")
    df_tokens = calculate_df('tokens', is_lemma=False)

    print("Подсчитываем df для лемм...")
    df_lemmas = calculate_df('lemmas', is_lemma=True)

    print("Вычисляем TF-IDF для токенов...")
    compute_tfidf(df_tokens, 'tokens', 'tfidf_tokens', is_lemma=False)

    print("Вычисляем TF-IDF для лемм...")
    compute_tfidf(df_lemmas, 'lemmas', 'tfidf_lemmas', is_lemma=True)

    print("Готово! Результаты сохранены в папки tfidf_tokens/ и tfidf_lemmas/")
