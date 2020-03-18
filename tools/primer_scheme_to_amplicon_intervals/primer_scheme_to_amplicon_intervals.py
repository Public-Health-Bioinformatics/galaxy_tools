#!/usr/bin/env python

from __future__ import print_function

import argparse
import csv
import json


def parse_primer_scheme(primer_scheme):
    primer_pairs = {}
    fieldnames = [
        'ref',
        'start',
        'end',
        'primer_name',
        'pool',
    ]
    primer_pair_names = set()
    with open(primer_scheme) as f:
        reader = csv.DictReader(f, delimiter="\t", quotechar='"', fieldnames=fieldnames)
        for row in reader:
            pair_name = '_'.join(row['primer_name'].split('_')[0:2])
            left_right = row['primer_name'].split('_')[2].lower()
            if pair_name not in primer_pairs.keys():
                primer_pairs[pair_name] = {}
                primer_pairs[pair_name][left_right] = {
                    'start': int(row['start']),
                    'end': int(row['end']),
                }
            else:
                primer_pairs[pair_name][left_right] = {
                    'start': int(row['start']),
                    'end': int(row['end']),
                }
            

    return primer_pairs


def main(args):
    primer_pairs = parse_primer_scheme(args.primer_scheme)
    print(json.dumps(primer_pairs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("primer_scheme", help="Input: Primer Scheme (.bed)")
    args = parser.parse_args()
    main(args)
