#!/Users/macbook/anaconda3/bin/python

import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--seq')

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)
logging.info("script name: {}".format(args[0]))
logging.info("input sequence: {}".format(args.seq))

nucl = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

output = ''
gc = 0
for letter in args.seq:
    output += nucl[letter]
    if letter in ['G', 'C']:
        gc += 1
print(output[::-1])
print(f'{gc/len(args.seq):.3f}')

logging.info("reversed-complement sequence: {}".format(output[::-1]))
logging.info("GC-content (input seq): {}".format(gc/len(args.seq)))