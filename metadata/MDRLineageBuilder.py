import pandas as pd


inFile = "C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Mappings.csv"
outFile_path = "C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Mappings_"
def buildLineage():
    print "---Starting buildLineage()-----"
    df = pd.read_csv(inFile, sep=",")
    df.rename(columns=lambda x: x.strip().replace(" ", "_"), inplace=True)

    df["Source_System_Name"] = df["Source_System_Name"].str.strip()
    df["Source_Entity_Name"] = df["Source_Entity_Name"].str.upper()
    df["Source_Attribute_Name"] = df["Source_Attribute_Name"].str.upper()
    df["Target_Entity_Name"] = df["Target_Entity_Name"].str.upper()
    df["Target_Attribute_Name"] = df["Target_Attribute_Name"].str.upper()

    df_ux_vm   = df[df["Source_System_Name"] == 'UX Sitemap']
    df_vm_ifs  = df[df["Source_System_Name"] == 'Visual Map']
    df_ifs_xsd = df[df["Source_System_Name"] == 'IFS']
    df_xsd_ldm = df[df["Source_System_Name"] == 'ABS Dev']

    print df["Source_System_Name"].value_counts()

    print "df", len(df)
    print "df_ux_vm", len(df_ux_vm)
    print "df_vm_ifs", len(df_vm_ifs)
    print "df_ifs_xsd", len(df_ifs_xsd)
    print "df_xsd_ldm", len(df_xsd_ldm)

    df_ux_vm_ifs = pd.merge(left=df_ux_vm,right=df_vm_ifs, left_on=["Target_Entity_Name","Target_Attribute_Name"],right_on=["Source_Entity_Name","Source_Attribute_Name"],how='left')
    df_ux_vm_ifs.to_csv(outFile_path+"ux_vm_ifs_by_join.csv",sep=",",index=False)
    print "df_ux_vm_vm_ifs", len(df_ux_vm_ifs)


    df_ux_vm_ifs_xsd = pd.merge(left=df_ux_vm_ifs, right=df_ifs_xsd, left_on=["Target_Entity_Name_y", "Target_Attribute_Name_y"],
                               right_on=["Source_Entity_Name", "Source_Attribute_Name"], how='left')

    df_ux_vm_ifs_xsd.rename(columns={"Source_Entity_Name_x":"Screen_Entity_Name",
                                     "Source_Attribute_Name_x":"Screen_Attribute_Name",
                                     "Target_Entity_Name_x": "VM_Entity_Name",
                                     "Target_Attribute_Name_x": "VM_Attribute_Name",
                                     "Target_Entity_Name_y": "IFS_Entity_Name",
                                     "Target_Attribute_Name_y": "IFS_Attribute_Name",
                                     "Target_Entity_Name": "XSD_Entity_Name",
                                     "Target_Attribute_Name": "XSD_Attribute_Name"
                                     },
                            inplace=True)
    required_cols_df_ux_vm_ifs_xsd = ["Screen_Entity_Name","Screen_Attribute_Name",
                                      "VM_Entity_Name","VM_Attribute_Name",
                                      "IFS_Entity_Name","IFS_Attribute_Name",
                                      "XSD_Entity_Name","XSD_Attribute_Name",
                                      "Transformation_Mapping_rule"
                                      ]
    df_ux_vm_ifs_xsd.to_csv(outFile_path + "df_ux_vm_ifs_xsd_by_join.csv", sep=",", index=False,columns=required_cols_df_ux_vm_ifs_xsd)
    print "df_ux_vm_ifs_xsd", len(df_ux_vm_ifs_xsd)

if __name__ == "__main__":
    buildLineage()