import os.path
import dataclasses
from argparse import ArgumentParser
import pandas as pd
from logging import getLogger , INFO , basicConfig

logger = getLogger(__name__)
basicConfig(level=INFO)
logger.info("===== Starting the script =====") 

# Define the header for the summary results
header = ['query_accession', 'query_organism_name', 'query_species_taxid', 'DFAST_QC_organism_name', 'DFAST_QC_species_taxid', 'MASH_organism_name', 'MASH_species_taxid', 
          'DFAST_QC_ani', 'ani_threshold', 'MASH_distance', 'MASH_ANI', 'DFAST_QC_status', 'MASH_status', "Result_Consistency",'dfastqc_match', 'mash_match', 
          'status_species_taxid','dfastqc_checkm','availability_of_reference_genome']

# Define a function to summarize results
def summary_results(result_folder,assembly_summary,ani_report):
    # Initialize a dictionary to store combined results

    # Define a data class for Assembly information
    @dataclasses.dataclass
    class Assembly:
        accession: str
        organism_name: str
        species_taxid: int

    ANI_Report = pd.read_csv(ani_report, sep = "\t")

    dqc_ref_file = "reference_genomes.tsv"
    def get_species_with_ref_genome():
        S = set()
        for line in open(dqc_ref_file):
            if line.startswith("accession"):
                continue
            species_taxid = int(line.strip().split("\t")[2])
            S.add(species_taxid)
        return S

    species_with_ref_genome = get_species_with_ref_genome()
    
    def combined_dict():
        combined_dict = {}
        for key in header:
            combined_dict[key] = []
        return combined_dict
    
    combined_dict = combined_dict()
    
    logger.info("===== Reading assembly_summary file =====") 
    # Read assembly_summary file and store information in dictionaries
    A_S = {}
    with open(assembly_summary) as a:
        next(a)  # skip first line
        for line in a:
            cols = line.strip("\n").split("\t")
            accession, organism_name, species_taxid,= cols[0], cols[7], cols[6]
            asm = Assembly(accession, organism_name, species_taxid)
            A_S[accession] = asm      
    
    logger.info("===== Done =====") 
    logger.info("===== Starting processing results =====") 
    no_result_files = []
    # Traverse each directory in the root folder
    for folder_name in os.listdir(result_folder): 
        folder_path = os.path.join(result_folder, folder_name)
        mash_result = os.path.join(folder_path, "distances_ref.tab")
        dfast_qc_result = os.path.join(folder_path, "tc_result.tsv")
        checkm_file = os.path.join(folder_path, "cc_result.tsv")
        if not os.path.exists(dfast_qc_result):
            no_result_files.append(folder_name)
            continue

        dfast_no_result = False
        inconclusive_ind_species_taxid = []
        with open(dfast_qc_result) as d:
            lines = d.readlines()
            if len(lines) == 1:
                dfast_no_result = True
                inconclusive_ind_species_taxid.append('-')
                dfastqc_checkm = "-"
            else:
                first_line = lines[1].strip("\n").split("\t")
                for line in lines[1:]:
                    # Split the line by tab delimiter
                    columns = line.strip().split("\t")
                    # Check if the status is "inconclusive"
                    if columns[-1] == "inconclusive" or columns[-1] == "indistinguishable":
                        # Append the species_taxid
                        inconclusive_ind_species_taxid.append(columns[4])
                with open(checkm_file) as c:
                    next(c)
                    # Iterate over each line in the file
                    for line in c:
                        # Split the line by tab delimiter
                        cc_columns = line.strip().split("\t")
                        dfastqc_checkm = cc_columns[11]

        L = open(mash_result).readlines()
        L = [line.strip("\n").split("\t") for line in L]
        L = sorted(L, key=lambda x: float(x[2]))
        top_hit = L[0][0]
        MASH_distance = float(L[0][2])
        MASH_ANI = (1 - MASH_distance) * 100
        # Access the first element (index 0) to get "GCA_004341945.1"
        mash_accession = top_hit.split('/')[-1].replace(".fna.gz","")


        query_accession = folder_name.split('_',1)[1]
        query_organism_name = A_S[query_accession].organism_name
        query_species_taxid = A_S[query_accession].species_taxid
        if dfast_no_result:
            DFAST_QC_organism_name = DFAST_QC_species_taxid = DFAST_QC_ani = ani_threshold = DFAST_QC_status = "-"

        else:
            DFAST_QC_organism_name, DFAST_QC_species_taxid, DFAST_QC_ani, ani_threshold, DFAST_QC_status= first_line[0], first_line[4], first_line[7], first_line[10], first_line[11]
        
        MASH_organism_name = A_S[mash_accession].organism_name
        MASH_species_taxid = A_S[mash_accession].species_taxid
        MASH_DISTANCE_THRESHOLD = 0.05
        MASH_status = (MASH_distance < MASH_DISTANCE_THRESHOLD)


        dfastqc_match = "Match" if DFAST_QC_species_taxid == query_species_taxid else "Mismatch"
        mash_match = "Match" if MASH_species_taxid == query_species_taxid else "Mismatch"
        Result_Consistency = MASH_status and (DFAST_QC_status == "conclusive")

        if DFAST_QC_status == "conclusive" and dfastqc_match == "Match":
            status_species_taxid = "conclusive_match"
        elif DFAST_QC_status in ["inconclusive", "indistinguishable"] and query_species_taxid in inconclusive_ind_species_taxid :
            status_species_taxid = "inconclusive_match"
        elif DFAST_QC_status == "below_threshold" and dfastqc_match == "Match" :
            status_species_taxid = "below_threshold_Match"
        elif DFAST_QC_status == "below_threshold"  and dfastqc_match == "Mismatch" :
            status_species_taxid = "below_threshold_Mismatch"
        elif DFAST_QC_status == "-":
            status_species_taxid = "no_hit"
        else:
            status_species_taxid = "Mismatch"

        availability_of_reference_genome = "YES" if int(query_species_taxid) in species_with_ref_genome else "NO"

        for key in combined_dict.keys():
            if key in locals():
                combined_dict[key].append(locals()[key])
            else:
                print(f"Warning: Variable for key '{key}' not found in local variables")

        logger.info(f"===== processing {folder_name} Done =====")

    # Convert to the dictionaries to DataFrame
    df = pd.DataFrame(combined_dict)
    # Merge DataFrames on the common accession columns and keep only the desired column
    df = pd.merge(df, ANI_Report[['# genbank-accession','taxonomy-check-status','declared-type-ANI','best-match-species-taxid','comment','best-match-status']], left_on='query_accession', right_on='# genbank-accession', how='left')
    df = df.drop('# genbank-accession', axis=1)
    assembly_genebank = pd.read_csv(assembly_summary, sep = "\t",skiprows=[0],dtype={34: str, 35: str, 36: str})
    df = pd.merge(df, assembly_genebank[['#assembly_accession','relation_to_type_material']], left_on='query_accession', right_on='#assembly_accession', how='left')
    df = df.drop('#assembly_accession', axis=1)  

    #Filtering by only genomes that have reference genome.
    df_ref_true = df[df["availability_of_reference_genome"] == "YES"]

    # Output TSV File
    output_file = "summary_Genebank.tsv"
    output_file_ref_true = "dfast_qc_benchmark.tsv"
    # Save to TSV file
    df.to_csv(output_file, sep='\t', index=False)
    df_ref_true.to_csv(output_file_ref_true, sep='\t', index=False)
    logger.info(f"===== Processing all results done. Saving results to {output_file} =====") 
    logger.info(f"===== Saving filtered results for benchmarking to {output_file_ref_true} =====") 
    if len(no_result_files) > 0:
        logger.info(f"Files that had no DFAST_QC results are {no_result_files}")


if __name__ == '__main__':
    # Define a function to parse command-line arguments
    def parse_args():
        parser = ArgumentParser()
        parser.add_argument(
            "-r",
            "--result_folder",
            type=str,
            required=True,
            help=f"Path to reference analysis results folder",
            metavar="PATH"
        )
        parser.add_argument(
            "-as",
            "--assembly_summary",
            type=str,
            required=True,
            help=f"Path to assembly_summary file",
            metavar="PATH"
        )
        parser.add_argument(
            "-ani",
            "--ani_report",
            type=str,
            required=True,
            help=f"Path to ANI report file",
            metavar="PATH"
        )
        args = parser.parse_args()
        return args

    args = parse_args()
    summary_results(args.result_folder, args.assembly_summary, args.ani_report)

