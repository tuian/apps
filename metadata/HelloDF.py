import pandas as pd

csv_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
csv_filename_1 = "Staff.csv"
csv_filename_2 = "Department.csv"
output_csv_filename = "Joined.csv"

df1 = pd.read_csv(csv_folder_path + csv_filename_1, sep=",")
df2 = pd.read_csv(csv_folder_path + csv_filename_2, sep=",")

print "################## Staff Table ##############################################"
print df1.head()
print "################## Department Table ##############################################"
print df2.head()

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

merged_inner.to_csv(csv_folder_path+output_csv_filename,sep=",",index=False,header=True)


#df.rename(columns={"LDM Object": "Entity Name"}, inplace=True)