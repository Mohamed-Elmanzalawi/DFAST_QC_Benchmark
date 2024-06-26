# Description: GenBank Dataset for evaluation of Taxonomy check generation script. 
import pandas as pd
import os
import subprocess
from logging import getLogger, INFO, basicConfig
from argparse import ArgumentParser

# Define the logger 
logger = getLogger()
basicConfig(level=INFO,format="%(asctime)s-%(levelname)s- %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def test_data_GeneBank(dfastqc_genome_directory):
    logger.info("===== Starting the script =====")
    def run_command(cmd, task_name=None, shell=True):
        if task_name:
            logger.info("Task started: %s", task_name)
        if shell:
            cmd = " ".join(cmd)
        logger.info("Running command: %s", cmd)
        p = subprocess.run(cmd, shell=shell, encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if p.returncode != 0:
            logger.error("Command failed. Aborted. [%s]", cmd)
            logger.error("Output: %s\n%s", "-" * 80, p.stdout)
            exit(1)
        else:
            if task_name:
                logger.info("Task succeeded: %s", task_name)
            if p.stdout:
                logger.debug("%s output %s\n%s%s", task_name, "-" * 50, p.stdout, "-" * 50)

    # Define the main directory and genbank_test_data directory
    main_dir = os.getcwd()
    genbank_test_data = os.path.join(main_dir, "genbank_test_data")

    # Create the directory if it doesn't exist
    logger.info(f"Creating the directory GenBank analysis.")
    os.makedirs(genbank_test_data, exist_ok=True)
    logger.info("Done")

    # Specify the directory containing our genomes.
    if dfastqc_genome_directory:
        genome_directory = dfastqc_genome_directory
    else:
        logger.error("Please provide the path to the directory containing the genomes.")
        exit(1)

    logger.info(f"{genome_directory} is the directory containing the genomes .. creating a list of all genomes.")
    # List all genomes in the directory.
    all_genomes = os.listdir(genome_directory)
    for index, genome_file in enumerate(all_genomes):
        # replace ".fna.gz" with blank space.
        all_genomes[index] = genome_file.replace(".fna.gz", "")
    logger.info("Done")

    assemply_report_cmd = ["curl","-o","genbank_test_data/assembly_summary_genbank.txt","-L","https://ftp.ncbi.nlm.nih.gov/genomes/genbank/assembly_summary_genbank.txt"]
    ani_report_cmd = ["curl","-o","genbank_test_data/ANI_report_prokaryotes.txt","-L","https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/ANI_report_prokaryotes.txt"]
    logger.info("Downloading assembly_summary_genbank.txt and ANI_report_prokaryotes.txt")
    run_command(assemply_report_cmd)
    run_command(ani_report_cmd)


    df_refseq = pd.read_table("genbank_test_data/assembly_summary_genbank.txt", skiprows=1,dtype={34: str, 35: str, 36: str})
    # inplace is set to True, as it modifies the original DataFrame in place and does not return a new DataFrame.
    df_refseq.rename(columns={'#assembly_accession': 'assembly_accession'}, inplace=True)

    logger.info("Filtering the data to have only bacteria and archaea and the latest version of the genome.")
    df_refseq_prok = df_refseq[df_refseq["group"].isin(["bacteria", "archeae"])]
    df_refseq_prok_latest = df_refseq_prok[df_refseq_prok["version_status"]=="latest"]
    logger.info("Done")

    logger.info("Merging the data with ANI_report_prokaryotes.txt and filtering the data to have only OK taxonomy check status.")
    ani_report = pd.read_csv("genbank_test_data/ANI_report_prokaryotes.txt", sep = "\t")
    df_refseq_prok_latest_ok= pd.merge(df_refseq_prok_latest, ani_report[["taxonomy-check-status",'# genbank-accession']], left_on='assembly_accession', right_on='# genbank-accession', how='left')
    df_refseq_prok_latest_ok = df_refseq_prok_latest_ok.drop('# genbank-accession', axis=1)
    df_refseq_prok_latest_ok = df_refseq_prok_latest_ok[df_refseq_prok_latest_ok["taxonomy-check-status"]=="OK"]
    logger.info("Done")


    logger.info("Filtering the data to have non type material and unique genomes not in out list of genomes.")
    # Genomes in RefSeq but not in our reference data + No type material was found. 
    df_uniq_genome = df_refseq_prok_latest_ok[~df_refseq_prok_latest_ok["assembly_accession"].isin(all_genomes)]
    df_uniq_genome = df_uniq_genome[df_uniq_genome["relation_to_type_material"]=="na"]
    logger.info("Done")

    # Candidatus, uncultured 
    def is_valid_name(S):
        organism = S["organism_name"]
        exclude_names = ["Enterobacter cloacae complex sp.", "Pseudomonas fluorescens group sp.", "Bacillus cereus group sp.", "Citrobacter freundii complex sp."]
        for name in exclude_names:
            if organism.startswith(name):
                return False
        org_split = organism.split()
        if len(org_split)==1:
            return False
        else:
            first_word, second_word = org_split[0:2]
        if second_word in ["sp.", "bacterium", "cf.", "endosymbiont", "symbiont", "genomosp."]:   # Clostridiales bacterium,  Cyanosarcina cf.    Spiroplasma endosymbiont     Type-E symbiont of Plautia stali     Agrobacterium genomosp. 3 str. CFBP 6623
            return False
        first_letter = first_word[0]
        if first_letter.islower():
            return False
        if first_word in ["Candidatus", "uncultured", "SAR324"]:  # synthetic, unidentified prokaryote, SAR324 cluster bacterium
            return False
        else:
            return True

    logger.info("Removing Candidatus, uncultured and unidentified prokaryotes .. etc. from the data.")
    # Removing uncultured and unidentified prokaryotes
    df_uniq_genome=df_uniq_genome[df_uniq_genome.apply(is_valid_name, axis = 1)]
    logger.info("Done")

    logger.info("Removing duplicates from species_taxid to have only one from each species_taxid.")
    # Removing duplicates from species_taxid to have only one from each species_taxid
    df_uniq_genome = df_uniq_genome.sample(frac=1).drop_duplicates(subset="species_taxid")
    logger.info("Done")

    logger.info("Saving the data and creating a dummy data for testing.")
    # saving the data
    df_uniq_genome.to_csv("genbank_test_data/genbank_prok_1_per_species.tsv", header=True, index=False, sep="\t")
    df_uniq_genome.to_csv("genbank_test_data/genbank_prok_1_per_species_accession.tsv", columns=["assembly_accession"], header=False, index=False, sep="\t")

    # Dummy data for testing
    df_uniq_genome_dummy = df_uniq_genome.head(5)
    df_uniq_genome_dummy.to_csv("genbank_test_data/genbank_prok_1_per_species_dummy.tsv", columns=["assembly_accession"],  header=False, index=False, sep="\t")
    logger.info("Done")

    # Number of genomes to be adjusted in the HPC job file.
    number_of_genomes = df_uniq_genome.shape[0]
    logger.info(rf"Please adjust the [#$ -t] in run_dfastqc_genBank.sh to [#$ -t {number_of_genomes}]. For dummy data, adjust to [#$ -t 5].")
    logger.info("===== Script Done =====")

if __name__ == '__main__':
    # Define a function to parse command-line arguments
    def parse_args():
        parser = ArgumentParser()
        parser.add_argument(
            "-g",
            "--dfastqc_genome_directory",
            type=str,
            required=True,
            help="Path to DFAST_QC reference genomes directory",
            metavar="PATH"
        )
        args = parser.parse_args()
        return args

    args = parse_args()
    test_data_GeneBank(args.dfastqc_genome_directory)