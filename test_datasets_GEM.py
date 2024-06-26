# Description: GEMs  Dataset generation script for evaluation of Taxonomy check. 
import pandas as pd
import os
import subprocess
from logging import getLogger, INFO, basicConfig

# Define the logger 
logger = getLogger()
basicConfig(level=INFO,format="%(asctime)s-%(levelname)s- %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

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

logger.info("===== Starting the script =====")

# Define the main directory and genbank_test_data directory
main_dir = os.getcwd()
gem_test_data = os.path.join(main_dir, "gem_test_data")

# Create the directory if it doesn't exist
logger.info(f"Creating the directory GEM analysis.")
os.makedirs(gem_test_data, exist_ok=True)
logger.info("Done")

gem_meta_data = ["curl","-o","gem_test_data/genome_metadata.tsv","-L","https://portal.nersc.gov/GEM/genomes/genome_metadata.tsv"]
logger.info("Downloading GEM's genome_metadata.tsv file")
run_command(gem_meta_data)

# Read the genome_metadata.tsv file
logger.info("Reading the genome_metadata.tsv file")
gem_metadata_file="gem_test_data/genome_metadata.tsv"
df = pd.read_table(gem_metadata_file)
logger.info("Done")

# Selecting 10000 random samples
logger.info("Selecting 10000 random samples")
df10000 = df.sample(n=10000)
df10000 = df10000.reset_index()
del df10000["index"]
df10000["sub_dir"] = df10000.index // 1000
logger.info("Done")

# Saving the 10000 random samples file.
logger.info("Saving the data and creating a dummy data for testing.")
df10000.to_csv("gem_test_data/gem_mags_10000.tsv", header=True, index=False, sep="\t")
df10000.to_csv("gem_test_data/gem_mags_10000_ID_list.tsv", columns=["genome_id", "sub_dir"], header=False, index=False, sep="\t")
# Dummy data for testing
df10000_dummy = df10000.head(5)
df10000.to_csv("gem_test_data/gem_mags_5_dummy.tsv", header=True, index=False, sep="\t")
df10000_dummy.to_csv("gem_test_data/gem_mags_5_ID_list_dummy.tsv", columns=["genome_id", "sub_dir"], header=False, index=False, sep="\t")
logger.info("Done")

# Number of genomes to be adjusted in the HPC job file.
number_of_genomes = df10000.shape[0]
logger.info(rf"Please adjust the [#$ -t] in run_dfastqc_GEM.sh to [#$ -t {number_of_genomes}]. For dummy data, adjust to [#$ -t 5].")
logger.info("===== Script Done =====")
