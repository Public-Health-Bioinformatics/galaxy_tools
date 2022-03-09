#!/usr/bin/env python

import argparse
import csv
import json
import sys

def parse_bracken_abundances(bracken_abundances_path):
    bracken_abundances = []
    with open(bracken_abundances_path, 'r') as f:
        reader = csv.DictReader(f, dialect='excel-tab')
        for row in reader:
            b = {}
            b['name'] = row['name']
            b['taxonomy_id'] = row['taxonomy_id']
            b['taxonomy_lvl'] = row['taxonomy_lvl']
            b['kraken_assigned_reads'] = int(row['kraken_assigned_reads'])
            b['added_reads'] = int(row['added_reads'])
            b['new_est_reads'] = int(row['new_est_reads'])
            b['bracken_fraction_total_reads'] = float(row['fraction_total_reads'])
            bracken_abundances.append(b)

    return bracken_abundances


def parse_kraken_report(kraken_report_path):
    kraken_report = []
    with open(kraken_report_path, 'r') as f:
        for line in f:
            kraken_line = {}
            [percentage, reads_total, reads_this_level, taxonomic_level, ncbi_taxid, taxon_name] = line.strip().split(None, 5)
            kraken_line['percentage'] = float(percentage)
            kraken_line['reads_total'] = int(reads_total)
            kraken_line['reads_this_level'] = int(reads_this_level)
            kraken_line['taxonomic_level'] = taxonomic_level
            kraken_line['ncbi_taxid'] = ncbi_taxid
            kraken_line['taxon_name'] = taxon_name
            kraken_report.append(kraken_line)

    return kraken_report


def main(args):
    kraken_report = parse_kraken_report(args.kraken_report)
    bracken_abundances = parse_bracken_abundances(args.bracken_abundances)

    kraken_report_unclassified_reads = list(filter(lambda x: x['taxon_name'] == 'unclassified', kraken_report))[0]['reads_this_level']
    kraken_report_classified_reads = list(filter(lambda x: x['taxon_name'] == 'root', kraken_report))[0]['reads_total']

    total_reads = kraken_report_classified_reads + kraken_report_unclassified_reads
    percent_unclassified = float(kraken_report_unclassified_reads) / float(total_reads)

    bracken_unclassified_entry = {
        'name': 'unclassified',
        'taxonomy_id': 0,
        'taxonomy_lvl': 'U',
        'kraken_assigned_reads': kraken_report_unclassified_reads,
        'added_reads': 0,
        'new_est_reads': kraken_report_unclassified_reads,
        'kraken_fraction_total_reads': percent_unclassified,
        'bracken_fraction_total_reads': 0.0,
    }

    bracken_abundances = [bracken_unclassified_entry] + bracken_abundances

    output_fieldnames = [
        'name',
        'taxonomy_id',
        'taxonomy_lvl',
        'kraken_assigned_reads',
        'added_reads',
        'new_est_reads',
        'total_reads',
        'kraken_fraction_total_reads',
        'bracken_fraction_total_reads',
    ]

    writer = csv.DictWriter(sys.stdout, fieldnames=output_fieldnames, dialect='excel-tab')
    writer.writeheader()
    
    for b in bracken_abundances:
        b['total_reads'] = total_reads
        kraken_adjusted_fraction_total_reads = float(b['kraken_assigned_reads']) / float(total_reads)
        b['kraken_fraction_total_reads'] = '{:.6f}'.format(kraken_adjusted_fraction_total_reads)
        bracken_adjusted_fraction_total_reads = float(b['new_est_reads']) / float(total_reads)
        b['bracken_fraction_total_reads'] = '{:.6f}'.format(bracken_adjusted_fraction_total_reads)

    for b in sorted(bracken_abundances, key=lambda x: x['bracken_fraction_total_reads'], reverse=True):
        writer.writerow(b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--kraken-report')
    parser.add_argument('-a', '--bracken-abundances')
    args = parser.parse_args()
    main(args)
