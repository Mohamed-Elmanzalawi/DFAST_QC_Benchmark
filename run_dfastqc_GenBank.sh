#$ -S /bin/bash
#$ -cwd
#$ -pe def_slot 1
#$ -l mem_req=8G,s_vmem=8G
#$ -o logs_genebank/
#$ -e logs_genebank/
#$ -t 1-5688:1
#$ -tc 40

conda activate dfast_qc
export OMP_NUM_THREADS=1

# Extract task ID
NUM=$SGE_TASK_ID
NUM2=`printf %04d $NUM`

#Main directories
main_dir=$(pwd)
genebank_test_data=${main_dir}/genbank_test_data
if [ -z "$1" ]; then
    echo "Please provide the path to the dfast_qc directory"
    exit 1
else
    dfast_qc_dir="$1"
fi

# Input file containing genome accessions
if [ -z "$2" ]; then
    GENOMELIST=${genebank_test_data}/genbank_prok_1_per_species_accession.tsv
else
    GENOMELIST="$2"
fi
ACCESSION=`cat $GENOMELIST |head -$NUM |tail -1`

# Directory for storing downloaded genomes
GENOME_DIR_ROOT=${main_dir}/genomes_genebank


./dfast_file_downloader.py --assembly_fasta ${ACCESSION} --out $GENOME_DIR_ROOT

GENOME_FASTA=${GENOME_DIR_ROOT}/${ACCESSION}.fna

#RefSeq & GTDB Taxonomy search
${dfast_qc_dir}/dfast_qc  -i ${GENOME_FASTA} -o DQC_genebank_results/${NUM2}_${ACCESSION} --force -r /home/melmanzalawi/dfast_qc/dqc_reference  --enable_gtdb

#MASH RefSeq Taxonomy search
mash dist ${dfast_qc_dir}/dqc_reference/ref_genomes_sketch.msh ${GENOME_FASTA} > DQC_genebank_results/${NUM2}_${ACCESSION}/distances_ref.tab


