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
    ap.add_argument('-n', '--ngram', type=int, help="mode n-gram")
    args = ap.parse_args()

    text = args.infile.read()
    result = ''

    denoise = denoise_text(text)
    clean_text = replace_contractions(denoise)
    unigram = word_tokenize(clean_text)
    if args.unigram:
    	result = unigram
    	label = 'Unigram'
    if args.bigram:
    	result = list(bigrams(unigram))
    	label = 'Bigram'
    if args.ngram:
    	result = list(ngrams(unigram, args.ngram))
    	label = 'N-Gram -> '+str(args.ngram)

    print(BLUE+label+':'+RST+'\n', result)


if __name__ == '__main__':
	main()
