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
## Files Info
 
### GenBank analysis scripts:
-test_datasets_GenBank.ipynb: Test data preparation script. 
