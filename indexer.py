from collections import defaultdict
import json
import os

inverted_index = defaultdict(set)

def build_inverted_index():
    for i in range(1, 193):
        lemma_file = f'lemmas/lemmas_{i}.txt'
        if os.path.exists(lemma_file):
            with open(lemma_file, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split()
                    if parts:
                        lemma = parts[0]
                        all_words = parts
                        for word in all_words:
                            inverted_index[word].add(i)

    with open('inverted_index.json', 'w', encoding='utf-8') as f:
        json.dump({k: sorted(list(v)) for k, v in inverted_index.items()}, f, ensure_ascii=False, indent=2)


build_inverted_index()