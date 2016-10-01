import pandas as pd
import time
folder = "C:/MDR/Data"
output_filename = ""

df = pd.read_excel(folder + 'MDR_LOADING.xlsx',sheetname="Mappings")

writer = pd.ExcelWriter(folder + output_filename)
df.to_excel(writer, sheet_name="Stats",index=False)

df = df[df["Status"].str.upper() == "Open".upper()]

if(df.empty): print "Dataframe is empty"


time.strftime('%Y-%m-%d %H:%M:%S')

object_duplicated_by_columns = ["System Name","Entity Name", "Attribute Name","Type"]
object_sort_by_columns       = ["System Name", "Entity Name", "Attribute Name", "Type"]
df.drop_duplicates(subset=object_duplicated_by_columns, keep=False, inplace=True)


df.rename(columns={"LDM INTL ID":"Transformation_Mapping_Rule","LDM Text":"Attribute_Description","LDM Object": "Target_Entity_Name_L","LDM Field":"Target_Attribute_Name_L","Source Name":"Source_Entity_Name","Element Name":"Source_Attribute_Name"}, inplace=True)


df.sort_values(by=object_sort_by_columns, inplace=True, na_position='first', ascending=[False, True, True, True])


#ignore the rows with blank Entity Name
df = df[df["LDM Object"].notnull()]


# Read CSV
output_csv_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
input_csv_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
input_filename = ""
output_filename = "ABS_EntityName_T_E_A_Correct.csv"

required_columns = ["Entity Name", "Attribute Name"]

df = pd.read_csv(input_csv_folder_path + input_filename, sep=",",usecols=required_columns)
