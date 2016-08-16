import pandas as pd
import xlrd

# Loading a CSV file
#df = pd.read_csv('../data/example.csv')

# Loading a EXLS file
# xls_file = pd.ExcelFile('./data/LDM OBJ Report.xlsx')
# df = xls_file.parse('export0')
#
# print df

xls_file = pd.ExcelFile('./data/LDM OBJ Report.xlsx')
df = xls_file.parse('export0')

print df.head(20)
