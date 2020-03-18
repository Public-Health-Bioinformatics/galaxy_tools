#!/usr/bin/env python

from __future__ import print_function

import argparse
import csv
import json


def parse_primer_scheme(primer_scheme):
    primer_pairs = []
    fieldnames = [
        'ref',
        'start',
        'end',
        'primer_name',
        'pool',
    ] 
    with open(primer_scheme) as f:
        reader = csv.DictReader(f, delimiter="\t", quotechar='"', fieldnames=fieldnames)
        for row in reader:
            primer_pairs.append(row)
    return primer_pairs


def main(args):
    primer_pairs = parse_primer_scheme(args.primer_scheme)
    print(json.dumps(primer_pairs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("primer_scheme", help="Input: Primer Scheme (.bed)")
    args = parser.parse_args()
    main(args)
