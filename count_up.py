#!/usr/bin/env python

# this is a python script template
# this next line will download the file using curl

gff="Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.37.gff3.gz"
fasta="Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.dna.chromosome.Chromosome.fa.gz"

import re, csv,os,gzip,itertools

# this is code which will parse FASTA files
# define what a header looks like in FASTA format
def isheader(line):
    return line[0] == '>'

def aspairs(f):
    seq_id = ''
    sequence = ''
    for header,group in itertools.groupby(f, isheader):
        if header:
            line = next(group)
            seq_id = line[1:].split()[0]
        else:
            sequence = ''.join(line.strip() for line in group)
            yield seq_id, sequence



if not os.path.exists(gff):
    os.system("curl -O ftp://ftp.ensemblgenomes.org/pub/bacteria/release-45/gff3/bacteria_0_collection/escherichia_coli_str_k_12_substr_mg1655/Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.37.gff3.gz")

if not os.path.exists(fasta):
    os.system("curl -O ftp://ftp.ensemblgenomes.org/pub/bacteria/release-45/fasta/bacteria_0_collection/escherichia_coli_str_k_12_substr_mg1655/dna/Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.dna.chromosome.Chromosome.fa.gz")

    
with gzip.open(gff,"rt") as fh:
    file = csv.reader (fh, delimiter= '\t')

    gene_count = 0
    total_gene_length = 0
    for row in file:
#        print (row)    
        if row[0].startswith ("#"):
            continue
        gene = re.match (r'gene', row[2])
        if gene:
            gene_count += 1
            gene_length = int(row[4]) - int(row[3])
            total_gene_length += gene_length    
    print ("number of genes is", gene_count)
    print ("total length of the genes is", total_gene_length)


with gzip.open(fasta,"rt") as f:
    seqs = dict(aspairs(f))
    
    for k,v in seqs.items():
        genome_length = len(v)
        print("total length of genome is", genome_length)
        
    print("the percentage of them genome which is coding is", total_gene_length/genome_length*100)

