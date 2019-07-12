#!/usr/bin/env python
import sys, os, argparse
import re

def RegEx(s, q):
    foundCol = '\033[30;48;5;82m'
    notFoundCol = '\033[230;48;5;1m'
    resetCol = '\033[0m'

    count = 0
    lastMatch = 0
    formattedText = ''
    tmp = re.finditer(q, s)
    for match in tmp:
        start, end = match.span()
        formattedText += s[lastMatch: start]
        formattedText += foundCol
        formattedText += s[start: end]
        formattedText += resetCol
        lastMatch = end
        count += 1
    formattedText += s[lastMatch:]

    if(count == 0):
        formattedText = notFoundCol + 'Not Found' + resetCol

    return formattedText


def main():
    # create argument
    ap = argparse.ArgumentParser(description='Simple RegEx')
    ap.add_argument('infile', type=argparse.FileType('r'), default=sys.stdin, help='Input file text')
    ap.add_argument('-p', '--pattern', required=True, help='Regular Expression pattern')
    args = ap.parse_args()
    
    res = RegEx(args.infile.read(), args.pattern)
    print(res)


if __name__ == '__main__':
    if os.name != 'posix':
        print('OS tidak support')
        sys.exit(1)
    main()
