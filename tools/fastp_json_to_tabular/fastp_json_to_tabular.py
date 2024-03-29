#!/usr/bin/env python

import argparse
import json

def main(args):
    with open(args.fastp_json, 'r') as f:
        fastp_report = json.load(f)

    reads_single_paired = fastp_report['summary']['sequencing'].split(' ')[0]

    if reads_single_paired == 'paired':
        total_read_pairs_before_filtering = str(int(int(fastp_report['summary']['before_filtering']['total_reads']) / 2))
        total_read_pairs_after_filtering = str(int(int(fastp_report['summary']['after_filtering']['total_reads']) / 2))
        read2_mean_length_before_filtering = fastp_report['summary']['before_filtering']['read2_mean_length']
        read2_mean_length_after_filtering = fastp_report['summary']['after_filtering']['read2_mean_length']
    else:
        total_read_pairs_before_filtering = 'NA'
        total_read_pairs_after_filtering = 'NA'
        read2_mean_length_before_filtering = 'NA'
        read2_mean_length_after_filtering = 'NA'

    total_reads_before_filtering = fastp_report['summary']['before_filtering']['total_reads']
    total_reads_after_filtering = fastp_report['summary']['after_filtering']['total_reads']

    total_bases_before_filtering = fastp_report['summary']['before_filtering']['total_bases']
    total_bases_after_filtering = fastp_report['summary']['after_filtering']['total_bases']

    read1_mean_length_before_filtering = fastp_report['summary']['before_filtering']['read1_mean_length']
    read1_mean_length_after_filtering = fastp_report['summary']['after_filtering']['read1_mean_length']

    q20_bases_before_filtering = fastp_report['summary']['before_filtering']['q20_bases']
    q20_bases_after_filtering = fastp_report['summary']['after_filtering']['q20_bases']

    q20_rate_before_filtering = fastp_report['summary']['before_filtering']['q20_rate']
    q20_rate_after_filtering = fastp_report['summary']['after_filtering']['q20_rate']

    q30_bases_before_filtering = fastp_report['summary']['before_filtering']['q30_bases']
    q30_bases_after_filtering = fastp_report['summary']['after_filtering']['q30_bases']

    q30_rate_before_filtering = fastp_report['summary']['before_filtering']['q30_rate']
    q30_rate_after_filtering = fastp_report['summary']['after_filtering']['q30_rate']

    gc_content_before_filtering = fastp_report['summary']['before_filtering']['gc_content']
    gc_content_after_filtering = fastp_report['summary']['after_filtering']['gc_content']
    if 'adapter_cutting' in fastp_report:
        adapter_trimmed_reads = fastp_report['adapter_cutting']['adapter_trimmed_reads']
        adapter_trimmed_bases = fastp_report['adapter_cutting']['adapter_trimmed_bases']
    else:
        adapter_trimmed_reads = 0
        adapter_trimmed_bases = 0

    output_fields = [
        'total_reads_before_filtering',
        'total_read_pairs_before_filtering',
        'total_reads_after_filtering',
        'total_read_pairs_after_filtering',
        'total_bases_before_filtering',
        'total_bases_after_filtering',
        'read1_mean_length_before_filtering',
        'read1_mean_length_after_filtering',
        'read2_mean_length_before_filtering',
        'read2_mean_length_after_filtering',
        'q20_bases_before_filtering',
        'q20_bases_after_filtering',
        'q20_rate_before_filtering',
        'q20_rate_after_filtering',
        'q30_bases_before_filtering',
        'q30_bases_after_filtering',
        'q30_rate_before_filtering',
        'q30_rate_after_filtering',
        'gc_content_before_filtering',
        'gc_content_after_filtering',
        'adapter_trimmed_reads',
        'adapter_trimmed_bases',
    ]

    output_data = []
    if args.sample_id:
        output_fields = ['sample_id'] + output_fields
        output_data = [args.sample_id]

    print(args.delimiter.join(output_fields))

    output_data = output_data + [
        total_reads_before_filtering,
        total_read_pairs_before_filtering,
        total_reads_after_filtering,
        total_read_pairs_after_filtering,
        total_bases_before_filtering,
        total_bases_after_filtering,
        read1_mean_length_before_filtering,
        read1_mean_length_after_filtering,
        read2_mean_length_before_filtering,
        read2_mean_length_after_filtering,
        q20_bases_before_filtering,
        q20_bases_after_filtering,
        q20_rate_before_filtering,
        q20_rate_after_filtering,
        q30_bases_before_filtering,
        q30_bases_after_filtering,
        q30_rate_before_filtering,
        q30_rate_after_filtering,
        gc_content_before_filtering,
        gc_content_after_filtering,
        adapter_trimmed_reads,
        adapter_trimmed_bases,
    ]
    print(args.delimiter.join(map(str, output_data)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fastp_json')
    parser.add_argument('-s', '--sample-id')
    parser.add_argument('-d', '--delimiter', default='\t')
    args = parser.parse_args()
    main(args)
