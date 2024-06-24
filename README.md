DFAST_QC: Rapid Quality Checking and Taxonomic Identification Tool for Prokaryotic Genomes
===================
Repository contributing to the manuscript "DFAST_QC: Rapid Quality Checking and Taxonomic Identification Tool for Prokaryotic Genomes"
-------------------
Authors:
Mohamed Elmanzalawi and Yasuhiro Tanizawa


This repository contains scripts to replicate [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc) benchmarking results.

## Dependencies
- [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc). Please ensure you are using version 1.0.0 as any change in the version might yield different results or errors.
- [Pandas](https://github.com/pandas-dev/pandas) as it is needed for the final summary files.
- The scripts rely on using high-performance computing systems which in our case is [The National institute of genetics (NIG) Supercomputer](https://sc.ddbj.nig.ac.jp/en/). If another HPC was used some parameters for job details should be adjusted accordingly.  

**Under Progress
## Detailed Benchmarking steps
 
### GenBank analysis:
**1. Generate the benchmarking data.**

**Before running the script please change the DFAST_QC genome directory pathway to your machine. This is necessary since the script will collect a list of genomes present there and use them in a filtering step**
```
genome_directory = "/path/to/dfast_qc/genomes/directory"
```
For example:
```
genome_directory = "/Users/mohamed/Desktop/dfast_qc/dqc_reference/genomes"
```
The script will download all the genome assemblies from GenBank using the assembly_summary_genbank.txt file and ANI_report_prokaryotes.txt which is used in filtering. Both can be found [here](https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/) and merge them. Then filter them in the following manner:

- Retrieve all genomes that are either Bacteria or Archaea. (found in assembly_summary_genbank.txt)

- Collect only those genomes with the version status "Latest" and marked as "OK" in the taxonomy check. (found in ANI_report_prokaryotes.txt)

- Exclude genomes found in the DFAST_QC genome directory. (the script will generate the list automatically)

- Select only non-type material genomes. (found in assembly_summary_genbank.txt)

- Removing uncultured and unidentified prokaryotes. (using specific keywords like uncultured,Candidatus .. etc)

- Finally, select one random sample from every species.

```
python test_datasets_GenBank.ipynb
```
This script will also automatically download [dfast_file_downloader.py](https://github.com/nigyta/dfast_core/blob/master/scripts/dfast_file_downloader.py), which is necessary for downloading the genomes. 

Another option is that it provides a dummy data file "genebank_prok_1_per_species_dummy.tsv" containing 5 genome accessions to test the workflow. This allows you to identify and address any errors caused by format changes in the files before processing the full dataset.

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
Once you have copied the file "reference_genomes.tsv" to the same directory as the script, you can proceed to run the script.

```
python summarize_GenBank_results.py
```







