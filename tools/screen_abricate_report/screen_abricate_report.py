#!/usr/bin/env python

from __future__ import print_function

import argparse
import csv
import re


class Range(object):
    """
    Used to limit the min_coverage and min_identity args to range 0.0 - 100.0
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start <= other <= self.end

    def __contains__(self, item):
        return self.__eq__(item)

    def __iter__(self):
        yield self

    def __repr__(self):
        return  str(self.start) + " - " + str(self.end)

def parse_screen_file(screen_file):
    screen = []
    with open(screen_file) as f:
        reader = csv.DictReader(f, delimiter="\t", quotechar='"')
        for row in reader:
            screen.append(row)
    return screen


def get_fieldnames(input_file):
    with open(input_file) as f:
        reader = csv.DictReader(f, delimiter="\t", quotechar='"')
        row = next(reader)
    fieldnames = row.keys()
    return fieldnames

def detect_gene(abricate_report_row, regex, min_coverage, min_identity):
    gene_of_interest = bool(re.search(regex, abricate_report_row['GENE']))
    sufficient_coverage = float(abricate_report_row['%COVERAGE']) >= min_coverage
    sufficient_identity = float(abricate_report_row['%IDENTITY']) >= min_identity
    if gene_of_interest and sufficient_coverage and sufficient_identity:
        return True
    else:
        return False


def main(args):
    screen = parse_screen_file(args.screening_file)
    gene_detection_status_fieldnames = ['gene_name', 'detected']
    with open(args.abricate_report, 'r') as f1, \
            open(args.screened_report, 'w') as f2, \
            open(args.gene_detection_status, 'w') as f3:
        abricate_report_reader = csv.DictReader(f1, delimiter="\t", quotechar='"')
        screened_report_writer = csv.DictWriter(f2, delimiter="\t", quotechar='"',
                                                fieldnames=abricate_report_reader.fieldnames)
        gene_detection_status_writer = csv.DictWriter(f3, delimiter="\t", quotechar='"',
                                                      fieldnames=gene_detection_status_fieldnames)
        screened_report_writer.writeheader()
        gene_detection_status_writer.writeheader()

        for gene in screen:
            gene_detection_status = {
                'gene_name': gene['gene_name'],
                'detected': False
            }
            for abricate_report_row in abricate_report_reader:
                if detect_gene(abricate_report_row, gene['regex'], args.min_coverage, args.min_identity):
                    gene_detection_status['detected'] = True
                    screened_report_writer.writerow(abricate_report_row)
            gene_detection_status_writer.writerow(gene_detection_status)
            f1.seek(0)  # return file pointer to start of abricate report
            next(abricate_report_reader)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("abricate_report", help="Input: Abricate report to screen (tsv)")
    parser.add_argument("--screening_file", help="Input: List of genes to screen for (tsv)")
    parser.add_argument("--screened_report", help=("Output: Screened abricate report, including only genes of interest (tsv)"))
    parser.add_argument("--gene_detection_status", help=("Output: detection status for all genes listed in the screening file (tsv)"))
    parser.add_argument("--min_coverage", type=float,  default=90.0, choices=Range(0.0, 100.0), help=("Minimum percent coverage"))
    parser.add_argument("--min_identity", type=float, default=90.0, choices=Range(0.0, 100.0), help=("Minimum percent identity"))
    args = parser.parse_args()
    main(args)
