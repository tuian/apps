import pandas as pd
import os
from mdr_util import *

def checkPhase1_2_Duplicates():

    input_excel_folder_path_phase1 = "C:\MDR\Data\Repository\Input\Phase1"
    input_excel_filename_phase1 = "\Phase1_Objects_Mappings.xlsx"

    input_excel_folder_path_phase2 = "C:\MDR\Data\Repository\CSV_Sharepoint_Output"
    input_excel_filename_phase2_object = "\Objects.csv"
    input_excel_filename_phase2_mappings = "\Mappings.csv"

    output_csv_filename_all = "LDM_OBJ_REPORT_Output_All.csv"
    output_csv_filename_sharepoint = "LDM_OBJ_REPORT_Output_Sharepoint.csv"
    output_csv_folder_path = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"

    print "\n####################   Phase 1 and Phase 2 - Objects and Mappings - Duplicate Extrator  ####################\n"
    required_columns_objects = []
    required_columns_mappings = []

    #Phase 1
    df_phase1_objects = pd.read_excel(input_excel_folder_path_phase1+input_excel_filename_phase1,sheetname="Objects",index_col=None)
    df_phase1_mappings = pd.read_excel(input_excel_folder_path_phase1 + input_excel_filename_phase1, sheetname="Mappings",
                                      index_col=None)
    df_phase1_objects.insert(0,"Phase","Phase 1")
    df_phase1_mappings.insert(0, "Phase", "Phase 1")
    df_phase1_objects["Entity Name"] = df_phase1_objects["Entity Name"].str.strip()
    df_phase1_objects["Attribute Name"] = df_phase1_objects["Attribute Name"].str.strip()

    print df_phase1_objects.head()
    print df_phase1_mappings.head()

    #Phase 2
    df_phase2_objects  = pd.read_csv(input_excel_folder_path_phase2 + input_excel_filename_phase2_object,sep=",")
    df_phase2_mappings = pd.read_csv(input_excel_folder_path_phase2 + input_excel_filename_phase2_mappings, sep=",")
    df_phase2_objects.insert(0, "Phase", "Phase 2")
    df_phase2_mappings.insert(0, "Phase", "Phase 2")


    print df_phase2_objects.head()
    print df_phase2_mappings.head()

    #compare objects
    object_duplicated_by_columns = ["System Name","Entity Name", "Attribute Name","Type"]
    object_sort_by_columns       = ["System Name", "Entity Name", "Attribute Name", "Type"]

    mapping_duplicated_by_columns = []

    # drop duplicates within phases before comparing Phase 1 and Phase 2

        ###drop the duplicate rows in each Phase , keep first and inplace=True
    print "BEFORE: df_phase1_objects",len(df_phase1_objects)
    df_phase1_objects.drop_duplicates(subset=object_duplicated_by_columns, keep='first', inplace=True)
    print "AFTER: df_phase1_objects", len(df_phase1_objects)
    df_phase2_objects.drop_duplicates(subset=object_duplicated_by_columns, keep='first', inplace=True)

    # add dfs
    df_object = pd.concat([df_phase1_objects, df_phase2_objects])

        # sort df
    df_object.sort_values(by=object_sort_by_columns, inplace=True, na_position='first', ascending=[False, True, True, True])

        #get duplicates
    df_object_duplicated = df_object[df_object.duplicated(subset=object_duplicated_by_columns, keep=False)]

    columns_objects_csv = ["Phase","System Name", "Instance Name", "Entity Name", "Attribute Name", "Type"]
    df_object_duplicated = df_object_duplicated[df_object_duplicated["Phase"] == "Phase 2"]
    df_object_duplicated.to_csv(input_excel_folder_path_phase2+"\Phase1_Phase2_Object_Duplicates.csv", sep=",",header=True, index=None,columns=columns_objects_csv)

        #drop all duplicates from Phase 1 and Phase 2 combined
    columns_objects_csv_loading = ["System Name", "Instance Name", "Entity Name", "Attribute Name", "Owner", "Parent", "Type","Description", "URL", "Document Name", "XPATH"]
    df_object.drop_duplicates(subset=object_duplicated_by_columns, keep=False, inplace=True)
    df_object = df_object[df_object["Phase"] == "Phase 2"]
    df_object.to_csv(input_excel_folder_path_phase2 + "\BTP_Phase2_Objects.csv", sep=",",header=True, index=None, columns=columns_objects_csv_loading)


    # compare mappings

    #mapping_duplicated_by_columns = ["Source Entity Name", "Source Attribute Name"]
    #mapping_sort_by_columns = ["Source Entity Name", "Source Attribute Name"]
    mapping_duplicated_by_columns = ["Source Entity Name", "Source Attribute Name","Target Entity Name", "Target Attribute Name"]
    mapping_sort_by_columns       = ["Source Entity Name", "Source Attribute Name","Target Entity Name", "Target Attribute Name"]

        ###drop the duplicate rows, keep first and inplace=True
    df_phase1_mappings.drop_duplicates(subset=mapping_duplicated_by_columns, keep='first', inplace=True)
    df_phase2_mappings.drop_duplicates(subset=mapping_duplicated_by_columns, keep='first', inplace=True)

    df_mappings = pd.concat([df_phase1_mappings, df_phase2_mappings])
    #df_mappings.sort_values(by=mapping_sort_by_columns, inplace=True, na_position='first',ascending=[True, True])
    df_mappings.sort_values(by=mapping_sort_by_columns, inplace=True, na_position='first',ascending=[True, True,True,True])

    # get duplicates
    df_mapping_duplicated = df_mappings[df_mappings.duplicated(subset=mapping_duplicated_by_columns, keep=False)]

    columns_mappings_csv = ["Phase","Source System Name", "Source Instance Name", "Source Entity Name", "Source Attribute Name",
                            "Target System Name", "Target Instance Name", "Target Entity Name", "Target Attribute Name"
                            ]

    df_mapping_duplicated = df_mapping_duplicated[df_mapping_duplicated["Phase"] == "Phase 2"]
    df_mapping_duplicated.to_csv(input_excel_folder_path_phase2 + "\Phase1_Phase2_Mapping_Duplicates.csv", sep=",",header=True, index=None,columns=columns_mappings_csv)

        #drop all duplicates from Phase 1 and Phase 2 combined
    columns_mappings_csv_loading = ["Source System Name", "Source Instance Name", "Source Entity Name", "Source Attribute Name",
                            "Target System Name", "Target Instance Name", "Target Entity Name", "Target Attribute Name",
                            "Attribute Description", "Business Rule", "Transformation_Mapping rule", "Comments",
                            "Mapping Name", "Action", "Last_Update_Date", "Modified_By"]


    df_mappings.drop_duplicates(subset=mapping_duplicated_by_columns, keep=False, inplace=True)
    df_mappings = df_mappings[df_mappings["Phase"] == "Phase 2"]
    df_mappings.to_csv(input_excel_folder_path_phase2 + "\BTP_Phase2_Mappings.csv", sep=",",header=True, index=None, columns=columns_mappings_csv_loading)

if __name__ == "__main__":

    checkPhase1_2_Duplicates()
