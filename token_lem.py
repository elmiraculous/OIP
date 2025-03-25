import nltk
import re
import os
from pymorphy3 import MorphAnalyzer
from collections import defaultdict 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from num2words import num2words
nltk.download('punkt_tab')
nltk.download('stopwords')

morph = MorphAnalyzer()
russian_stopwords = set(stopwords.words('russian'))

def convert_number(text):
    def replace_number(match):
        return num2words(match.group(), lang='ru')  
    
    return re.sub(r'\b\d+\b', replace_number, text)
 

def clean_text(input_text):
    # HTML-теги
    clean_text = re.sub('<[^<]+?>', '', input_text)
    # JavaScript-код 
    clean_text = re.sub(r'window\.\w+|function\w*\([^)]*\)|document\.\w+', '', clean_text)
    # спецсимволы
    clean_text = re.sub(r'[^а-яА-ЯёЁ\s]', '', clean_text)
    # URL и ссылки
    clean_text = re.sub(r'http\S+', '', clean_text)
    clean_text = clean_text.lower()
    # Знаки препинания
    clean_text = re.sub(r'[^\w\s]', '', clean_text)
    clean_text = convert_number(clean_text)
    return clean_text

def open_file():
    with open(r'pages/page_1.html', 'r', encoding='utf-8') as file :
        text = clean_text(file.read()) 
    return text


# Лемматизация токенов
def lemmatize_tokens(tokens):
    lemmatized = defaultdict(list)
    for token in tokens:
        if len(token) < 2 or token in russian_stopwords:
            continue
        
        else:
            parsed = morph.parse(token)[0]
            lemma = parsed.normal_form
            if token not in lemmatized[lemma]: 
                lemmatized[lemma].append(token)
    return {lemma: sorted(forms) for lemma, forms in lemmatized.items()}
# Обработка файла
def process_file():
    for i in range(1, 193):
        filename = f'hw1/pages/page_{i}.html'
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned_text = clean_text(text) 
                tokens = word_tokenize(cleaned_text) 
                tokens = [token for token in tokens if token not in stopwords.words('russian')]
                lemmatized_tokens = lemmatize_tokens(tokens)
                sorted_lemmas = sorted(lemmatized_tokens.items())

                filename_tokens = f'tokens/token_{i}.txt' 
                filename_lemmas = f'lemmas/lemmas_{i}.txt'  

                with open(filename_tokens, 'w', encoding='utf-8') as f_tokens, open(filename_lemmas, 'w', encoding='utf-8') as f_lemmas:
                    for lemma, token_list in sorted_lemmas:
                        f_lemmas.write(f"{lemma} {' '.join(sorted(token_list))}\n")
                        f_tokens.write(f"{lemma}\n")

def main():
    process_file()
    print('ok')

if __name__ == "__main__":
    main()

