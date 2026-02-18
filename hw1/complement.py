#!/Users/macbook/anaconda3/bin/python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--seq')

args = parser.parse_args()

nucl = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

output = ''
gc = 0
for letter in args.seq:
    output += nucl[letter]
    if letter in ['G', 'C']:
        gc += 1
print(output[::-1])
print(f'{gc/len(args.seq):.3f}')

