import os.path
from argparse import ArgumentParser
import pandas as pd
from logging import getLogger , INFO , basicConfig

logger = getLogger(__name__)
basicConfig(level=INFO)
logger.info("===== Starting the script =====") 

# Define the header for the summary results
header = ['query_accession','DFAST_QC_accession', 'DFAST_QC_gtdb_species', 'MASH_accession','DFAST_QC_ani', 'ani_circumscription_radius', 
          'MASH_distance', 'MASH_ANI', 'DFAST_QC_status', 'MASH_status', "Result_Consistency",'dfastqc_match', 'mash_match','dfastqc_vs_mash_accession' ]

# Define a function to summarize results
def summary_results(result_folder,GTDB_TK_result):
    # Initialize a dictionary to store combined results
    def combined_dict():
        combined_dict = {}
        for key in header:
            combined_dict[key] = []
        return combined_dict
    
    combined_dict = combined_dict()
    
    # Traverse each directory in the root folder
    for folder_name in os.listdir(result_folder): 
        folder_path = os.path.join(result_folder, folder_name)
        mash_gtdb = os.path.join(folder_path, "distances_gtdb.tab")
        dfast_qc_gtdb = os.path.join(folder_path, "result_gtdb.tsv")

        dfast_no_result = False
        with open(dfast_qc_gtdb) as d:
            lines = d.readlines()
            if len(lines) == 1:
                dfast_no_result = True
            else:
                first_line = lines[1].strip("\n").split("\t")

        L = open(mash_gtdb).readlines()
        L = [line.strip("\n").split("\t") for line in L]
        L = sorted(L, key=lambda x: float(x[2]))
        top_hit = L[0][0]
        MASH_distance = float(L[0][2])
        MASH_ANI = (1 - MASH_distance) * 100
        # Access the first element (index 0) to get for example "GCA_004341945.1"
        MASH_accession = top_hit.split('/')[-1].replace("_genomic.fna.gz","")


        query_accession = folder_name.split('_',1)[1]

        if dfast_no_result:
            DFAST_QC_accession, DFAST_QC_gtdb_species, DFAST_QC_ani, ani_circumscription_radius, DFAST_QC_status= "-", "-", "-", "-", "-"

        else:
            DFAST_QC_accession, DFAST_QC_gtdb_species, DFAST_QC_ani, ani_circumscription_radius, DFAST_QC_status= first_line[0], first_line[1], first_line[2], first_line[6], first_line[12]
        
        MASH_DISTANCE_THRESHOLD = 0.05
        MASH_status = (MASH_distance < MASH_DISTANCE_THRESHOLD)


        dfastqc_match = "Match" if DFAST_QC_accession == query_accession else "Mismatch"
        mash_match = "Match" if MASH_accession == query_accession else "Mismatch"
        Result_Consistency = MASH_status and (DFAST_QC_status == "conclusive")

        dfastqc_vs_mash_accession = "Identical" if MASH_accession == DFAST_QC_accession else "Different"

        # Append results to the dictionary
        for key in combined_dict.keys():
            if key in locals():
                combined_dict[key].append(locals()[key])
            else:
                print(f"Warning: Variable for key '{key}' not found in local variables")

        logger.info(f"===== processing {folder_name} Done =====")
        
    # Convert to Pandas DataFrame
    df = pd.DataFrame(combined_dict)
    # Temporary result file for dfast_qc incase of error in merging due to formate change.
    df.to_csv('tem_result.tsv', sep='\t', index=False)
    
    # Merge DataFrames on the common accession columns and keep only the desired column
    GTDB_TK_result_file = pd.read_csv(GTDB_TK_result, sep = "\t")
    results_merged = pd.merge(df, GTDB_TK_result_file[['user_genome','closest_genome_reference','classification','closest_genome_ani']], 
                              left_on='query_accession', 
                              right_on='user_genome', 
                              how='left')
    
    results_merged.to_csv('tem_result.tsv', sep='\t', index=False)
    results_merged = results_merged.drop('user_genome', axis=1)
    results_merged = results_merged.rename(columns={'closest_genome_ani':'GTDB_tk_ani'})

    # Checking whether if DFAST_QC or GTBD-TK had a result or not.
    results_merged["DFAST_QC_assign"] = results_merged["DFAST_QC_accession"].apply(lambda x: "assigned" if x != "-" else "unassigned")
    results_merged["GTDB_tk_assign"] = results_merged["closest_genome_reference"].apply(lambda x: "assigned" if x != "nan" else "unassigned")


    # Output TSV File
    output_file = "summary_GEM.tsv"
    # Save to TSV file
    results_merged.to_csv(output_file, sep='\t', index=False)
    logger.info(f"===== Processing results done. Saving results to {output_file} =====") 
    os.remove('tem_result.tsv')

if __name__ == '__main__':
    # Define a function to parse command-line arguments
    def parse_args():
        parser = ArgumentParser()
        parser.add_argument(
            "-r",
            "--dfastqc_result_folder",
            type=str,
            required=True,
            help=f"Path to reference analysis results folder",
            metavar="PATH"
        )
        parser.add_argument(
            "-g",
            "--gtdb_result",
            type=str,
            required=True,
            help=f"Path to GTDB result file",
            metavar="PATH"
        )
        args = parser.parse_args()
        return args

    args = parse_args()
    summary_results(args.dfastqc_result_folder, args.gtdb_result)

