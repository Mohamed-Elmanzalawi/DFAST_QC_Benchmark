import glob

glob_pat = "GTDBtk_GEM10000_results/*/*.summary.tsv"
result_files = sorted(glob.glob(glob_pat))
print(result_files)

import pandas as pd

df = None
for file_name in result_files:
    if df is None:
        df = pd.read_table(file_name) 
        # print(df.head())
    else:
        new_df = pd.read_table(file_name) 
        df = pd.concat([df, new_df], ignore_index=True)

print(df.shape)

df.to_csv("result_GTDBtk_all.tsv", sep="\t", header=True, index=False)
