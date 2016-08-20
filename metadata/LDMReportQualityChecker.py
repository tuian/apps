import pandas as pd

csv_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
csv_filename_1 = "LDM_INTF_Report_Output.csv"
csv_filename_2 = "LDM_OBJ_REPORT_Output.csv"
output_csv_filename_inner = "LDM_Data_Quality_Report_Inner.csv"
output_csv_filename_left = "LDM_Data_Quality_Report_Left.csv"

join_key ="Internal ID"
df1 = pd.read_csv(csv_folder_path + csv_filename_1, sep=",")
df2 = pd.read_csv(csv_folder_path + csv_filename_2, sep=",")

print "################## Interface Table ##############################################"
df1.drop(df1.columns[[0,1,2,3]], axis=1, inplace=True)

print df1.head()
print df1.info()
print "################## Object Table ##############################################"
#df2.drop(df2.columns[["Owner","Parent"]], axis=1, inplace=True)
df2.drop("System Name",axis=1,inplace=True)
df2.drop("Instance Name",axis=1,inplace=True)
df2.drop("Owner",axis=1,inplace=True)
df2.drop("Parent",axis=1,inplace=True)
print df2.head()
print df2.info()

print "################## INNER JOIN ##############################################"
merged_df = pd.merge(left=df1,right=df2, left_on='Internal ID', right_on='Internal ID',how='inner')
#merged_df = pd.merge(left=df1,right=df2, on=['Internal ID','Entity Name'],copy=False)
merged_df = merged_df.fillna('-')
print merged_df.head()
print merged_df.info()


displayColumns = ["Element Name",""]
merged_df.to_csv(csv_folder_path+output_csv_filename_inner,sep=",",index=False,header=True)

'''
print "################## LEFT JOIN ##############################################"
merged_df = pd.merge(left=df1,right=df2, left_on='Internal ID', right_on='Internal ID',how='left',sort=True)
merged_df = merged_df.fillna('-')
print merged_df.head()
print merged_df.info()

merged_df.to_csv(csv_folder_path+output_csv_filename_left,sep=",",index=False,header=True)

'''