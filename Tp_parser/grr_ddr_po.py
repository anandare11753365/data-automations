

import pandas as pd

df = pd.read_csv('I:/engineering/dev/team_userver_analog/kquah3/AQUA_LATEST/FCS_DATA_ANALYSIS_186336.csv', header=0, sep=',', quotechar='"')


# print(df.columns)

# print(df['TEST_NAME'].drop_duplicates().to_csv("grr_ddr_data.csv"))


df[(df['TEST_NAME'].str.contains("_VNOM_")) &\
   (df['TEST_NAME'].str.contains("_5600_")) &\
   (df['TEST_NAME'].str.contains("_HIGHST_")) |\
   (df['TEST_NAME'].str.contains("_HIGHREC1ST_")) &\
   (df['TEST_NAME'].str.contains("_DDRD1_")) &\
   (df['TEST_NAME'].str.contains("_HWTRAINCTL0"))
    ].to_csv("grr_ddr_data3.csv")


# df[df['TEST_NAME'].str.contains("_DATA_", na=False)].to_csv("grr_ddr_data2.csv")