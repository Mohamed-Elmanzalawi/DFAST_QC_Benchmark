#$ -S /bin/bash
#$ -cwd
#$ -pe def_slot 10
#$ -l mem_req=150G,s_vmem=150G
#$ -l medium
#$ -o logs_gtdbtk
#$ -e logs_gtdbtk
## -l intel

conda activate dfast_qc

for SUB_DIR in {0..9}; do
GENOME_DIR=genomes_GEM10000/${SUB_DIR}
OUT_DIR=GTDBtk_GEM10000_results/${SUB_DIR}
gtdbtk classify_wf --genome_dir ${GENOME_DIR} --out_dir ${OUT_DIR} --mash_db GTDB_Mash_database/gtdb_ref_sketch.msh --cpus $NSLOTS
echo "${SUB_DIR} is done"
done

