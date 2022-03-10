

## Obtain original sequence data

```
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/049/SRR17619849/SRR17619849_1.fastq.gz
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR176/049/SRR17619849/SRR17619849_2.fastq.gz
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR179/045/SRR17907745/SRR17907745_1.fastq.gz
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR179/045/SRR17907745/SRR17907745_2.fastq.gz
```

## Obtain kraken2/bracken database

large file ~38GB compressed, ~50GB uncompressed

```
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20210517.tar.gz
```

## Run kraken2

```
kraken2 --db k2_standard_20210517 --report --report SRR17619849_kraken2.txt --paired SRR17619849_1.fastq.gz SRR17619849_2.fastq.gz 
kraken2 --db k2_standard_20210517 --report --report SRR17907745_kraken2.txt --paired SRR17907745_1.fastq.gz SRR17907745_2.fastq.gz 
```

## Run bracken

```
bracken -d k2_standard_20210517 -i SRR17619849_kraken2.txt -o SRR17619849_bracken_abundances.tsv -r 250 -l S
bracken -d k2_standard_20210517 -i SRR17907745_kraken2.txt -o SRR17907745_bracken_abundances.tsv -r 150 -l S
```
