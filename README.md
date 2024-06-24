DFAST_QC: Rapid Quality Checking and Taxonomic Identification Tool for Prokaryotic Genomes
===================
Repository contributing to the manuscript "DFAST_QC: Rapid Quality Checking and Taxonomic Identification Tool for Prokaryotic Genomes"
-------------------
Authors:
Mohamed Elmanzalawi and [Yasuhiro Tanizawa](https://github.com/nigyta)


This repository contains scripts to replicate [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc) benchmarking results.

## Dependencies
- [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc). Please ensure you are using version 1.0.0 as any change in the version might yield different results or errors.
  
  **You can install [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) and run the following command:**
```
conda install bioconda::dfast_qc=1.0.0
```
- [Pandas](https://github.com/pandas-dev/pandas) as it is needed for the final summary files.

```
conda install anaconda::pandas
```
- [Genome Taxonomy Database tool kit (GATK-TK)](https://github.com/Ecogenomics/GTDBTk). Please follow their installation procedures. 
- Some of the scripts are designed to utilize high-performance computing systems. Ours are specifically tailored for [The National institute of genetics (NIG) Supercomputer](https://sc.ddbj.nig.ac.jp/en/). If an alternative HPC system is employed, adjustments may be necessary for certain parameters related to job details, such as those in step 2 of the GenBank analysis and step * in the GTDB analysis.

**Under Progress
## Detailed Benchmarking steps
 
### GenBank analysis:
**1. Generate the benchmarking data.**

**Before running the script, please update the directory pathway for the DFAST_QC genome directory to match your local machine. This adjustment is essential as the script will compile a list of genomes from this location and utilize them during the filtering process.**
```
genome_directory = "/path/to/dfast_qc/genomes/directory"
```
For example:
```
genome_directory = "/Users/mohamed/Desktop/dfast_qc/dqc_reference/genomes"
```
Then run the script:
```
python test_datasets_GenBank.ipynb
```

The script will download all the genome assemblies from GenBank using the assembly_summary_genbank.txt file and ANI_report_prokaryotes.txt for filtering purposes. Both are available [here](https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/) It then merges these datasets and filters them as follows:

- Retrieve all genomes that are either Bacteria or Archaea. (found in assembly_summary_genbank.txt)

- Collect only those genomes with the version status "Latest" and marked as "OK" in the taxonomy check. (found in ANI_report_prokaryotes.txt)

- Exclude genomes found in the DFAST_QC genome directory. (the script will generate the list automatically)

- Select only non-type material genomes. (found in assembly_summary_genbank.txt)

- Removing uncultured and unidentified prokaryotes. (using specific keywords like uncultured,Candidatus .. etc)

- Finally, select one random sample from every species.


This script will also automatically download [dfast_file_downloader.py](https://github.com/nigyta/dfast_core/blob/master/scripts/dfast_file_downloader.py), which is necessary for downloading the genomes. 

Alternatively, the script also provides a **dummy data file named "genebank_prok_1_per_species_dummy.tsv"** containing 5 genome accessions. This file serves as a test dataset to validate the workflow, enabling users to detect and resolve any errors caused by format changes in the files before processing the entire dataset.

**2. Submit a Job to the NIG-SC.**
```
qsub run_dfastqc_GenBank.sh
```
In case you want to use the dummy data run the following command:
```
qsub summary_GenBank_job.sh -a genebank_test_data/genebank_prok_1_per_species_accession_dummy.tsv
```
Where `-a` is the path to the dummy data or any species accession data. If not provided the script will use the real data generated for the test data script.

**3. Combine all DFAST_QC results to get the summary file.**

**The script will also select genomes that have reference genomes only using "reference_genomes.tsv" which can be generated using [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc) by the following command:**
```
dqc_admin_tools.py dump_sqlite_db
```
After copying the file "reference_genomes.tsv" to the same directory as the script, you may proceed to execute the script.
```
python summarize_GenBank_results.py
```

### GTDB analysis:
**1. Generate the benchmarking data.**
```
python test_datasets_gtdb.ipynb
```
The script will download genomes from the [genomic catalog of Earth’s microbiome](https://genome.jgi.doe.gov/portal/GEMs/GEMs.home.html) and select 10000 random samples.
Similar to the GenBank script, it performs functions such as retrieving  [dfast_file_downloader.py](https://github.com/nigyta/dfast_core/blob/master/scripts/dfast_file_downloader.py) and generating dummy data.






