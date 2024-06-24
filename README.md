DFAST_QC: Rapid Quality Checking and Taxonomic Identification Tool for Prokaryotic Genomes
===================
Repository contributing to a manuscript "DFAST_QC: Rapid Quality Checking and Taxonomic Identification Tool for Prokaryotic Genomes"
-------------------
Authors:
Mohamed Elmanzalawi and Yasuhiro Tanizawa


This repository contains scripts to replicate [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc) benchmarking results.

## Dependencies
- [DFAST_QC v1.0.0](https://github.com/nigyta/dfast_qc). Please ensure you are using version 1.0.0 as any change in the version might yield different results or errors.
- [Pandas](https://github.com/pandas-dev/pandas) as it is needed for the final Excel files.
- The scripts rely on using high-performance computing systems which in our case is [The National institute of genetics (NIG) Supercomputer](https://sc.ddbj.nig.ac.jp/en/). If another HPC was used some parameters for job details should be adjusted accordingly.  

Under Progress
## Benchmarking steps
 
### GenBank analysis:
1. Generate the test data using test_datasets_GenBank.ipynb script.
```
python test_datasets_GenBank.ipynb
```
This script will automatically download [dfast_file_downloader.py](https://github.com/nigyta/dfast_core/blob/master/scripts/dfast_file_downloader.py), which is necessary for downloading the genomes. Additionally, it provides a dummy data file "genebank_prok_1_per_species_dummy.tsv" containing 5 genome accessions to test the workflow. This allows you to identify and address any errors caused by format changes in the files before processing the full dataset.

2. Submit a Job to the NIG-SC using run_dfastqc_GenBank.sh.
```
qsub run_dfastqc_GenBank.sh
```
In case you want to use the dummy data run the following command:
```
qsub summary_GenBank_job.sh -a genebank_test_data/genebank_prok_1_per_species_accession_dummy.tsv
```
Where `-a` is the path to the dummy data or any species accession data. If not provided the script will use the real data generated for the test data script.

3. 








