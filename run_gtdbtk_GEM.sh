#$ -S /bin/bash
#$ -cwd
#$ -pe def_slot 10
#$ -l mem_req=150G,s_vmem=150G
#$ -l medium
#$ -o logs_gtdbtk
#$ -e logs_gtdbtk
## -l intel

conda activate dfast_qc

if [ "$1" == "dummy" ]; then
    GENOME_DIR=genomes_GEM/0
    OUT_DIR=GTDBtk_GEM_results/0
    gtdbtk classify_wf --genome_dir ${GENOME_DIR} --out_dir ${OUT_DIR} --mash_db GTDB_Mash_database/gtdb_ref_sketch.msh --cpus $NSLOTS
    echo "dummy data is done"
    done
else
    for SUB_DIR in {0..9}; do
    GENOME_DIR=genomes_GEM/${SUB_DIR}
    OUT_DIR=GTDBtk_GEM_results/${SUB_DIR}
    gtdbtk classify_wf --genome_dir ${GENOME_DIR} --out_dir ${OUT_DIR} --mash_db GTDB_Mash_database/gtdb_ref_sketch.msh --cpus $NSLOTS
    echo "${SUB_DIR} is done"
    done
fi