
# polledHiC

### NF-CORE HIC PIPELINE ON MARIA'S DATA

```
dir=/work2/project/fragencode/workspace/diffhic
reads=$dir/data/sus_scrofa/foetalmuscle
#runid=nfcoretest
runid=nfcorehic
outdir=$dir/results/hic/sus_scrofa/foetalmuscle/$runid
genome=/work2/project/fragencode/data/species/sus_scrofa/Sscrofa11.1/sus_scrofa.fa
chromsize=/work2/project/fragencode/data/species/sus_scrofa/Sscrofa11.1.90/chrom.len
frags=/work2/project/fragencode/data/species/sus_scrofa/Sscrofa11.1.90/restrictionfragments_HindIII.bed
script=$outdir.sh
log=$outdir.log
err=$outdir.err
```

Now constructing the script

```
echo '#!/bin/bash
#SBATCH -J '$runid'
#SBATCH -e '$err'
#SBATCH -o '$log'
#SBATCH -p workq
#SBATCH --mail-type=END,FAIL
#SBATCH --export=ALL
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G

mkdir -p '$outdir'
cd '$outdir'

module purge
module load bioinfo/nfcore-Nextflow-v19.04.0

# most are default options - skipping ICE because normalizing each technical replicate is not relevant
nextflow run nf-core/hic \
 -revision    1.1.0 \
 -profile     genotoul \
 -name      '$runid' \
 -c '"'"'/home/sfoissac/work/.nextflow/mount.conf'"'"' \
 --fasta      '$genome' \
 --bwt2_index '$genome' \
 --outdir     '$outdir' \
 --work-dir   '$outdir' \
 -resume \
 --reads      '"'"''$reads'/*_R{1,2}.fastq.gz'"'"' \
 --bwt2_opts_end2end '"'"'--very-sensitive -L 30 --score-min L,-0.6,-0.2 --end-to-end --reorder'"'"' \
 --bwt2_opts_trimmed '"'"'--very-sensitive -L 20 --score-min L,-0.6,-0.2 --end-to-end --reorder'"'"' \
 --min_mapq 10 \
 --restriction_site  '"'"'A^AGCTT'"'"' \
 --ligation_site     '"'"'AAGCTAGCTT'"'"' \
 --restriction_fragments '$frags' \
 --chromosome_size '$chromsize' \
 --min_insert_size 20 \
 --max_insert_size 1000 \
 --rm_singleton \
 --rm_dup \
 --bin_size                  '"'"'1000000,500000,200000,50000'"'"' \
 --ice_max_iter     100 \
 --ice_filer_low_count_perc  0.02 \
 --ice_filer_high_count_perc 0 \
 --ice_eps     0.1 \
 --skipIce\
 --skipCool' > $script
```

An finally launching the script

```
sbatch $script
```
