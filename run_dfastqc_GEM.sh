#$ -S /bin/bash
#$ -cwd
#$ -pe def_slot 1
#$ -l mem_req=8G,s_vmem=8G
#$ -o logs/
#$ -e logs/
#$ -t 1-10000:1
#$ -tc 40

conda activate dfast_qc
export OMP_NUM_THREADS=1

# Extract task ID
NUM=$SGE_TASK_ID
NUM2=`printf %05d $NUM`

#Main directories
main_dir=$(pwd)
genebank_test_data=${main_dir}/gem_test_data
if [ -z "$1" ]; then
    echo "Please provide the path to the dfast_qc directory"
    exit 1
else
    dfast_qc_dir="$1"
fi

# Input file containing genome accessions
if [ -z "$2" ]; then
    GENOMELIST=${genebank_test_data}/gem_mags_10000_ID_list.tsv
else
    GENOMELIST="$2"
fi

LINE=`cat $GENOMELIST |head -$NUM |tail -1`
GENOME_ID=`echo $LINE | cut -d " " -f 1`
SUB_DIR=`echo $LINE | cut -d " " -f 2`

# Directory for storing downloaded genomes
GENOME_DIR_ROOT=genomes_GEM
URL_ROOT=https://portal.nersc.gov/GEM/genomes/fna

URL=${URL_ROOT}/${GENOME_ID}.fna.gz
GENOME_DIR=${GENOME_DIR_ROOT}/${SUB_DIR}
mkdir -p ${GENOME_DIR}

curl https://portal.nersc.gov/GEM/genomes/fna/${GENOME_ID}.fna.gz > ${GENOME_DIR}/${GENOME_ID}.fna.gz

gunzip ${GENOME_DIR}/${GENOME_ID}.fna.gz

GENOME_FASTA=${GENOME_DIR}/${GENOME_ID}.fna

#RefSeq & GTDB Taxonomy search
${dfast_qc_dir}/dfast_qc -i ${GENOME_FASTA} -o DQC_GEM_results/${NUM2}_${GENOME_ID} --force -r /home/melmanzalawi/dfast_qc/dqc_reference --enable_gtdb 

#MASH GTDB Taxonomy search
mash dist ${dfast_qc_dir}/dqc_reference/gtdb_genomes_sketch.msh ${GENOME_FASTA} > DQC_GEM_results/${NUM2}_${GENOME_ID}/distances_gtdb.tab
