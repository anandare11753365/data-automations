
import pandas as pd

df = pd.read_csv("C:/Users/anandare/source/repos/data-automations/data-automations/WLW_DDR/PPV_HVM_GENERIC_from_ituff_CLEAN_Unit208_SINGLEINIT.txt_processed.csv")
df.fillna(method='ffill',inplace=True)
df.fillna(method='bfill',inplace=True)

df.drop_duplicates(inplace=True)

df.to_csv("PPV_HVM_GENERIC_from_ituff_CLEAN_Unit208_SINGLEINIT_pp.csv",index=False)