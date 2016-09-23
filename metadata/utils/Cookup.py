import pandas as pd

folder = "C:/MDR/Data"

df = pd.read_excel(folder + 'MDR_LOADING.xlsx',sheetname="Mappings")
df = df[df["Status"].str.upper() == "Open".upper()]
