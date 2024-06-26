#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -l s_vmem=8G
#$ -l mem_req=8G
#$ -l d_rt=144:00:00
#$ -l s_rt=144:00:00

# Tip: you can run the following command to excute the script once run_dfastqc_GenBank.sh is done:
#      qsub -hold_jid run_dfastqc_GenBank.sh summary_GenBank_job.sh
#      This is for NIG-SC. Other HPC systems will require different formate.

conda activate dfast_qc
export OMP_NUM_THREADS=1

main_dir= $(pwd)
genebank_test_data=${main_dir}/genebank_test_data
python summarize_genebank_results.py -r ${main_dir}/DQC_genebank_results -as ${genebank_test_data}/assembly_summary_genbank.txt -ani ${genebank_test_data}/ANI_report_prokaryotes.txt
