#!/usr/bin/env python
import argparse
from beautifultable import BeautifulTable

BLUE = '\033[38;5;27m'
RST = '\033[0m'

def colored(a):
    res = list(BLUE+str(i) for i in a)
    return res

def med(s, t, costs=(1, 1, 2)):
    rows = len(s)+1
    cols = len(t)+1
    deletes, inserts, substitutes = costs
    
    # membuat matrix dummy
    dist = [[0 for x in range(cols)] for x in range(rows)]

    for row in range(1, rows):
        dist[row][0] = row * deletes

    for col in range(1, cols):
        dist[0][col] = col * inserts
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + cost) # substitution
    return dist, row, col


def print_med(s, t, dist):
    tb = BeautifulTable()
    tb.set_style(BeautifulTable.STYLE_NONE)
    tb.column_headers = colored([' ','#']+list(t))
    for r, i in zip(dist, list(range(len(s)+1))):
        tmp = s[i-1] if (i > 0) else '#'
        tb.append_row(colored(list(tmp)) + r)
    print(tb)


def main():
    # # create argument
    ap = argparse.ArgumentParser(description='Minimum Edit Distance')
    ap.add_argument('string1', help='String 1')
    ap.add_argument('string2', help='String 2')
    ap.add_argument('-c', type=int, dest='costs', required=False, nargs=3, 
                        metavar=('del', 'ins', 'sub'), help="levenshtein distance costs")
    args = ap.parse_args()
    string1 = args.string1
    string2 = args.string2
    costs = args.costs if args.costs is not None else [1,1,2]
    med_res, row, col  = med(string1, string2, costs)

    print('\nCosts (del ins sub): {}\n'.format(costs))
    print_med(string1, string2, med_res)
    print('\nLevenshtein Distance: {}'.format(med_res[row][col]))

if __name__ == '__main__':
    main()
