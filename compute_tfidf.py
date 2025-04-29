import os
import math
from collections import defaultdict


def load_documents(tokens_dir, lemmas_dir, max_docs=192):
    documents_tokens = {}
    documents_lemmas = {}

    for doc_id in range(1, max_docs + 1):
        token_file = os.path.join(tokens_dir, f"token_{doc_id}.txt")
        lemma_file = os.path.join(lemmas_dir, f"lemmas_{doc_id}.txt")

        if os.path.exists(token_file):
            with open(token_file, 'r', encoding='utf-8') as f:
                documents_tokens[str(doc_id)] = f.read().split()

        if os.path.exists(lemma_file):
            documents_lemmas[str(doc_id)] = []
            with open(lemma_file, 'r', encoding='utf-8') as f:
                for line in f:
                    lemma, *forms = line.strip().split()
                    documents_lemmas[str(doc_id)].append((lemma, forms))

    return documents_tokens, documents_lemmas


def calculate_tf(documents, documents_tokens=None, is_lemmas=False):
    tf = {}
    for doc_id, data in documents.items():
        term_counts = defaultdict(int)
        if is_lemmas:
            for lemma, forms in data:
                term_counts[lemma] += sum(documents_tokens[doc_id].count(form) for form in forms)
        else:
            for term in data:
                term_counts[term] += 1
        tf[doc_id] = term_counts
    return tf


def calculate_idf(documents, is_lemmas=False):
    idf = defaultdict(float)
    num_docs = len(documents)
    term_doc_count = defaultdict(int)

    for data in documents.values():
        unique_terms = set(lemma for lemma, forms in data) if is_lemmas else set(data)
        for term in unique_terms:
            term_doc_count[term] += 1

    for term, count in term_doc_count.items():
        idf[term] = math.log(num_docs / count) if count else 0.0

    return idf


def calculate_tf_idf(tf, idf):
    return {
        doc_id: {term: freq * idf[term] for term, freq in terms.items()}
        for doc_id, terms in tf.items()
    }


def save_results(idf, tf_idf, output_dir, prefix):
    os.makedirs(output_dir, exist_ok=True)
    for doc_id, terms in tf_idf.items():
        with open(os.path.join(output_dir, f"{prefix}_page_{doc_id}.txt"), 'w', encoding='utf-8') as f:
            for term in terms:
                f.write(f"{term} {idf[term]} {tf_idf[doc_id][term]}\n")


def main():
    tokens_dir = "tokens"
    lemmas_dir = "lemmas"
    output_terms_dir = "tf_idf_terms"
    output_lemmas_dir = "tf_idf_lemmas"

    print("Loading documents...")
    documents_tokens, documents_lemmas = load_documents(tokens_dir, lemmas_dir)

    if not documents_tokens or not documents_lemmas:
        print("Error: No documents loaded. Check file paths.")
        return

    print("Calculating TF-IDF for tokens...")
    tf_tokens = calculate_tf(documents_tokens)
    idf_tokens = calculate_idf(documents_tokens)
    tf_idf_tokens = calculate_tf_idf(tf_tokens, idf_tokens)

    print("Calculating TF-IDF for lemmas...")
    tf_lemmas = calculate_tf(documents_lemmas, documents_tokens, is_lemmas=True)
    idf_lemmas = calculate_idf(documents_lemmas, is_lemmas=True)
    tf_idf_lemmas = calculate_tf_idf(tf_lemmas, idf_lemmas)

    print("Saving results...")
    save_results(idf_tokens, tf_idf_tokens, output_terms_dir, "terms")
    save_results(idf_lemmas, tf_idf_lemmas, output_lemmas_dir, "lemmas")

    print("Done!")


if __name__ == "__main__":
    main()