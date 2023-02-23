#!/usr/bin/env python

import argparse
import datetime
import glob
import json
import os
import sys
import urllib.request

from zipfile import ZipFile

def get(url):
    response_content = None
    request = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(request) as response:
            response_content = response.read()
    except:
        log_msg = {
            'timestamp': str(datetime.datetime.now().isoformat()),
            'event': 'connection_error',
            'url': url,
        }
        print(json.dumps(log_msg), file=sys.stderr)
        exit(-1)

    return response_content
        

def main(args):
    
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)

    alleles_url = '/'.join([
        'https://www.cgmlst.org/ncs/schema',
        args.scheme_id,
        'alleles/',
    ])

    alleles_zip_data = get(alleles_url)
    alleles_zip_path = os.path.join(args.outdir, 'alleles.zip')
    with open(alleles_zip_path, 'wb') as f:
        f.write(alleles_zip_data)

    with ZipFile(alleles_zip_path, 'r') as f:
        f.extractall(args.outdir)

    if os.path.exists(alleles_zip_path):
        os.remove(alleles_zip_path)

    with open(os.path.join(args.outdir, 'scheme.fa'), 'w') as scheme_file:
        for fasta_file_path in glob.glob(os.path.join(args.outdir, '*.fasta')):
            locus_id = os.path.basename(fasta_file_path).split('.')[0].replace('_', '-')
            with open(fasta_file_path, 'r') as fasta_file:
                for line in fasta_file.readlines():
                    if line.startswith('>'):
                        allele_id = line.lstrip('>')
                        new_defline = '>' + locus_id + '_' + allele_id
                        scheme_file.write(new_defline)
                    else:
                        scheme_file.write(line)
            os.remove(fasta_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheme-id", "-i", required=True, help="scheme id")
    parser.add_argument("--outdir", "-o", dest="outdir", default='./scheme', help="output directory")
    args = parser.parse_args()
    main(args)
