#!/Users/macbook/anaconda3/bin/python

import argparse
from collections import defaultdict as dd
import json
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fa')
parser.add_argument('-k', '--kmer')
parser.add_argument('-o', '--out')

args = parser.parse_args()

#
# Logging initialization
#
logging.basicConfig(level=logging.DEBUG)
logging.info("script name: {}".format(args[0]))
logging.info("input fasta file: {}".format(args.fa))
logging.info("input kmer length: {}".format(args.kmer))
logging.info("input output file: {}".format(args.out))

out = {}
def count_kmers(name, seq, k):
    seq_stats = dd(int)
    for i in range(len(seq) - k + 1):
        seq_stats[seq[i:i+k]] += 1
    
    out[name] = dict(seq_stats)

seq = ''
name = None
with open(args.fa, 'r') as file:
    for line in file:
        if line[0] == '>':
            if seq != '':
                count_kmers(name, seq, k = int(args.kmer))
            name = line.strip()
            seq = ''
        else:
            seq += line.strip()
    count_kmers(name, seq, k = int(args.kmer))
file.close()

with open(args.out, 'w') as file:
    json.dump(out, file, indent=4)

logging.info("done!")