def compare_tfidf(token_path, lemma_path):
    def load_tfidf(filepath):
        tfidf = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 3:
                    term, idf, tfidf_val = parts
                    tfidf[term] = (float(idf), float(tfidf_val))
        return tfidf

    tokens = load_tfidf(token_path)
    lemmas = load_tfidf(lemma_path)

    all_keys = set(tokens.keys()).union(lemmas.keys())

    print(f"{'Термин':<15} {'IDF токен':<10} {'TF-IDF токен':<15} | {'IDF лемма':<10} {'TF-IDF лемма'}")
    print("-" * 65)

    for term in sorted(all_keys):
        tok = tokens.get(term, (0, 0))
        lem = lemmas.get(term, (0, 0))
        if abs(tok[1] - lem[1]) > 1e-6:  # если tf-idf отличаются
            print(f"{term:<15} {tok[0]:<10.6f} {tok[1]:<15.6f} | {lem[0]:<10.6f} {lem[1]:.6f}")

# Пример использования:
compare_tfidf("tfidf_tokens/tfidf_1.txt", "tfidf_lemmas/tfidf_1.txt")
