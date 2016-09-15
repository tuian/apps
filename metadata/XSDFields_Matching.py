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

def columnValues():
    #list = ["BTFG$UI_BP.BP","BTFG$UI_BP_LIST.ALL#CUSTR"]

    csv_folder_path_Avaloq = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    csv_filename_2 = "ABS_LDM.xlsx"

    df = pd.read_excel(csv_folder_path_Avaloq + csv_filename_2, sheetname="Flat Layout")

    for i in range(0, len(df)):
        # split the value by $ delimiter to get the LDM Object and LDM Field
        if (".XSD" in str(df.loc[i, "Source Name"])):
            df.loc[i, "Source Name"] = str(df.loc[i, "Source Name"]).replace(".XSD", "")

    list = set(df["Source Name"])

    #print list
    return list

def getIFSXSDFields():

    csv_folder_path_Sharepoint = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
    # csv_filename_1 = "Objects_xsd.csv"
    csv_filename_1 = "Objects_xsd_all_phases.csv"

    csv_folder_path_Avaloq = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    output_csv_xsd_fields_ifs_documents = "XSD_Fields_IFS_Documents_Output.csv"

    print "################## XSD Fields - IFS Documents ##############################################"
    df1 = pd.read_csv(csv_folder_path_Sharepoint + csv_filename_1, sep=",")
    df1.drop("System Name",axis=1,inplace=True)
    df1.drop("Instance Name",axis=1,inplace=True)
    df1.drop("Owner",axis=1,inplace=True)
    df1.drop("Parent",axis=1,inplace=True)
    df1.drop("URL",axis=1,inplace=True)
    df1.drop("Document Name",axis=1,inplace=True)
    df1.drop("Description",axis=1,inplace=True)
    # print df1.head()
    # print df1.info()
    #print "Row Count: ",df1.count()

    # print "Type before: \n", df1["Type"].value_counts()
    df1 = df1[(df1["Type"] == "Attribute")]


    # print "Type after: \n ", df1["Type"].value_counts()
    print df1.head()
    # print df1.info()
    df1.dropna(subset=["Attribute Name"], inplace=True)
    df1.drop_duplicates(subset=["Entity Name", "Attribute Name"], keep='first', inplace=True)
    df1.to_csv(csv_folder_path_Avaloq+output_csv_xsd_fields_ifs_documents,sep=",",index=False,header=True)

    return df1

def getIFSXSDFieldsBySubset():

    csv_folder_path_Sharepoint = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
    # csv_filename_1 = "Objects_xsd.csv"
    csv_filename_1 = "Objects_xsd_all_phases.csv"

    csv_folder_path_Avaloq = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    output_csv_xsd_fields_ifs_documents = "XSD_Fields_IFS_Documents_Output.csv"

    print "################## XSD Fields - IFS Documents ##############################################"
    df1 = pd.read_csv(csv_folder_path_Sharepoint + csv_filename_1, sep=",")
    df1.drop("System Name",axis=1,inplace=True)
    df1.drop("Instance Name",axis=1,inplace=True)
    df1.drop("Owner",axis=1,inplace=True)
    df1.drop("Parent",axis=1,inplace=True)
    df1.drop("URL",axis=1,inplace=True)
    df1.drop("Document Name",axis=1,inplace=True)
    df1.drop("Description",axis=1,inplace=True)
    # print df1.head()
    # print df1.info()
    #print "Row Count: ",df1.count()

    # print "Type before: \n", df1["Type"].value_counts()
    df1 = df1[(df1["Type"] == "Attribute")]

    sub_list = columnValues()

    df1 = df1[(df1["Entity Name"].isin(sub_list))]

    # print "Type after: \n ", df1["Type"].value_counts()
    print df1.head()
    # print df1.info()
    df1.dropna(subset=["Attribute Name"], inplace=True)
    df1.drop_duplicates(subset=["Entity Name","Attribute Name"],keep='first',inplace=True)
    df1.to_csv(csv_folder_path_Avaloq+output_csv_xsd_fields_ifs_documents,sep=",",index=False,header=True)

    return df1

def getAvaloqXSDFields_RawFile():

    csv_folder_path_Avaloq = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    csv_filename_2 = "ABS_LDM.xlsx"
    output_csv_xsd_fields_Avaloq_INF_report = "XSD_Fields_Avaloq_Interface_Report_Output.csv"
    print "################## XSD Fields - Avaloq Interface Report Raw File##############################################"
    df2 = pd.read_excel(csv_folder_path_Avaloq + csv_filename_2, sheetname="Flat Layout")
    print df2.head()
    # df2.drop(df2.columns[["Owner","Parent"]], axis=1, inplace=True)
    df2.drop("LDM Field", axis=1, inplace=True)
    df2.drop("LDM Object", axis=1, inplace=True)
    df2.drop("LDM Text", axis=1, inplace=True)
    df2.drop("LDM Object ID", axis=1, inplace=True)
    df2.drop("LDM Field ID", axis=1, inplace=True)
    df2.drop("LDM INTL ID", axis=1, inplace=True)
    # df2.drop("Owner",axis=1,inplace=True)
    # df2.drop("Parent",axis=1,inplace=True)

    for i in range(0, len(df2)):
        # split the value by $ delimiter to get the LDM Object and LDM Field
        if (".XSD" in str(df2.loc[i, "Source Name"])):
            df2.loc[i, "Source Name"] = str(df2.loc[i, "Source Name"]).replace(".XSD", "")

    df2.rename(columns={"Source Name": "Entity Name", "Element Name": "Attribute Name"}, inplace=True)
    #df[['a', 'b']] = df[['a', 'b']].fillna(value=0)
    #df2[["Attribute Name"]] = df2[["Attribute Name"]].fillna(value='-',inplace=True)
    #df2 = df2[~df2["Attribute Name"].isnull()]
    #df2.dropna(subset=["Attribute Name"],inplace=True)
    print df2.head()
    # print df2.info()
    df2.to_csv(csv_folder_path_Avaloq + output_csv_xsd_fields_Avaloq_INF_report, sep=",", index=False, header=True)

    return df2

def getAvaloqXSDFields_ProcessedFile():

    csv_folder_path_Avaloq = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    csv_filename_2 = "LDM_INTF_Report_Output.csv"
    output_csv_xsd_fields_Avaloq_INF_report = "XSD_Fields_Avaloq_Interface_Report_Output.csv"

    print "################## XSD Fields - Avaloq Interface Report ##############################################"

    df2 = pd.read_csv(csv_folder_path_Avaloq + csv_filename_2, sep=",")
    # df2.drop(df2.columns[["Owner","Parent"]], axis=1, inplace=True)
    df2.drop("Source_System_Name", axis=1, inplace=True)
    df2.drop("Source_Instance_Name", axis=1, inplace=True)
    df2.drop("Attribute_Description", axis=1, inplace=True)
    df2.drop("Business_Rule", axis=1, inplace=True)
    df2.drop("Comments", axis=1, inplace=True)
    # df2.drop("Owner",axis=1,inplace=True)
    # df2.drop("Parent",axis=1,inplace=True)



    for i in range(0, len(df2)):
        # split the value by $ delimiter to get the LDM Object and LDM Field
        if (".XSD" in str(df2.loc[i, "Source_Entity_Name"])):
            df2.loc[i, "Source_Entity_Name"] = str(df2.loc[i, "Source_Entity_Name"]).replace(".XSD", "")


    # print df2.info()
    df2.rename(columns={"Source_Entity_Name":"Entity Name","Source_Attribute_Name": "Attribute Name"}, inplace=True)
    print df2.head()
    df2.to_csv(csv_folder_path_Avaloq + output_csv_xsd_fields_Avaloq_INF_report, sep=",", index=False, header=True)

    return df2

def mergeXSDFields(join_type):

    output_csv_filename_inner_join = "XSD_Match_Quality_Report_Inner_Join.csv"

    prefix_output_csv_filename = "XSD_Match_Quality_Report_"
    suffix_output_csv_filename = "_Join.csv"
    output_file_name = prefix_output_csv_filename +join_type+suffix_output_csv_filename

    join_key = ""
    join_key_left = "Attribute Name"
    join_key_right = "Element Name"

    #df1 = getIFSXSDFields()
    df1 = getIFSXSDFieldsBySubset()

    #df2 = getAvaloqXSDFields_ProcessedFile()
    df2 = getAvaloqXSDFields_RawFile()

    csv_folder_path_Avaloq = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    print "################## INNER JOIN ##############################################"
    #merged_df = pd.merge(left=df1,right=df2, left_on=join_key_left, right_on=join_key_right,how='inner')
    #merged_df = pd.merge(left=df1,right=df2,  on="Attribute Name",copy=False)
    merged_df = pd.merge(left=df1,right=df2, on=["Entity Name","Attribute Name"],how=join_type)
    merged_df.sort_values(by=["Entity Name","Attribute Name"],inplace=True)
    #merged_df = pd.merge(left=df1,right=df2,  left_on=["Entity Name","Attribute Name"],right_on=["Source Name","Element Name"],how='inner')
    #merged_df = pd.merge(left=df1,right=df2, on=['Internal ID','Entity Name'],copy=False)
    merged_df = merged_df.fillna('-')
    print merged_df.head()
    print merged_df.info()

    #requiredColumns = ["Element Name",""]
    merged_df.to_csv(csv_folder_path_Avaloq+output_file_name,sep=",",index=False,header=True)

    print "Count:",len(merged_df.drop_duplicates(subset=["Entity Name","Attribute Name"],keep='first'))
    print "IFS - AVALOQ REPORT - XSD MATCH - STATISTICS"
    print "IFS XSDs = {} and XSD Fields = {} (Phase 1 and Phase 2)".format(len(set(df1["Entity Name"])),len(df1))
    print "Avaloq XSDs = {} and XSD Fields = {}".format(len(set(df2["Entity Name"])),len(df2))
    print "Matching XSD Fields: Count = {}, Percentage (Match/Total) = {}%".format(len(merged_df),round( (len(merged_df) / (( len(df1).__float__() ))*100),2) )
    # print "IFS XSDs", len(set(df1["Entity Name"]))
    # print "Avaloq XSDs", len(set(df2["Entity Name"]))


#mergeXSDFields('left')
#columnValues()

csv_folder_path_Avaloq = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
input_filename = "ABS_LDM.xlsx"
output_filename = "Column_Values.xlsx"

def getSeries(input_filename,input_sheet_name,column_name,output_filename):

    df = pd.read_excel(input_filename, sheetname=input_sheet_name)

    # for i in range(0, len(df)):
    #     # split the value by $ delimiter to get the LDM Object and LDM Field
    #     if (".XSD" in str(df.loc[i, "Source Name"])):
    #         df.loc[i, "Source Name"] = str(df.loc[i, "Source Name"]).replace(".XSD", "")

    column_values = set(df[column_name])
    df.to_excel(output_filename)
    print list(column_values)

    return list(column_values)



getSeries(csv_folder_path_Avaloq+input_filename,"Flat Layout","Source Name",csv_folder_path_Avaloq+output_filename)

