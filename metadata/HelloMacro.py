'''
Objectives: How to merge two dataframes...or CSV files.... or tables...
Learnings:
Axis 0 row (drops a row, mean of the row)
Axis 1 column (drops a the column, mean of the column etc)

'''
import os
import pandas as pd

#def
macro_folder_path = "C:\\MDR\\Data\\Macro\\"
output_excel_filename = "Sharepoint_Harvest.xlsx"
files = os.listdir(macro_folder_path)
#print files

files_xlsm = [f for f in files if f[-4:] == 'xlsm']
#print files_xlsm
print "Total Number of Macro Files: ",len(files_xlsm)
print "Extraction in progress..."

df_screen_fields = pd.DataFrame()
df_vm_fields = pd.DataFrame()
df_ifs_fields = pd.DataFrame()
df_xsd_fields = pd.DataFrame()
df_mapping_screen_vm = pd.DataFrame()
df_mapping_vm_ifs = pd.DataFrame()
df_mapping_ifs_xsd = pd.DataFrame()



for macro_file_name in files_xlsm:

    data_screen_fields = pd.read_excel(macro_folder_path + macro_file_name, "Screen Fields")
    df_screen_fields = df_screen_fields.append(data_screen_fields)

    data_vm_fields = pd.read_excel(macro_folder_path + macro_file_name,"Visual Map Fields")
    df_vm_fields = df_vm_fields.append(data_vm_fields)

    data_ifs_fields= pd.read_excel(macro_folder_path + macro_file_name,"IFS Fields")
    df_ifs_fields = df_ifs_fields.append(data_ifs_fields)

    data_xsd_fields = pd.read_excel(macro_folder_path + macro_file_name, "XSD Fields")
    df_xsd_fields = df_xsd_fields.append(data_xsd_fields)

    data_mapping_screen_vm= pd.read_excel(macro_folder_path + macro_file_name,"Mappings_Screen_VisualMap")
    df_mapping_screen_vm = df_mapping_screen_vm.append(data_mapping_screen_vm)

    data_mapping_vm_ifs = pd.read_excel(macro_folder_path + macro_file_name,"Mapping_VisualMap_IFS")
    df_mapping_vm_ifs = df_mapping_vm_ifs.append(data_mapping_vm_ifs)

    data_mapping_ifs_xsd = pd.read_excel(macro_folder_path + macro_file_name, "Mapping_IFS_XSD")
    df_mapping_ifs_xsd = df_mapping_ifs_xsd.append(data_mapping_ifs_xsd)


screen_duplicated_by_columns = ["Entity Name","Attribute Name"]
df_screen_fields_duplicates = df_screen_fields[df_screen_fields.duplicated(subset=screen_duplicated_by_columns, keep=False)]
df_screen_fields_duplicates.sort_values(by=screen_duplicated_by_columns,inplace=True)
df_screen_fields_duplicates.to_excel(macro_folder_path+"output\\screen_fields_duplicates.xlsx",sheet_name="screen_fields_duplicates")

vm_duplicated_by_columns = ["VM Entity Name","Attribute Name"]
df_vm_fields_duplicates = df_vm_fields[df_vm_fields.duplicated(subset=vm_duplicated_by_columns, keep=False)]
df_vm_fields_duplicates.sort_values(by=vm_duplicated_by_columns,inplace=True)
df_vm_fields_duplicates.to_excel(macro_folder_path+"output\\vm_fields_duplicates.xlsx",sheet_name="vm_fields_duplicates")

ifs_duplicated_by_columns = ["IFS Entity Name","IFS Attribute Name"]
df_ifs_fields_duplicates = df_ifs_fields[df_ifs_fields.duplicated(subset=ifs_duplicated_by_columns, keep=False)]
df_ifs_fields_duplicates.sort_values(by=ifs_duplicated_by_columns,inplace=True)
df_ifs_fields_duplicates.to_excel(macro_folder_path+"output\\ifs_fields_duplicates.xlsx",sheet_name="ifs_fields_duplicates")

xsd_duplicated_by_columns = ["Entity Name","Attribute Name"]
df_xsd_fields_duplicates = df_xsd_fields[df_xsd_fields.duplicated(subset=xsd_duplicated_by_columns, keep=False)]
df_xsd_fields_duplicates.sort_values(by=xsd_duplicated_by_columns,inplace=True)
df_xsd_fields_duplicates.to_excel(macro_folder_path+"output\\xsd_fields_duplicates.xlsx",sheet_name="xsd_fields_duplicates")


m_duplicated_by_columns = ["Source Entity Name","Source Attribute Name","Target Entity Name","Target Attribute Name"]

df_mapping_screen_vm_duplicates = df_mapping_screen_vm[df_mapping_screen_vm.duplicated(subset=m_duplicated_by_columns, keep=False)]
df_mapping_screen_vm_duplicates.sort_values(by=m_duplicated_by_columns,inplace=True)
df_mapping_screen_vm_duplicates.to_excel(macro_folder_path+"output\\Mapping_UX_VM_Duplicates.xlsx",sheet_name="Mapping_UX_VM_Duplicates")

df_mapping_vm_ifs_duplicates = df_mapping_vm_ifs[df_mapping_vm_ifs.duplicated(subset=m_duplicated_by_columns, keep=False)]
df_mapping_vm_ifs_duplicates.sort_values(by=m_duplicated_by_columns,inplace=True)
df_mapping_vm_ifs_duplicates.to_excel(macro_folder_path+"output\\Mapping_VM_IFS_Duplicates.xlsx",sheet_name="Mapping_VM_IFS_Duplicates")

df_mapping_ifs_xsd_duplicates = df_mapping_ifs_xsd[df_mapping_ifs_xsd.duplicated(subset=m_duplicated_by_columns, keep=False)]
df_mapping_ifs_xsd_duplicates.sort_values(by=m_duplicated_by_columns,inplace=True)
df_mapping_ifs_xsd_duplicates.to_excel(macro_folder_path+"output\\Mapping_IFS_XSD_Duplicates.xlsx",sheet_name="Mapping_IFS_XSD_Duplicates")

writer = pd.ExcelWriter(macro_folder_path+"output\\"+output_excel_filename)

df_screen_fields.drop_duplicates(subset=screen_duplicated_by_columns, keep='first', inplace=True)
df_screen_fields.sort_values(by=screen_duplicated_by_columns,inplace=True)
df_screen_fields.to_excel(writer,sheet_name="Screen Fields")

df_vm_fields.drop_duplicates(subset=vm_duplicated_by_columns, keep='first', inplace=True)
df_vm_fields.sort_values(by=vm_duplicated_by_columns,inplace=True)
df_vm_fields.to_excel(writer,sheet_name="Visual Map Fields")

df_ifs_fields.drop_duplicates(subset=ifs_duplicated_by_columns, keep='first', inplace=True)
df_ifs_fields.sort_values(by=ifs_duplicated_by_columns,inplace=True)
df_ifs_fields.to_excel(writer,sheet_name="IFS Fields")

df_xsd_fields.drop_duplicates(subset=xsd_duplicated_by_columns, keep='first', inplace=True)
df_xsd_fields.sort_values(by=xsd_duplicated_by_columns,inplace=True)
df_xsd_fields.to_excel(writer,sheet_name="XSD Fields")

df_mapping_screen_vm.drop_duplicates(subset=m_duplicated_by_columns, keep='first', inplace=True)
df_mapping_screen_vm.sort_values(by=m_duplicated_by_columns,inplace=True)
df_mapping_screen_vm.to_excel(writer,sheet_name="Mappings_Screen_VisualMap")

df_mapping_vm_ifs.drop_duplicates(subset=m_duplicated_by_columns, keep='first', inplace=True)
df_mapping_vm_ifs.sort_values(by=m_duplicated_by_columns,inplace=True)
df_mapping_vm_ifs.to_excel(writer,sheet_name="Mapping_VisualMap_IFS")

df_mapping_ifs_xsd.drop_duplicates(subset=m_duplicated_by_columns, keep='first', inplace=True)
df_mapping_ifs_xsd.sort_values(by=m_duplicated_by_columns,inplace=True)
df_mapping_ifs_xsd.to_excel(writer,sheet_name="Mapping_IFS_XSD")

writer.save()






print "Extraction completed !!!"
print "Check Output File: ",macro_folder_path+"output\\"+output_excel_filename

''''''

print df_screen_fields.info()
print df_vm_fields.info()
print df_ifs_fields.info()
print df_xsd_fields.info()

print df_mapping_screen_vm.info()
print df_mapping_vm_ifs.info()
print df_mapping_ifs_xsd.info()


