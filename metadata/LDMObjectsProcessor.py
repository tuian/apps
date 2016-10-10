import pandas as pd
import numpy as np
from mdr_util import *
from MetadataExtractor import getObjects,getMapping_XSD_LDM,list_name_mapping_xsd_ldm,GP_PHASE_NO,list_name_xsd_fields_abs,list_name_ldm_fields

# Loading a CSV file
#df = pd.read_csv('../data/example.csv')

# Loading a EXLS file
# xls_file = pd.ExcelFile('./data/LDM OBJ Report.xlsx')
# df = xls_file.parse('export0')
#
# print df

GV_Latest_LDM_Report_Filename = "LDM_Flat_Report_8_06_10_2016"
#pre-conditions
#Old Name to Old Interface Name
#Sheet Name to "Flat_Report"
#File Name in the report.xlsx and in the python GV variable

def generateLDMObjectReport():
    #Analysis:
    #LDM Objects are straight forward. Just extract the full contents from the report without much manipulation.
    # the column "Internal ID" is the important column that uniquely identifies the rows (pretty much)

    input_excel_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Input\\"
    input_excel_filename = "LDM_OBJ_REPORT.xlsx"

    output_csv_filename_all = "LDM_OBJ_REPORT_Output_All.csv"
    output_csv_filename_sharepoint = "LDM_OBJ_REPORT_Output_Sharepoint.csv"
    output_csv_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"

    print "\n######################################   LDM Object Report  ################################################\n"
    print "Input Excel sheet Folder Name should be '{}' and File Name should be '{}' .\n".format(input_excel_folder_path, input_excel_filename)
    print "Please ensure you have deleted the first column from the Avaloq Report exported as excel sheet.\n"
    print "Confirm the input excel file, Folder Name , File Name and if you have deleted the first column ? [Yes/No]:"

    # answer = raw_input()
    answer = "Yes"

    if(answer == 'Yes'):

        if (checkFileName(input_excel_folder_path + input_excel_filename)):
            print "\n Excel File '{}' located".format(input_excel_filename)
            print "\n Generating CSV file, please wait.....\n"

            createFolderPath(input_excel_folder_path)
            createFolderPath(output_csv_folder_path)

            df = pd.read_excel(input_excel_folder_path+input_excel_filename,sheetname="export0",index_col=None)
            #print df.head()

            #xls_file = pd.ExcelFile('./data/input/raw/LDM_OBJ_REPORT.xlsx')
            #df = xls_file.parse('export0',index_col="Field")

            #df.insert(1,'LDM Object New', "-")

            #print df.loc[0, 'LDM Object']



            # insert Metadata related columns columns
            df.insert(0, "System Name", "ABS")
            df.insert(1, "Instance Name", "LDM")
            # LDM Object , Field
            df.insert(4, "Owner", "")
            df.insert(5, "Parent", "")
            df.insert(6, "Type", "Attribute")
            df.insert(7, "MDR Phase", "Phase 2")
            #df.insert(6, "Type", df["Field Type Details"])
            df.insert(8, "Description", df["Field Description"])

            # insert two new columns for LDM Object and LDM Field. Copy the value of Internal ID into these two columns
            df.insert(11,"Internal ID LDM Object",df["Internal ID"])
            df.insert(12,"Internal ID LDM Field" ,df["Internal ID"])

            ''' '''
            # Go through each row and make corrections to cell values
            for i in range(0, len(df)):
                #print df.loc[i,'LDM Object']

                #split the value by $ delimiter to get the LDM Object and LDM Field
                if ('$' in str(df.loc[i,"Internal ID"])):
                    list_of_values = df.loc[i,"Internal ID"].split("$")
                    df.loc[i,"Internal ID LDM Object"]  = list_of_values[0]
                    df.loc[i,"Internal ID LDM Field"]  = list_of_values[1]

                else:
                    #df.loc[i, "Internal ID LDM Object"] = df.loc[i,"Internal ID"]
                    df.loc[i, "Internal ID LDM Object"] = ""
                    df.loc[i, "Internal ID LDM Field"] = ""

                if(pd.isnull(df.loc[i,'LDM Object'])):
                    #print "Inside None"
                    df.loc[i, 'LDM Object'] = df.loc[i-1, 'LDM Object']

                # if Field is blank , it is mostly an Object. So copy the Object Name to the Field Name
                if (pd.isnull(df.loc[i, 'Field'])):
                    df.loc[i, 'Field'] = df.loc[i, 'LDM Object']
                    df.loc[i, 'Type']  = "Object"

                # if Field type is blank , it is mostly an Object. So fill "Object"
                if (pd.isnull(df.loc[i, 'Field Type'])): df.loc[i, 'Field Type'] = "Object"

                if(pd.isnull(df.loc[i,'Description'])):
                    df.loc[i,"Description"]  = "(ABS Field Type " + str(df.loc[i,"Field Type"]) + ")"
                else:
                    df.loc[i, "Description"] = str(df.loc[i, "Description"]).replace(",","") + " / (ABS Field Type " + str(df.loc[i, "Field Type"]) + ")"

                if("Compiles to a" in str(df.loc[i, "Type"])): df.loc[i, "Type"] = str(df.loc[i, "Type"]).replace("Compiles to a ","")


            # drop rows with Field as blank
            #df = df.dropna(subset=['Field'])
            # drop rows with Field Type as blank
            #df = df.dropna(subset=['Field Type'])

            #print df.head(10)


            #df.drop("Field Type Details",axis=1,inplace=True)



            #replace ' ' in the column names to '_'
            df.columns = df.columns.str.replace(' ', '_')

            # All columns
            df.to_csv(output_csv_folder_path + output_csv_filename_all, sep=",", index=False, header=True)

            #Specific required columns
            df.rename(columns={"LDM_Object": "Entity_Name", "Field": "Attribute_Name","Type":"Attribute_Type"}, inplace=True)
            required_columns = ["System_Name", "Instance_Name", "Entity_Name", "Attribute_Name", "Owner", "Parent","Attribute_Type", "Description"]
            df.to_csv(output_csv_folder_path+output_csv_filename_sharepoint,sep=",",index=False,header=True,columns=required_columns)



            print " All good. LDM Object Report CSV file generated successfully.\n"
            print " Check the output csv file '{}' in the folder '{}' for all columns from the Avaloq report".format(output_csv_filename_all, output_csv_folder_path)
            print " Check the output csv file '{}' in the folder '{}' for columns specific to sharepont".format(output_csv_filename_sharepoint,output_csv_folder_path)
        else:
            print "\n\t ERROR: Excel File {} Not Found. Please check !".format(input_excel_filename)

    else:
        print "Not generating CSV file.....\n"
        print "Re-Run the program after deleting the first column in Avaloq report.\n"

def generateLDMInterfaceReport():
    #Analysis / Notes:
    #
    # There are essentially two types of fields: Complex Fields and Simple Fields.
    # XSD Simple Fields are mapped  by the Internal ID to the LDM Simple Fields - Directly
    # For XSD Complex Fields, LDM Object Name is given in the LDM Field
    # Use LDM Text Type - to find if the mapping is to a simple field or complex object


    input_excel_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Input\\LDM_Flat_Report\\"
    input_excel_filename = "LDM_Flat_Report_4_23_09_2016.xlsx"

    output_csv_filename = "LDM_INTF_Report_Output.csv"
    output_csv_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"

    print "\n######################################   LDM Interface Report  ################################################\n"
    print "Input Excel sheet Folder Name should be '{}' and File Name should be '{}' .\n".format(input_excel_folder_path,input_excel_filename)
    print "Please ensure you have deleted the first column from the Avaloq Report exported as excel sheet.\n"
    print "Confirm the input excel file, Folder Name , File Name and if you have deleted the first column ? [Yes/No]:"

    #answer = raw_input()
    answer = "Yes"
    if(answer.upper() == 'Yes'.upper()):


        if(checkFileName(input_excel_folder_path+input_excel_filename)):

            print "\n Excel File '{}' located".format(input_excel_filename)
            print "\n Generating CSV file, please wait.....\n"

            createFolderPath(input_excel_folder_path)
            createFolderPath(output_csv_folder_path)

            df = pd.read_excel(input_excel_folder_path + input_excel_filename, sheetname="Flat_Report", index_col=None)
            #df = pd.read_excel('./data/input/raw/'+input_excel_filename,sheetname="export0",index_col=None)


            #xls_file = pd.ExcelFile('./data/input/raw/LDM_OBJ_REPORT.xlsx')
            #df = xls_file.parse('export0',index_col="Field")


            #print df.loc[0, 'LDM Object']

            # insert Metadata related columns columns
            df.insert(0, "Source_System_Name", "ABS Dev")
            df.insert(1, "Source_Instance_Name", "XSD")
            df.insert(2, "Target_System_Name", "ABS")
            df.insert(3, "Target_Instance_Name", "LDM")
            df.insert(4, "MDR_Phase", "Phase 2")
            #df.insert(4, "Owner", "")
            #df.insert(5, "Parent", "")
            #df.insert(7,'Transformation_Mapping_Rule','')
            #df.insert(8,'Mapping_Name','')
            #df.insert(9,'Action','')
            #df.insert(10,'Last_Update_Date','')
            #df.insert(11,'Modified_By','')
            df.insert(5, 'Business_Rule', 'Direct')
            df.insert(6,'Comments',"Old Interface Name: "+df["Old Interface Name"] + "|" +"New Interface Name: " + df["Interface Name"])

            # insert two new columns
            # df.insert(6, "LDM Text Type",df["LDM Text"])
            # df.insert(7, "Internal ID"  ,df["LDM Text"])
            # df.insert(8, "LDM Object Type", df["LDM Text"])

            #print df.head()
            ''' '''
            # Go through each row and make corrections to cell values
            '''
            for i in range(0, len(df)):
                #print df.loc[i,'LDM Object']

                if (pd.isnull(df.loc[i, 'LDM Field'])):
                    # print "Inside None"
                    df.loc[i, 'LDM Field'] = df.loc[i, 'LDM Object']
            '''
                # #split the value by $ delimiter to get the LDM Object and LDM Field
                # if ("." in str(df.loc[i,"LDM Text"])):
                #     list_of_values = df.loc[i,"LDM Text"].split(".")
                #     df.loc[i,"LDM Text Type"]  = str(list_of_values[0]).replace("LDM:btfg$code_","")
                #     df.loc[i,"Internal ID"]    = list_of_values[1]
                #
                # else:
                #     #df.loc[i, "Internal ID LDM Object"] = df.loc[i,"Internal ID"]
                #     df.loc[i, "LDM Text Type"] = ""
                #     df.loc[i, "Internal ID"]   = ""

                # if ("$" in str(df.loc[i, "Internal ID"])):
                #     list_of_values = df.loc[i, "Internal ID"].split("$")
                #     df.loc[i, "LDM Object Type"] = list_of_values[0]
                #     if(list_of_values[0] == "obj"):
                #         df.loc[i, "LDM Object"] = "Object"

                # if(pd.isnull(df.loc[i,'Interface Name'])):
                #     #print "Inside None"
                #     df.loc[i, 'Interface Name'] = df.loc[i-1, 'Interface Name']
                #
                # if (pd.isnull(df.loc[i, 'Source Name'])):
                #     # print "Inside None"
                #     df.loc[i, 'Source Name'] = df.loc[i - 1, 'Source Name']


            # # drop rows if column "Element Name" is blank
            # df = df.dropna(subset=['Element Name'])

            # drop rows if column "LDM Field" is blank
            # df = df.dropna(subset=['LDM Field']) # Do not drop the LDM Field if blank, rather copy the LDM Object column value

            #print df.head(10)

            #drop the two columns
            #df.drop(labels=["LDM Field ID","LDM Object ID"],inplace=True,axis=1)

            # drop rows if the LDM Object ("Target Entity Name") is blank
            df = df.dropna(subset=['LDM Object'])

            df.rename(columns={"LDM INTL ID":"Transformation_Mapping_Rule","LDM Text":"Attribute_Description","LDM Object": "Target_Entity_Name_L","LDM Field":"Target_Attribute_Name_L","Source Name":"Source_Entity_Name","Element Name":"Source_Attribute_Name"}, inplace=True)



            required_columns = ["Source_System_Name","Source_Instance_Name","Source_Entity_Name","Source_Attribute_Name","Target_System_Name","Target_Instance_Name","Target_Entity_Name_L","Target_Attribute_Name_L","Comments","MDR_Phase","Attribute_Description","Business_Rule","Transformation_Mapping_Rule"]
            df.to_csv(output_csv_folder_path+output_csv_filename,sep=",",index=False,header=True,columns=required_columns)

            print " All good. LDM Interface Report CSV file generated successfully.\n"
            print " Check the output csv file '{}' in the folder '{}' ".format(output_csv_filename,output_csv_folder_path)

        else:
            print "\n\t ERROR: Excel File {} Not Found. Please check !".format(input_excel_filename)
    else:
        print "Not generating CSV file.....\n"
        print "Re-Run the program after deleting the first column in Avaloq report.\n"


def getXSD_LDM_Mapping_Delta(latest_ldm_report_filename):

    #First Column Name - Old Interface Name
    #Sheetname = Flat_Report

    input_excel_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Input\\LDM_Flat_Report\\"
    #input_excel_filename = "LDM_Flat_Report_4_23_09_2016.xlsx"
    input_excel_filename = latest_ldm_report_filename + ".xlsx"

    #output_csv_filename = "LDM_INTF_Report_Mappings_Delta.xlsx"
    output_csv_filename = latest_ldm_report_filename + "_ABS_XSD_LDM_Mappings_Delta.xlsx"

    output_csv_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    file = output_csv_folder_path + output_csv_filename
    columns_mappings_csv = ["Source Entity Name", "Source Attribute Name",
                            "Target Entity Name", "Target Attribute Name",
                            "Attribute Description", "Business Rule", "Transformation_Mapping rule", "Comments",
                            "Mapping Name", "Action", "Last_Update_Date", "Modified_By"]

    columns_mappings_csv_abs = ["Source Entity Name", "Source Attribute Name",
                            "Target Entity Name", "Target Attribute Name",
                            "Attribute Description", "Business Rule", "Transformation_Mapping rule", "Comments",
                            "Mapping Name"]

    object_duplicated_by_columns = ["Source Entity Name", "Source Attribute Name","Target Entity Name","Target Attribute Name"]
    object_duplicated_by_columns_drop = ["Source Entity Name", "Source Attribute Name", "Target Entity Name"]
    object_duplicated_by_columns_drop_4 = ["Source Entity Name", "Source Attribute Name", "Target Entity Name","Target Attribute Name"]
    writer = pd.ExcelWriter(output_csv_folder_path + output_csv_filename)

    # get the data from the latest report
    if (checkFileName(input_excel_folder_path + input_excel_filename)):
        print "\n Excel File '{}' located".format(input_excel_filename)
        print "\n Generating CSV file, please wait.....\n"

        createFolderPath(input_excel_folder_path)
        createFolderPath(output_csv_folder_path)

        df_latest_report = pd.read_excel(input_excel_folder_path + input_excel_filename, sheetname="Flat_Report", index_col=None)
        # df = pd.read_excel('./data/input/raw/'+input_excel_filename,sheetname="export0",index_col=None)
        df_latest_report["Source Name"] = df_latest_report["Source Name"].str.upper()
        df_latest_report["Element Name"] = df_latest_report["Element Name"].str.upper()
        df_latest_report["LDM Field"] = df_latest_report["LDM Field"].str.upper()
        df_latest_report["LDM Object"] = df_latest_report["LDM Object"].str.upper()

        df_latest_report.rename(columns={"LDM Object": "Target Entity Name", "LDM Field": "Target Attribute Name","Source Name": "Source Entity Name", "Element Name": "Source Attribute Name","LDM INTL ID": "Transformation_Mapping rule", "LDM Text": "Attribute Description"}, inplace=True)


        print "Latest Report Records:", df_latest_report.info()
        print df_latest_report.head()
        df_latest_report.sort_values(by=object_duplicated_by_columns, inplace=True, na_position='first',ascending=[True, True, True, True])

        df_latest_report["Target Attribute Name"].fillna("-", inplace=True)

        df_latest_report.to_excel(writer, sheet_name="Latest Report", index=False, columns=columns_mappings_csv_abs)
        df_latest_report = df_latest_report[(df_latest_report["Target Attribute Name"] <> "TO BE UPDATED")]
        df_latest_report = df_latest_report[(df_latest_report["Target Entity Name"].notnull())]
        #df_latest_report["Target Attribute Name"].fillna("-",inplace=True)
        #df_latest_report.rename(columns={"Modified_By": "Modified_By ABS"}, inplace=True)
        print "ABS:",df_latest_report.tail(5)
        #df_latest_report.head()
        #df_latest_report.drop(["Modified_By"], axis=1, inplace=True)
    # get the data from the sharepoint


    df_sp = pd.DataFrame(getMapping_XSD_LDM(list_name_mapping_xsd_ldm, GP_PHASE_NO),columns=columns_mappings_csv)


    print "Sharepoint Records:",df_sp.info()
    print df_sp.head()
    df_sp.sort_values(by=object_duplicated_by_columns, inplace=True, na_position='first',
                                 ascending=[True, True, True, True])
    #df_sp["Target Attribute Name"].fillna("-", inplace=True)
    #df_sp["Target Attribute Name"].replace(np.NaN, '-')
    #df_sp["Target Attribute Name"] = df_sp["Target Attribute Name"].apply(lambda x: x if not pd.isnull(x) else '-')

    df_sp.to_excel(writer, sheet_name="Sharepoint", index=False, columns=columns_mappings_csv)
    df_sp.rename(columns={"Attribute Description":"Attribute Description SP","Attribute Description": "Attribute Description SP","Transformation_Mapping rule":"Transformation_Mapping rule SP"}, inplace=True)
    #df_sp["Target Attribute Name"].fillna("-",inplace=True)
    print "SP",df_sp.tail(5)

    # get the delta by join the dfs
    join_cols = ["Source Entity Name", "Source Attribute Name","Target Entity Name","Target Attribute Name"]
    df_join = pd.merge(left=df_latest_report, right=df_sp, how='left', left_on=join_cols,right_on=join_cols)

    df_join["Business Rule"] = 'Direct'
    df_join["Comments"] = "Old Interface Name: " + df_join[
        "Old Interface Name"] + "|" + "New Interface Name: " + df_join["Interface Name"]
    #df_join.drop_duplicates(subset=object_duplicated_by_columns_drop_4, keep=False, inplace=True)
    print "Join:",df_join.head(5)
    df_join = df_join[df_join["Modified_By"].isnull()]
    df_join.to_excel(writer, sheet_name="Delta by Join", index=False,
                     columns=columns_mappings_csv)

    # get the difference between sharepoint and latest report
        #concat both the dfs
    df_all_mappings = pd.concat([df_latest_report,df_sp])

    print "Before dropping duplicates:",df_all_mappings.info()
    print df_all_mappings.head()
    df_all_mappings.to_excel(writer, sheet_name="Delta - Before dropping", index=False, columns=columns_mappings_csv)

        #drop duplicates
    # drop rows if the LDM Object ("Target Entity Name") is blank
    df_all_mappings = df_all_mappings.dropna(subset=['Target Entity Name'])

    #df_all_mappings.fillna

    df_all_mappings.drop_duplicates(subset=object_duplicated_by_columns_drop, keep=False, inplace=True)

    df_all_mappings.insert(0, "Source System Name", "ABS Dev")
    df_all_mappings.insert(1, "Source Instance Name", "XSD")
    df_all_mappings.insert(2, "Target System Name", "ABS")
    df_all_mappings.insert(3, "Target Instance Name", "LDM")
    df_all_mappings.insert(4, "MDR Phase", "Phase 2")


    #df_all_mappings.insert(5, 'Business Rule', 'Direct')
    #df_all_mappings.insert(5, 'Comments', "Old Interface Name: " + df_all_mappings["Old Interface Name"] + "|" + "New Interface Name: " + df_all_mappings["Interface Name"])
    df_all_mappings["Business Rule"] = 'Direct'
    df_all_mappings["Comments"] = "Old Interface Name: " + df_all_mappings["Old Interface Name"] + "|" + "New Interface Name: " + df_all_mappings["Interface Name"]


    print "After dropping duplicates:",df_all_mappings.info()
    df_all_mappings.to_excel(writer, sheet_name="Delta - After dropping",index=False,columns=columns_mappings_csv)

    df_all_mappings_updated = df_all_mappings[df_all_mappings["Target Attribute Name"] == "TO BE UPDATED"]
    df_all_mappings_new_entries = df_all_mappings[df_all_mappings["Target Attribute Name"] <> "TO BE UPDATED"]

    df_all_mappings_updated.to_excel(writer, sheet_name="To Be Updated", index=False, columns=columns_mappings_csv)
    df_all_mappings_new_entries.to_excel(writer, sheet_name="New Entries", index=False, columns=columns_mappings_csv)
    print "Process Completed. Check file {}.".format(file)

def getXSD_Fields_Delta(latest_ldm_report_filename):

    #First Column Name - Old Interface Name
    #Sheetname = Flat_Report

    input_excel_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Input\\LDM_Flat_Report\\"
    #input_excel_filename = "LDM_Flat_Report_4_23_09_2016.xlsx"
    input_excel_filename = latest_ldm_report_filename + ".xlsx"

    output_csv_filename = latest_ldm_report_filename + "_ABS_XSD_Fields_Delta.xlsx"
    output_csv_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"

    columns_mappings_csv = ["Interface Name","Entity Name", "Attribute Name","Type"]
    object_duplicated_by_columns = ["Entity Name", "Attribute Name"]
    object_duplicated_by_columns_drop = ["Entity Name", "Attribute Name"]

    writer = pd.ExcelWriter(output_csv_folder_path + output_csv_filename)

    # get the data from the latest report
    if (checkFileName(input_excel_folder_path + input_excel_filename)):
        print "\n Excel File '{}' located".format(input_excel_filename)
        print "\n Generating CSV file, please wait.....\n"

        createFolderPath(input_excel_folder_path)
        createFolderPath(output_csv_folder_path)

        df_latest_report = pd.read_excel(input_excel_folder_path + input_excel_filename, sheetname="Flat_Report", index_col=None)
        # df = pd.read_excel('./data/input/raw/'+input_excel_filename,sheetname="export0",index_col=None)
        df_latest_report["Source Name"] = df_latest_report["Source Name"].str.upper()
        df_latest_report["Element Name"] = df_latest_report["Element Name"].str.upper()


        df_latest_report.rename(columns={"Source Name": "Entity Name", "Element Name": "Attribute Name"}, inplace=True)


        print "Latest Report Records:", df_latest_report.info()
        print df_latest_report.head()
        df_latest_report.sort_values(by=["Entity Name","Attribute Name"], inplace=True, na_position='first',ascending=[True, True])
        #dont assume there records are going to be unique within this report. There are duplicates at Entity and Attribute level
        #So remove duplicates, keeping first row. so that in the next joins , we can remove all.
        df_latest_report.drop_duplicates(subset=["Entity Name","Attribute Name"],keep='first',inplace=True)
        df_latest_report.to_excel(writer, sheet_name="Latest Report", index=False, columns=columns_mappings_csv)


    # get the data from the sharepoint


    df_sp = pd.DataFrame(getObjects(list_name_xsd_fields_abs),columns=columns_mappings_csv)
    #df_sp.insert(0,"Interface Name","")
    df_sp = df_sp[df_sp["Type"] == "Attribute"]
    print "Sharepoint Records:",df_sp.info()
    print df_sp.head()
    df_sp.sort_values(by=["Entity Name","Attribute Name"], inplace=True, na_position='first',
                                 ascending=[True, True])
    df_sp.to_excel(writer, sheet_name="Sharepoint", index=False, columns=columns_mappings_csv)

    # get the delta by join the dfs
    df_join = pd.merge(left=df_latest_report, right=df_sp, how='left', left_on=["Entity Name", "Attribute Name"],
                       right_on=["Entity Name", "Attribute Name"])
    df_join = df_join[df_join["Type"].isnull()]
    df_join.to_excel(writer, sheet_name="Delta by Join", index=False,
                     columns=["Entity Name", "Attribute Name", "Type"])

    # get the difference between sharepoint and latest report
        #concat both the dfs
    df_all_mappings = pd.concat([df_latest_report,df_sp])

    print "Before dropping duplicates:",df_all_mappings.info()
    print df_all_mappings.head()
    df_all_mappings.to_excel(writer, sheet_name="Delta - Before dropping", index=False, columns=columns_mappings_csv)

        #drop duplicates
    # drop rows if the LDM Object ("Target Entity Name") is blank
    #df_all_mappings = df_all_mappings.dropna(subset=['Target Entity Name'])

    #df_all_mappings.fillna

    df_all_mappings.drop_duplicates(subset=["Entity Name","Attribute Name"], keep=False, inplace=True)
    #df_all_mappings["Comments"] = "Old Interface Name: " + df_all_mappings["Old Interface Name"] + "|" + "New Interface Name: " + df_all_mappings["Interface Name"]


    print "After dropping duplicates:",df_all_mappings.info()
    df_all_mappings.to_excel(writer, sheet_name="Delta - After dropping",index=False,columns=columns_mappings_csv)

'''
def getLDM_Fields_Delta(latest_ldm_report_filename):

    #First Column Name - Old Interface Name
    #Sheetname = Flat_Report

    input_excel_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Input\\LDM_Flat_Report\\"
    #input_excel_filename = "LDM_Flat_Report_4_23_09_2016.xlsx"
    input_excel_filename = latest_ldm_report_filename + ".xlsx"

    output_csv_filename = latest_ldm_report_filename + "_ABS_LDM_Fields_Delta.xlsx"
    output_csv_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    file = output_csv_folder_path + output_csv_filename
    columns_mappings_csv = ["Entity Name","Attribute Name","Description","Type"]
    object_duplicated_by_columns = ["Entity Name", "Attribute Name"]
    object_duplicated_by_columns_drop = ["Entity Name", "Attribute Name"]

    writer = pd.ExcelWriter(output_csv_folder_path + output_csv_filename)

    # get the data from the latest report
    if (checkFileName(input_excel_folder_path + input_excel_filename)):
        print "\n Excel File '{}' located".format(input_excel_filename)
        print "\n Generating CSV file, please wait.....\n"

        createFolderPath(input_excel_folder_path)
        createFolderPath(output_csv_folder_path)

        df_latest_report = pd.read_excel(input_excel_folder_path + input_excel_filename, sheetname="Flat_Report", index_col=None)
        # df = pd.read_excel('./data/input/raw/'+input_excel_filename,sheetname="export0",index_col=None)
        df_latest_report["LDM Field"] = df_latest_report["LDM Field"].str.upper()
        df_latest_report["LDM Object"] = df_latest_report["LDM Object"].str.upper()

        #ignore the rows with blank Entity Name
        df_latest_report = df_latest_report[df_latest_report["LDM Object"].notnull()]

        df_latest_report.rename(columns={"LDM Object": "Entity Name", "LDM Field": "Attribute Name","LDM Text":"Description"}, inplace=True)


        print "Latest Report Records:", df_latest_report.info()
        print df_latest_report.head()
        df_latest_report.sort_values(by=["Entity Name","Attribute Name"], inplace=True, na_position='first',ascending=[True, True])
        #dont assume there records are going to be unique within this report. There are duplicates at Entity and Attribute level
        #So remove duplicates, keeping first row. so that in the next joins , we can remove all.
        df_latest_report.drop_duplicates(subset=["Entity Name","Attribute Name"],keep='first',inplace=True)
        df_latest_report.to_excel(writer, sheet_name="Latest Report", index=False, columns=columns_mappings_csv)

    # get the data from the sharepoint


    df_sp = pd.DataFrame(getObjects(list_name_ldm_fields),columns=columns_mappings_csv)


    # take only the attributes
    df_sp = df_sp[df_sp["Type"] == "Attribute"]

    print "Sharepoint Records:",df_sp.info()
    print df_sp.head()
    df_sp.sort_values(by=["Entity Name","Attribute Name"], inplace=True, na_position='first',
                                 ascending=[True, True])
    df_sp.drop_duplicates(subset=["Entity Name", "Attribute Name"], keep='first', inplace=True)
    df_sp.to_excel(writer, sheet_name="Sharepoint", index=False, columns=columns_mappings_csv)


    # get the difference between sharepoint and latest report
        #concat both the dfs
    df_all_mappings = pd.concat([df_latest_report,df_sp])

    print "Before dropping duplicates:",df_all_mappings.info()
    print df_all_mappings.head()
    df_all_mappings.to_excel(writer, sheet_name="Concated records", index=False, columns=columns_mappings_csv)

        #drop duplicates
    # drop rows if the LDM Object ("Target Entity Name") is blank
    #df_all_mappings = df_all_mappings.dropna(subset=['Target Entity Name'])

    #df_all_mappings.fillna

    df_all_mappings.drop_duplicates(subset=["Entity Name","Attribute Name"], keep=False, inplace=True)
    #df_all_mappings["Comments"] = "Old Interface Name: " + df_all_mappings["Old Interface Name"] + "|" + "New Interface Name: " + df_all_mappings["Interface Name"]


    print "After dropping duplicates:",df_all_mappings.info()
    df_all_mappings.to_excel(writer, sheet_name="Delta",index=False,columns=columns_mappings_csv)
    print "Process Completed. Check file {}.".format(file)
'''

def getLDM_Fields_Delta_ByJoin(latest_ldm_report_filename):

    #First Column Name - Old Interface Name
    #Sheetname = Flat_Report

    input_excel_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Input\\LDM_Flat_Report\\"
    #input_excel_filename = "LDM_Flat_Report_4_23_09_2016.xlsx"
    input_excel_filename = latest_ldm_report_filename + ".xlsx"

    output_csv_filename = latest_ldm_report_filename + "_ABS_LDM_Fields_Delta.xlsx"
    output_csv_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    file = output_csv_folder_path + output_csv_filename
    columns_mappings_csv = ["Entity Name","Attribute Name","Description","Type"]
    object_duplicated_by_columns = ["Entity Name", "Attribute Name"]
    object_duplicated_by_columns_drop = ["Entity Name", "Attribute Name"]

    writer = pd.ExcelWriter(output_csv_folder_path + output_csv_filename)

    # get the data from the latest report
    if (checkFileName(input_excel_folder_path + input_excel_filename)):
        print "\n Excel File '{}' located".format(input_excel_filename)
        print "\n Generating CSV file, please wait.....\n"

        createFolderPath(input_excel_folder_path)
        createFolderPath(output_csv_folder_path)

        df_latest_report = pd.read_excel(input_excel_folder_path + input_excel_filename, sheetname="Flat_Report", index_col=None)
        # df = pd.read_excel('./data/input/raw/'+input_excel_filename,sheetname="export0",index_col=None)
        df_latest_report["LDM Field"] = df_latest_report["LDM Field"].str.upper()
        df_latest_report["LDM Object"] = df_latest_report["LDM Object"].str.upper()

        #ignore the rows with blank Entity Name
        df_latest_report = df_latest_report[df_latest_report["LDM Object"].notnull()]

        df_latest_report.rename(columns={"LDM Object": "Entity Name", "LDM Field": "Attribute Name","LDM Text":"Description"}, inplace=True)


        print "Latest Report Records:", df_latest_report.info()
        print df_latest_report.head()
        df_latest_report.sort_values(by=["Entity Name","Attribute Name"], inplace=True, na_position='first',ascending=[True, True])
        #dont assume there records are going to be unique within this report. There are duplicates at Entity and Attribute level
        #So remove duplicates, keeping first row. so that in the next joins , we can remove all.

        #fill the blanks with -. Needed for comparison.
        df_latest_report["Attribute Name"].fillna("-", inplace=True)

        df_latest_report_d   = df_latest_report[df_latest_report.duplicated(subset=["Entity Name", "Attribute Name"], keep='first')]
        df_latest_report_d.to_excel(writer, sheet_name="Latest Report - Duplicate", index=False, columns=columns_mappings_csv)

        df_latest_report.drop_duplicates(subset=["Entity Name","Attribute Name"],keep='first',inplace=True)
        df_latest_report.to_excel(writer, sheet_name="Latest Report", index=False, columns=columns_mappings_csv)

        df_latest_report.rename(columns={"Description": "Description ABS Report"}, inplace=True)

    # get the data from the sharepoint


    df_sp = pd.DataFrame(getObjects(list_name_ldm_fields),columns=columns_mappings_csv)


    # take only the attributes
    df_sp = df_sp[df_sp["Type"] == "Attribute"]

    print "Sharepoint Records:",df_sp.info()

    df_sp["Attribute Name"] = df_sp["Attribute Name"].apply(lambda x: x if (x <> '') else '-')

    print df_sp.head()
    df_sp.sort_values(by=["Entity Name","Attribute Name"], inplace=True, na_position='first',
                                 ascending=[True, True])
    df_sp.drop_duplicates(subset=["Entity Name", "Attribute Name"], keep='first', inplace=True)
    df_sp.to_excel(writer, sheet_name="Sharepoint", index=False, columns=columns_mappings_csv)

    #get the delta by join the dfs
    df_join = pd.merge(left=df_latest_report,right=df_sp,how='left',left_on=["Entity Name","Attribute Name"],right_on=["Entity Name","Attribute Name"])
    df_join = df_join[df_join["Type"].isnull()]
    df_join.to_excel(writer, sheet_name="Delta by Join", index=False, columns=["Entity Name","Attribute Name","Description ABS Report","Type"])

    # get the difference between sharepoint and latest report
        #concat both the dfs
    df_all_mappings = pd.concat([df_latest_report,df_sp])

    print "Before dropping duplicates:",df_all_mappings.info()
    print df_all_mappings.head()
    df_all_mappings.to_excel(writer, sheet_name="Concated records", index=False, columns=columns_mappings_csv)

        #drop duplicates
    # drop rows if the LDM Object ("Target Entity Name") is blank
    #df_all_mappings = df_all_mappings.dropna(subset=['Target Entity Name'])

    #df_all_mappings.fillna

    df_all_mappings.drop_duplicates(subset=["Entity Name","Attribute Name"], keep=False, inplace=True)
    #df_all_mappings["Comments"] = "Old Interface Name: " + df_all_mappings["Old Interface Name"] + "|" + "New Interface Name: " + df_all_mappings["Interface Name"]


    print "After dropping duplicates:",df_all_mappings.info()
    df_all_mappings.to_excel(writer, sheet_name="Delta",index=False,columns=columns_mappings_csv)
    print "Process Completed. Check file {}.".format(file)

#generateLDMObjectReport()
#generateLDMInterfaceReport()

getXSD_Fields_Delta(GV_Latest_LDM_Report_Filename)
getLDM_Fields_Delta_ByJoin(GV_Latest_LDM_Report_Filename)
getXSD_LDM_Mapping_Delta(GV_Latest_LDM_Report_Filename)



#getLDM_Fields_Delta(GV_Latest_LDM_Report_Filename)