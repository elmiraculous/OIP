import nltk
import re
import os
from pymorphy3 import MorphAnalyzer
from collections import defaultdict 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from num2words import num2words
from bs4 import BeautifulSoup
nltk.download('punkt_tab')
nltk.download('stopwords')

morph = MorphAnalyzer()
russian_stopwords = set(stopwords.words('russian'))

def convert_number(text):
    def replace_number(match):
        return num2words(match.group(), lang='ru')  
    
    return re.sub(r'\b\d+\b', replace_number, text)
 
def clean_text(input_text):
    soup = BeautifulSoup(input_text, 'html.parser')
    text = soup.get_text()
    
    # JavaScript-код 
    clean_text = re.sub(r'window\.\w+|function\w*\([^)]*\)|document\.\w+', '', text)
    # спецсимволы
    clean_text = re.sub(r'[^а-яА-ЯёЁ\s]', ' ', clean_text)
    # URL и ссылки
    clean_text = re.sub(r'http\S+', '', clean_text)
    clean_text = clean_text.lower()
    # Знаки препинания
    clean_text = re.sub(r'[^\w\s]', ' ', clean_text)
    # Множественные пробелы
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = convert_number(clean_text)
    return clean_text.strip()

def process_file():
    for i in range(1, 193):
        filename = f'pages/page_{i}.html'
        if os.path.exists(filename):
            print(f"Обработка файла {filename}")
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned_text = clean_text(text) 
                
                all_tokens = word_tokenize(cleaned_text)
                valid_tokens = [token for token in all_tokens if len(token) >= 2 and token not in russian_stopwords]
                
                lemmatized = defaultdict(list)
                for token in valid_tokens:
                    parsed = morph.parse(token)[0]
                    lemma = parsed.normal_form
                    if token not in lemmatized[lemma]:
                        lemmatized[lemma].append(token)
                
                sorted_lemmas = sorted(lemmatized.items())
                filename_tokens = f'tokens/token_{i}.txt' 
                filename_lemmas = f'lemmas/lemmas_{i}.txt'  

                # Создаем директории, если они не существуют
                os.makedirs('tokens', exist_ok=True)
                os.makedirs('lemmas', exist_ok=True)

                with open(filename_tokens, 'w', encoding='utf-8') as f_tokens:
                    for token in valid_tokens:
                        f_tokens.write(token + '\n')

                with open(filename_lemmas, 'w', encoding='utf-8') as f_lemmas:
                    for lemma, token_list in sorted_lemmas:
                        f_lemmas.write(f"{lemma} {' '.join(sorted(token_list))}\n")
            
            print(f"Токенов: {len(valid_tokens)}")
            print(f"Уникальных лемм: {len(lemmatized)}")
            print("---")

def main():
    process_file()
    print('ok')

if __name__ == "__main__":
    main()

