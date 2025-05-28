DFAST_QC: Quality Assessment and Taxonomic Identification Tool for Prokaryotic Genomes
===================
Repository contributing to the manuscript "DFAST_QC: Quality Assessment and Taxonomic Identification Tool for Prokaryotic Genomes"

You can read our manuscript at the following link:  
**Elmanzalawi, M., Fujisawa, T., Mori, H., Nakamura, Y., & Tanizawa, Y. (2025). DFAST_QC: Quality assessment and taxonomic identification tool for prokaryotic Genomes. BMC Bioinformatics, 26(1), 3. [![GCB](https://img.shields.io/badge/DOI-10.1101/2024.03.11.584526-21908C.svg)](https://doi.org/10.1186/s12859-024-06030-y)**

-------------------
Authors:
Mohamed Elmanzalawi and [Yasuhiro Tanizawa](https://github.com/nigyta)


This repository contains scripts to replicate [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc) benchmarking results.

**General note: in our benchmark analysis all the tools were installed in a conda environment called "dfast_qc". In each of these scripts, we activate the conda environment.**
The scripts:
- [run_dfastqc_GEM.sh](https://github.com/Mohamed-Elmanzalawi/DFAST_QC_Benchmark/blob/main/run_dfastqc_GEM.sh#L10)

- [run_dfastqc_GenBank.sh](https://github.com/Mohamed-Elmanzalawi/DFAST_QC_Benchmark/blob/main/run_dfastqc_GenBank.sh#L10)

- [run_gtdbtk_GEM.sh](https://github.com/Mohamed-Elmanzalawi/DFAST_QC_Benchmark/blob/main/run_gtdbtk_GEM.sh#L10)

- [summary_GenBank_job.sh](https://github.com/Mohamed-Elmanzalawi/DFAST_QC_Benchmark/blob/main/run_dfastqc_GenBank.sh#L10)

**So either delete the conda activation line in these scripts or create a "dfast_qc" conda environment and install all the Dependencies.**

**The conda env we used is available as yml file which can be used to create it by running the following command:**
```
conda env create -f dfast_qc.yml
```
After activating the conda env export the path to GTDB-Tk database on your machine. For example:
```
export GTDBTK_DATA_PATH=/new/path/to/gtdbtk/db
```

## Dependencies
- [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc). Please ensure you are using version 1.0.0 as any change in the version might yield different results or errors.
  
  **You can install [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) and run the following command:**
```
conda install bioconda::dfast_qc=1.0.0
```
- [Pandas v2.2.0](https://github.com/pandas-dev/pandas) for creating the final summary files.

```
conda install anaconda::pandas=2.2.0 
```
- **[Genome Taxonomy Database tool kit (GATK-TK) v2.4.0](https://github.com/Ecogenomics/GTDBTk)**. Please follow their installation procedures. 
- Some of the scripts are designed to utilize high-performance computing systems. Ours are specifically tailored for [The National Institute of Genetics (NIG) Supercomputer](https://sc.ddbj.nig.ac.jp/en/). If an alternative HPC system is employed, adjustments may be necessary for certain parameters related to job details, such as those in step 2 of the GenBank analysis and step * in the GTDB analysis.

## Detailed Benchmarking steps
 
### GenBank analysis:
**1. Generate the benchmarking data.**
```
python test_datasets_GenBank.py -g path/to/dfast_qc/genome/directory
```
**Here ```-g``` is the pathway for the DFAST_QC genome directory. This is essential as the script will compile a list of genomes from this location and utilize them during the filtering process.**

The script will download all the genome assemblies from GenBank from the assembly_summary_genbank.txt file using a modified version of [dfast_file_downloader.py](https://github.com/nigyta/dfast_core/blob/master/scripts/dfast_file_downloader.py). Also ANI_report_prokaryotes.txt will be downloaded for filtering purposes. Both are available [here](https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/). It then merges these datasets and filters them as follows:

- Retrieve all genomes that are either Bacteria or Archaea. (found in assembly_summary_genbank.txt)

- Collect only those genomes with the version status "Latest" and marked as "OK" in the taxonomy check. (found in ANI_report_prokaryotes.txt)

- Exclude genomes found in the DFAST_QC genome directory. (the script will generate the list automatically)

- Select only non-type material genomes. (found in assembly_summary_genbank.txt)

- Removing uncultured and unidentified prokaryotes. (using specific keywords like uncultured,Candidatus .. etc)

- Finally, select one random sample from every species.


This script will also automatically download [dfast_file_downloader.py](https://github.com/nigyta/dfast_core/blob/master/scripts/dfast_file_downloader.py), which is necessary for downloading the genomes. 

Alternatively, the script also provides a **dummy data file named "genebank_prok_1_per_species_dummy.tsv"** containing 5 genome accessions. This file serves as a test dataset to validate the workflow, enabling users to detect and resolve any errors caused by format changes in the files before processing the entire dataset.

**2. Submit a Job to the NIG-SC to get DFAST_QC results.**

**Don't forget to change the number of genomes in argument```[#$ -t {number_of_genomes}]``` in the job script run_dfastqc_GenBank.sh. The number is provided once you finish running test_datasets_GenBank.py.**

**Example: ```[#$ -t 9000]```**

Then You can run the script.
```
qsub run_dfastqc_GenBank.sh /home/melmanzalawi/dfast_qc genebank_test_data/genebank_prok_1_per_species_accession.tsv
```
In case you want to use the dummy data run the following command
```
qsub run_dfastqc_GenBank.sh /home/melmanzalawi/dfast_qc genebank_test_data/genebank_prok_1_per_species_accession_dummy.tsv
```
- The First argument is the path to the DFAST_QC directory. 

- The second argument is the path to the dummy data or any species accession data. If not provided the script will use the real data generated for the test data script.

**3. Combine all DFAST_QC results to get the summary file.**

**The script will also select genomes that have reference genomes only using "reference_genomes.tsv" which can be generated using [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc) by the following command:**
```
dqc_admin_tools.py dump_sqlite_db
```
After copying the file "reference_genomes.tsv" to the same directory as the script, you may proceed to execute the script.
```
python summarize_GenBank_results.py -r DQC_genebank_results/ -as genbank_test_data/assembly_summary_genbank.txt -ani genbank_test_data/ANI_report_prokaryotes.txt 
```
**```-r``` is the pathway for the DFAST_QC results directory.**

**```-as``` is the pathway for assembly_summary_genbank.txt file.**

**```-ani``` is the pathway for ANI_report_prokaryotes.txt file.**

You can also run it using the NIG-SC by running the following job:
```
qsub summary_GenBank_job.sh
```

### GEMs analysis:
Genomic catalog of Earth’s microbiomes (GEMS)

**1. Generate the benchmarking data.**
```
python test_datasets_GEM.py
```
The script will download genomes from the [genomic catalog of Earth’s microbiome](https://genome.jgi.doe.gov/portal/GEMs/GEMs.home.html) and select 10000 random samples.
Similar to the GenBank script, it performs functions such as generating dummy data.

**2. Submit a Job to the NIG-SC to get DFAST_QC results.**
```
qsub run_dfastqc_GEM.sh /home/melmanzalawi/dfast_qc gem_test_data/gem_mags_10000_ID_list.tsv
```
In case you want to use the dummy data run the following command
```
qsub run_dfastqc_GEM.sh /home/melmanzalawi/dfast_qc gem_test_data/gem_mags_5_ID_list_dummy.tsv
```
- The First argument is the path to the DFAST_QC directory.

- The second argument is the path to the dummy data or any species accession data. If not provided the script will use the real data generated for the test data script.

**3. Submit a Job to the NIG-SC to get GTDB-TK results.**
```
qsub run_gtdbtk_GEM.sh
```
In case you want to use the dummy data run the following command
```
qsub run_gtdbtk_GEM.sh dummy
```
**3. Combine all GTDB-TK results into one file.**
```
python summarize_GTDBtk_results.py
```

**4. Combine both GTDB-TK final result file and DFAST_QC to get the summary file.**
```
python summarize_GEM_results.py -r DQC_GEM_results/ -g result_GTDBtk_all.tsv
```





