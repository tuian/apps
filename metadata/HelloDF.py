import pandas as pd

csv_folder_path = "C:\\MDR\\Data\Labs\\"
csv_filename_1 = "Staff.csv"
csv_filename_2 = "Department.csv"
output_csv_filename = "Staff_Department_Join_Output_"

df1 = pd.read_csv(csv_folder_path + csv_filename_1, sep=",")
df2 = pd.read_csv(csv_folder_path + csv_filename_2, sep=",")

print "################## Staff Table ##############################################"
print df1.head()
df1["Staff Name"].value_counts()



print "################## Department Table ##############################################"
print df2.head()

def joinTables(left_df,right_df,join_left_columns_on,join_right_columns_on,join_how):
    print "################## {} JOIN ##############################################".format(join_how)
    merged = pd.merge(left=left_df, right=right_df, left_on=join_left_columns_on, right_on=join_right_columns_on, how=join_how,sort=True)
    merged = merged.fillna('-')
    print merged
    merged.to_csv(csv_folder_path + output_csv_filename +join_how+".csv", sep=",", index=False, header=True)

print "################## LEFT JOIN ##############################################"
merged_inner = pd.merge(left=df1,right=df2, left_on='Department ID', right_on='Department ID',how='left',sort=True)
merged_inner = merged_inner.fillna('-')
print merged_inner.head()

print "################## RIGHT JOIN ##############################################"
merged_inner = pd.merge(left=df1,right=df2, left_on='Department ID', right_on='Department ID',how='right',sort=True)
merged_inner = merged_inner.fillna('-')
print merged_inner.head()

print "################## INNER JOIN ##############################################"
merged_inner = pd.merge(left=df1,right=df2, left_on='Department ID', right_on='Department ID',how='inner',sort=True)
merged_inner = merged_inner.fillna('-')
print merged_inner.head()



print "################## OUTER JOIN ##############################################"
merged_inner = pd.merge(left=df1,right=df2, left_on='Department ID', right_on='Department ID',how='outer',sort=True)
merged_inner = merged_inner.fillna('-')
# merged_inner["Staff ID"] = merged_inner["Staff ID"].fillna('-')
# merged_inner["Staff Name"] = merged_inner["Staff Name"].fillna('-')
print merged_inner.head()

''''''

left_columns  = ["Department ID"]
right_columns = ["Department ID"]

joinTables(df1,df2,left_columns,right_columns,"inner")
joinTables(df1,df2,left_columns,right_columns,"left")
joinTables(df1,df2,left_columns,right_columns,"right")
joinTables(df1,df2,left_columns,right_columns,"outer")


#df.rename(columns={"LDM Object": "Entity Name"}, inplace=True)