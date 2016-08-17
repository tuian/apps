import pandas as pd
import xlrd
import numpy as np

# Loading a CSV file
#df = pd.read_csv('../data/example.csv')

# Loading a EXLS file
# xls_file = pd.ExcelFile('./data/LDM OBJ Report.xlsx')
# df = xls_file.parse('export0')
#
# print df

xls_file = pd.ExcelFile('./data/input/LDM OBJ Report.xlsx')
df = xls_file.parse('export0')

# df.insert(1,'LDM Object New', "-")
# print df.loc[0, 'LDM Object']

for i in range(1, len(df)):
    #print df.loc[i,'LDM Object']
    if(pd.isnull(df.loc[i,'LDM Object'])):
        #print "Inside None"
        df.loc[i, 'LDM Object'] = df.loc[i-1, 'LDM Object']

df = df.dropna(subset=['Field'])
df = df.dropna(subset=['Field Type'])

print df.head(10)


df.to_csv("./data/output/LDM OBJ Report Output.csv")
