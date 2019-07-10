#!/usr/bin/env python
import sys, argparse
import nltk
from nltk import word_tokenize, sent_tokenize
from preprocessing import denoise_text, replace_contractions
from beautifultable import BeautifulTable

BLUE = '\033[230;48;5;25m'
BT = '\033[38;5;27m'
RST = '\033[0m'

def colored(a):
    res = list(BT+str(i) for i in a)
    return res

def pos_tagger(text):
    denoise = denoise_text(text)
    clean_text = replace_contractions(denoise)
    token = word_tokenize(clean_text)
    tag = nltk.pos_tag(token)
    univ_tag = nltk.pos_tag(token, tagset='universal')
    return clean_text, tag, univ_tag

def get_info(q):
    tags = {
            'VERB': 'verbs (all tenses and modes)',
            'NOUN': 'nouns (common and proper)',
            'PRON': 'pronouns',
            'ADJ': 'adjectives',
            'ADV': 'adverbs',
            'ADP': 'adpositions (prepositions and postpositions)',
            'CONJ': 'conjunctions',
            'DET': 'determiners',
            'NUM': 'cardinal numbers',
            'PRT': 'particles or other function words',
            'X': 'other: foreign words, typos, abbreviations',
            '.': 'punctuation'
            }
    return tags.get(q) if q in tags else ' '

def main():
    # create argument
    ap = argparse.ArgumentParser(description='POS Tag')
    ap.add_argument('infile', type=argparse.FileType('r'), default=sys.stdin, help='Input file text')
    args = ap.parse_args()
    
    text = args.infile.read()
    clean_text, tag, univ_tag = pos_tagger(text)

    print(BLUE+'Source:\n'+RST, text, '\n')
    print(BLUE+'Clean:\n'+RST, clean_text, '\n')
    table = BeautifulTable()
    table.column_headers = colored(["No", "Word", "POS Tag", "Universal Tag", "Info"])
    for i in range(len(tag)):
      table.append_row([i+1, tag[i][0], tag[i][1], univ_tag[i][1], get_info(univ_tag[i][1])])
    table.set_style(BeautifulTable.STYLE_BOX_DOUBLED)
    print(table)

if __name__ == '__main__':
    main()
