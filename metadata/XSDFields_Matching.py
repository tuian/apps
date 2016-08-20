'''
Problem Statement:
Find the match between -
"XSD Fields harvested from IFS Documents"
and
"XSD Fields in the Avaloq Interface Report"

Left side = XSD Fields from IFS Document
Right side = XSD Fields from Avaloq Interface Report
Join by Attribute Name

Additional validation:
Clean the XSD Fields from IFS Documents before comparison
'''

import pandas as pd

csv_folder_path_Sharepoint = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
#csv_filename_1 = "Objects_xsd.csv"
csv_filename_1 = "Objects_xsd_all_phases.csv"
csv_folder_path_Avaloq     = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
csv_filename_2 = "LDM_INTF_Report_Output.csv"

output_csv_filename_inner_join = "XSD_Match_Quality_Report_Inner_Join.csv"
output_csv_xsd_fields_ifs_documents = "XSD_Fields_IFS_Documents_Output.csv"
output_csv_xsd_fields_Avaloq_INF_report = "XSD_Fields_Avaloq_Interface_Report_Output.csv"

join_key =""
join_key_left  = "Attribute Name"
join_key_right = "Element Name"

df1 = pd.read_csv(csv_folder_path_Sharepoint + csv_filename_1, sep=",")
df2 = pd.read_csv(csv_folder_path_Avaloq + csv_filename_2, sep=",")


print "################## XSD Fields - IFS Documents ##############################################"
df1.drop("System Name",axis=1,inplace=True)
df1.drop("Instance Name",axis=1,inplace=True)
df1.drop("Owner",axis=1,inplace=True)
df1.drop("Parent",axis=1,inplace=True)
# print df1.head()
# print df1.info()
#print "Row Count: ",df1.count()

# print "Type before: \n", df1["Type"].value_counts()
df1 = df1[(df1["Type"] == "Attribute")]


# print "Type after: \n ", df1["Type"].value_counts()
print df1.head()
# print df1.info()

df1.to_csv(csv_folder_path_Avaloq+output_csv_xsd_fields_ifs_documents,sep=",",index=False,header=True)

print "################## XSD Fields - Avaloq Interface Report ##############################################"
#df2.drop(df2.columns[["Owner","Parent"]], axis=1, inplace=True)
df2.drop("System Name",axis=1,inplace=True)
df2.drop("Instance Name",axis=1,inplace=True)
df2.drop("Owner",axis=1,inplace=True)
df2.drop("Parent",axis=1,inplace=True)

df2.rename(columns={"Entity Name":"LDM Object","Element Name": "Attribute Name"}, inplace=True)
df2.rename(columns={"Source Name":"Entity Name","Element Name": "Attribute Name"}, inplace=True)

for i in range(0, len(df2)):
    # split the value by $ delimiter to get the LDM Object and LDM Field
    if (".XSD" in str(df2.loc[i, "Entity Name"])):
        df2.loc[i, "Entity Name"] = str(df2.loc[i, "Entity Name"]).replace(".XSD", "")



print df2.head()
# print df2.info()
df2.to_csv(csv_folder_path_Avaloq+output_csv_xsd_fields_Avaloq_INF_report,sep=",",index=False,header=True)

print "################## INNER JOIN ##############################################"
#merged_df = pd.merge(left=df1,right=df2, left_on=join_key_left, right_on=join_key_right,how='inner')
#merged_df = pd.merge(left=df1,right=df2,  on="Attribute Name",copy=False)
merged_df = pd.merge(left=df1,right=df2,  on=["Entity Name","Attribute Name"],how='left')
#merged_df = pd.merge(left=df1,right=df2,  left_on=["Entity Name","Attribute Name"],right_on=["Source Name","Element Name"],how='inner')
#merged_df = pd.merge(left=df1,right=df2, on=['Internal ID','Entity Name'],copy=False)
merged_df = merged_df.fillna('-')
# print merged_df.head()
# print merged_df.info()

#requiredColumns = ["Element Name",""]
merged_df.to_csv(csv_folder_path_Avaloq+output_csv_filename_inner_join,sep=",",index=False,header=True)

