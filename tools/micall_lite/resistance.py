#!/usr/bin/env python

from __future__ import print_function


import argparse


from pprint import pprintg


import yaml



HCV_RULES_VERSION = "1.8"


def load_rules_config(rules_config, genotype, backup_genotype=None):
    rules = {
        'drug_class': {},
        'drugs': {}
    }
    rules['alg_name'] = 'HCV_RULES'
    rules['alg_version'] = HCV_RULES_VERSION
    rules['level_def'] = {
        '-1': 'Resistance Interpretation Not Available',
        '0': 'Sequence does not meet quality-control standards',
        '1': 'Likely Susceptible',
        '2': 'Not Indicated',
        '3': 'Mutations Detected; Effect Unknown',
        '4': 'Resistance Possible',
        '5': 'Resistance Likely'
    }
    rules['global_range'] = [('-INF', '3', '1'), ('4', '7', '4'), ('8', 'INF', '5')]
    for drug in rules_config:
        drug_code = drug['code']
        drug_rules = []
        region = None
        for genotype_config in drug['genotypes']:
            region = genotype_config['region']
            rule_text = genotype_config['rules']
            if genotype_config['genotype'] == genotype:
                rules['gene_def'][genotype_config['reference']] = [region]
                break
            elif genotype_config['genotype'] == backup_genotype:
                rules['gene_def'].setdefault(genotype_config['reference'], [region])
                break
            else:
                rule_text = 'SCORE FROM ( TRUE => "Not available" )'
        drug_rules.append((rule_text, [('scorerange', 'useglobalrange')]))
        try:
            rules['drug_class'][region].append(drug_code)
        except KeyError:
            rules['drug_class'][region] = [drug_code]
        rules['drugs'][drug_code] = (drug['name'], drug_rules)
    return rules


def main(args):
    with open(args.rules) as f:
        rules = load_rules_config(yaml.safe_load(f), None)
    pprint(rules)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("consensus", help="Consensus fasta")
    parser.add_argument("--rules", help="Rules file (yaml)")
    args = parser.parse_args()
    main(args)
