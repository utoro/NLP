#!/usr/bin/env python
import sys, argparse
from nltk import bigrams, trigrams, ngrams,word_tokenize
from preprocessing import denoise_text, replace_contractions

BLUE = '\033[230;48;5;25m'
ERR = '\033[230;48;5;1m'
RST = '\033[0m'

def main():
	# # create argument
    ap = argparse.ArgumentParser(description='Unigram Bigram N-Gram')
    ap.add_argument('infile', type=argparse.FileType('r'), default=sys.stdin, help='Input file text')
    ap.add_argument('--unigram', action='store_true', help='mode unigram')
    ap.add_argument('--bigram', action='store_true', help='mode bigram')
    ap.add_argument('--trigram', action='store_true', help='mode trigram')
    ap.add_argument('-n', '--ngram', type=int, help="mode n-gram")
    args = vars(ap.parse_args())

    text = args['infile'].read()
    denoise = denoise_text(text)
    clean_text = replace_contractions(denoise)
    unigram = word_tokenize(clean_text)

    opr = {'unigram': [unigram, 'Unigram'], 'bigram': [bigrams, 'Bigram'], 
         'trigram': [trigrams, 'Trigram'], 'ngram': [ngrams, 'N-Gram -> {}'.format(args['ngram'])]}

    c = 0
    for i in opr.keys():
        if args[i]:
            result = unigram if i == 'unigram' else list(opr[i][0](unigram, args['ngram'])) \
                  if i == 'ngram' else list(opr[i][0](unigram))
            print('{}{}:{}\n{}\n'.format(BLUE, opr[i][1],RST, result))
            c += 1

    if c == 0:
        ap.print_usage()
        sys.exit(1)


if __name__ == '__main__':
	main()
