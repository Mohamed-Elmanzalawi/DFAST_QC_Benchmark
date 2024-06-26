#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -l s_vmem=8G
#$ -l mem_req=8G
#$ -l d_rt=144:00:00
#$ -l s_rt=144:00:00

conda activate dfast_qc
export OMP_NUM_THREADS=1

main_dir= $(pwd)
genebank_test_data=${main_dir}/genebank_test_data
python summarize_genebank_results.py -r ${main_dir}/DQC_genebank_results -as ${genebank_test_data}/assembly_summary_genbank.txt -ani ${genebank_test_data}/ANI_report_prokaryotes.txt
