#!/usr/bin/env python
'''
source: https://www.kdnuggets.com/2018/03/text-data-preprocessing-walkthrough-python.html
'''
import sys, argparse
import re, string, unicodedata
import nltk, contractions, inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

BLUE = '\033[230;48;5;25m'
RST = '\033[0m'

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text

def replace_contractions(text):
    """
    	Replace contractions in string of text
    	ex : didn't   --> did not
    		 don't    --> do not
    		 couldn't --> could not
    """
    return contractions.fix(text)

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = [unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore') for word in words]
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = [word.lower() for word in words]
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = [re.sub(r'[^\w\s]', '', word) for word in words if re.sub(r'[^\w\s]', '', word) != '']
    return new_words

def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = [p.number_to_words(word) if word.isdigit() else word for word in words]
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = [word for word in words if word not in stopwords.words('english')]
    return new_words

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = [stemmer.stem(word) for word in words]
    return stems

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word, pos='v') for word in words]
    return lemmas

def stem_and_lemmatize(words):
    stems = stem_words(words)
    lemmas = lemmatize_verbs(words)
    return stems, lemmas

def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    return words

def preprocessing(text):
	denoise = denoise_text(text)
	clean_text = replace_contractions(denoise)
	token = word_tokenize(clean_text)
	rem_stopword = normalize(token)
	stems, lemmas = stem_and_lemmatize(rem_stopword)
	return clean_text, token, rem_stopword, stems, lemmas

def main():
    # create argument
    ap = argparse.ArgumentParser(description='Preprocessing Text')
    ap.add_argument('infile', type=argparse.FileType('r'), default=sys.stdin, help='Input file text')
    args = ap.parse_args()
    
    text = args.infile.read()
    clean_text, token, rem_stopword, stems, lemmas = preprocessing(text)
    print('{}Source:{}\n{}\n'.format(BLUE, RST, text))
    print('{}Clean Text:{}\n{}\n'.format(BLUE, RST, clean_text))
    print('{}Tokenization:{}\n{}\n'.format(BLUE, RST, token))
    print('{}Stopword removed:{}\n{}\n'.format(BLUE, RST,rem_stopword))
    print('{}Stemmed:{}\n{}\n'.format(BLUE, RST, stems))
    print('{}Lemmatized:{}\n{}\n'.format(BLUE, RST, lemmas))

if __name__ == '__main__':
    main()
