#!/usr/bin/env python

from __future__ import print_function

import argparse
import re
import sys

from Cheetah.Template import Template


def stop_err( msg ):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)


class BLASTBin:
    def __init__(self, label, file):
        self.label = label
        self.dict = {}
        
        file_in = open(file)
        for line in file_in:
            self.dict[line.rstrip().split('.')[0]] = ''
        file_in.close()
    
    def __str__(self):
        return "label: %s    dict: %s" % (self.label, str(self.dict))


class BLASTQuery:
    def __init__(self, query_id):
        self.query_id = query_id
        self.matches = []
        self.match_accessions = {}
        self.bins = {} #{bin(label):[match indexes]}
        self.pident_filtered = 0
        self.kw_filtered = 0
        self.kw_filtered_breakdown = {} #{kw:count}
        
    def __str__(self):
        return "query_id: %s    len(matches): %s    bins (labels only): %s    pident_filtered: %s    kw_filtered: %s    kw_filtered_breakdown: %s" \
            % (self.query_id,
               str(len(self.matches)),
               str([bin.label for bin in bins]),
               str(self.pident_filtered),
               str(self.kw_filtered),
               str(self.kw_filtered_breakdown))


class BLASTMatch:
    def __init__(self, subject_acc, subject_descr, score, p_cov, p_ident, subject_bins):
        self.subject_acc = subject_acc
        self.subject_descr = subject_descr
        self.score = score
        self.p_cov = p_cov
        self.p_ident = p_ident
        self.bins = subject_bins
        
    def __str__(self):
        return "subject_acc: %s    subject_descr: %s    score: %s    p-cov: %s    p-ident: %s" \
            % (self.subject_acc,
               self.subject_descr,
               str(self.score),
               str(round(self.p_cov,2)),
               str(round(self.p_ident, 2)))


#PARSE OPTIONS AND ARGUMENTS
parser = argparse.ArgumentParser()

parser.add_argument('-f', '--filter-keywords',
                    dest='filter_keywords',
                    )
parser.add_argument('-i', '--min-identity',
                    dest='min_identity',
                    )
parser.add_argument('-b', '--bins',
                    dest='bins',
                    action='append',
                    nargs='+'
                    )
parser.add_argument('-r', '--discard-redundant',
                    dest='discard_redundant',
                    default=False,
                    action='store_true'
                    )
parser.add_argument('input_tab')
parser.add_argument('cheetah_tmpl')
parser.add_argument('output_html')
parser.add_argument('output_tab')

args = parser.parse_args()


print('input_tab: %s    cheetah_tmpl: %s    output_html: %s    output_tab: %s' % (args.input_tab, args.cheetah_tmpl, args.output_html, args.output_tab))


#BINS
bins=[]
if args.bins != None:
    for bin in args.bins:
        bins.append(BLASTBin(bin[0], bin[1]))

print('database bins: %s' % str([bin.label for bin in bins]))

#FILTERS
filter_pident = 0
filter_kws = []
if args.filter_keywords:
    filter_kws = args.filter_keywords.split(',')
print('minimum percent identity: %s    filter_kws: %s' % (str(args.min_identity), str(filter_kws)))

if args.discard_redundant:
    print('Throwing out redundant hits...')


PIDENT_COL = 2
DESCR_COL = 24
SUBJ_ID_COL = 12
SCORE_COL = 11
PCOV_COL = 25
queries = []
current_query = ''
output_tab = open(args.output_tab, 'w')
    
with open(args.input_tab) as input_tab:
    for line in input_tab:
        cols = line.split('\t')
        if cols[0] != current_query:
            current_query = cols[0]
            queries.append(BLASTQuery(current_query))

        try:
            accs = cols[SUBJ_ID_COL].split('|')[1::2][1::2]
        except IndexError as e:
            stop_err("Problem with splitting:" + cols[SUBJ_ID_COL])

        #hsp option: keep best (first) hit only for each query and accession id.
        if args.discard_redundant:
            if accs[0] in queries[-1].match_accessions:
                continue #don't save the result and skip to the next
            else:
                queries[-1].match_accessions[accs[0]] = ''


        p_ident = float(cols[PIDENT_COL])
        #FILTER BY PIDENT
        if p_ident < filter_pident: #if we are not filtering, filter_pident == 0 and this will never evaluate to True
            queries[-1].pident_filtered += 1
            continue
        
        descrs = cols[DESCR_COL]
        #FILTER BY KEY WORDS
        filter_by_kw = False
        for kw in filter_kws:
            kw = kw.strip()
            if kw != '' and re.search(kw, descrs, re.IGNORECASE):
                filter_by_kw = True
                try:
                    queries[-1].kw_filtered_breakdown[kw] += 1
                except:
                    queries[-1].kw_filtered_breakdown[kw] = 1
        if filter_by_kw: #if we are not filtering, for loop will not be entered and this will never be True
            queries[-1].kw_filtered += 1
            continue
        descr = descrs.split(';')[0]
        
        #ATTEMPT BIN
        subj_bins = []
        for bin in bins: #if we are not binning, bins = [] so for loop not entered
            for acc in accs:
                if acc.split('.')[0] in bin.dict:
                    try:
                        queries[-1].bins[bin.label].append(len(queries[-1].matches))
                    except:
                        queries[-1].bins[bin.label] = [len(queries[-1].matches)]
                    subj_bins.append(bin.label)
                    break #this result has been binned to this bin so break
        acc = accs[0]
        
        score = int(float(cols[SCORE_COL]))
        p_cov = float(cols[PCOV_COL])
        
        #SAVE RESULT
        queries[-1].matches.append(
            BLASTMatch(acc, descr, score, p_cov, p_ident, subj_bins)
        )
        output_tab.write(line)            
input_tab.close()
output_tab.close()

'''
for query in queries:
    print(query)
    for match in query.matches:
        print('    %s' % str(match))
    for bin in query.bins:
        print('    bin: %s' % bin)
        for x in query.bins[bin]:
            print('        %s' % str(query.matches[x]))
'''

namespace = {'queries': queries}
html = Template(file=args.cheetah_tmpl, searchList=[namespace])
out_html = open(args.output_html, 'w')
out_html.write(str(html))
out_html.close()

