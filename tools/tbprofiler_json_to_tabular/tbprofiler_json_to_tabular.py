#!/usr/bin/env python

import argparse
import csv
import json
        

def main(args):

    with open(args.input, 'r') as f:
        report = json.load(f)

    qc_fieldnames = [
        'pct_reads_mapped',
        'num_reads_mapped',
        'median_coverage',
    ]

    with open(args.qc, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=qc_fieldnames, dialect='excel-tab', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        output = {k: report['qc'][k] for k in qc_fieldnames}
        writer.writerow(output)

    gene_coverage_fieldnames = [
        'locus_tag',
        'gene',
        'fraction',
        'cutoff',
    ]

    with open(args.gene_coverage, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=gene_coverage_fieldnames, dialect='excel-tab', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in report['qc']['gene_coverage']:
            writer.writerow(row)

    missing_positions_fieldnames = [
        'locus_tag',
        'gene',
        'position',
        'variants',
        'drugs'
    ]

    with open(args.missing_positions, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=missing_positions_fieldnames, dialect='excel-tab', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in report['qc']['missing_positions']:
            writer.writerow(row)

    resistance_variants_fieldnames = [
        'chrom',
        'genome_pos',
        'locus_tag',
        'feature_id',
        'gene',
        'type',
        'ref',
        'alt',
        'freq',
        'nucleotide_change',
        'protein_change',
        'change',
        'drugs',
    ]

    with open(args.resistance_variants, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=resistance_variants_fieldnames, dialect='excel-tab', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in report['dr_variants']:
            row['drugs'] = ', '.join([drug['drug'] + ':' + drug['confers'] for drug in row['drugs']])
            output = {k: row[k] for k in resistance_variants_fieldnames}
            writer.writerow(output)

    other_variants_fieldnames = [
        'chrom',
        'genome_pos',
        'locus_tag',
        'feature_id',
        'gene',
        'type',
        'ref',
        'alt',
        'freq',
        'nucleotide_change',
        'protein_change',
        'change',
        'gene_associated_drugs',
    ]

    with open(args.other_variants, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=other_variants_fieldnames, dialect='excel-tab', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in report['other_variants']:
            row['gene_associated_drugs'] = ', '.join(row['gene_associated_drugs'])
            output = {k: row[k] for k in other_variants_fieldnames}
            writer.writerow(output)

    analysis_metadata_fieldnames = [
        'timestamp',
        'tbprofiler_version',
        'mapping_program',
        'variant_calling_program',
        'db_name',
        'db_commit',
        'db_date',
    ]

    with open(args.analysis_metadata, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=analysis_metadata_fieldnames, dialect='excel-tab', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        output = {}
        output['timestamp'] = report['timestamp']
        output['tbprofiler_version'] = report['tbprofiler_version']
        output['db_name'] = report['db_version']['name']
        output['db_commit'] = report['db_version']['commit']
        output['db_date'] = report['db_version']['Date']
        for pipeline_entry in report['pipeline']:
            if pipeline_entry['Analysis'] == "Mapping":
                output['mapping_program'] = pipeline_entry['Program']
            elif pipeline_entry['Analysis'] == "Variant calling":
                output['variant_calling_program'] = pipeline_entry['Program']
        
        writer.writerow(output)
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--qc')
    parser.add_argument('--gene-coverage')
    parser.add_argument('--missing-positions')
    parser.add_argument('--resistance-variants')
    parser.add_argument('--other-variants')
    parser.add_argument('--analysis-metadata')
    args = parser.parse_args()
    main(args)
