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
Performance Tuning:
Improved the performance from ~20 mins to approx 3 mins, aftering moving the ABS Fields to a global cache.
 Initially was doing a nasty io operation in the for loop (reading the ABS fields from excel sheet each time)
 Thanks to PycallGraph module that helped to profile the code and understand the operations vs time.

From: C:\Python27\Scripts\
C:\Python27\python pycallgraph -v --max-depth 1 graphviz --output-file=XSDFields_Matching_22_09_1125.png -- C:\apps\apps\metadata\XSDFields_Matching.py


'''
from __future__ import division
import pandas as pd
import time
from mdr_util import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import cProfile
import re
from pycallgraph import PyCallGraph,Config,GlobbingFilter
from pycallgraph.output import GraphvizOutput
def addRow(key,value):
    object = {}
    object["Key"] = key
    object["Value"] = value

    return object

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
def columnValuesWithXSD(column_name):
    print "Setting ABS Fields in Global Cache: {}".format(column_name)
    #column_name should be
        #Entity Name
        #Attribute Name

    #list = ["BTFG$UI_BP.BP","BTFG$UI_BP_LIST.ALL#CUSTR"]

    csv_folder_path_Avaloq = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
    csv_filename_2 = "ABS_Fields.xlsx"

    df = pd.read_excel(csv_folder_path_Avaloq + csv_filename_2, sheetname="Sheet1")

    # for i in range(0, len(df)):
    #     # split the value by $ delimiter to get the LDM Object and LDM Field
    #     if (".XSD" in str(df.loc[i, "Source Name"])):
    #         df.loc[i, "Source Name"] = str(df.loc[i, "Source Name"]).replace(".XSD", "")

    #list = set(df["Entity Name"])
    list = set(df[column_name])

    #print list
    return list

GV_ABS_ENTITIES   = columnValuesWithXSD("Entity Name")
GV_ABS_ATTRIBUTES = columnValuesWithXSD("Attribute Name")

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

def setLookupRange():
    entities_list = []
    pass


def getLookupRange_Entities():
    entities_list = []

    return entities_list

def getLookupRange_Attributes():
    attributes_list = []

    return attributes_list


def getMatchingXSD_By_MatchPercent(row,p,input_column_name,lookup_field_type):
    #match_percentage=88
    match_percentage = p

    #input_string = row["Target Entity Name With XSD"]
    input_string = row[input_column_name]

    if input_string ==None: input_string = 'nan'

    # print "===Entering getMatchingXSD ==="
    # print "Input value:",input_string

    if ((input_string <> 'nan')):

        if(lookup_field_type=="E"):
            matching_xsd_values = process.extractOne(input_string,choices=GV_ABS_ENTITIES,score_cutoff=match_percentage)

        if (lookup_field_type == "A"):
            matching_xsd_values = process.extractOne(input_string, choices=GV_ABS_ATTRIBUTES, score_cutoff=match_percentage)

        #matching_xsd_values = "Fuzzy"

        if matching_xsd_values == None:
            #print "Process Output is None"
            return 'No Match'

        if matching_xsd_values <> None:
            #return list_of_XSDs[matching_xsd_values[0]]
            # print "Process Value:", matching_xsd_values
            # print type(matching_xsd_values)

            # print "Return Value:",matching_xsd_values[0]
            # print type(str(matching_xsd_values[0]))
            if (matching_xsd_values[1] ==100): return "Exact Match"
            if(matching_xsd_values[1] >= match_percentage):
                #print "===Exiting getMatchingXSD ==="
                #return "Partial Match: {} with {}% match".format(matching_xsd_values[0], matching_xsd_values[1])
                return "{}".format(matching_xsd_values[0])
            else:
                # print "===Exiting getMatchingXSD ==="
                return 'Partial Match - Below Control Value {}%, Returned: {} with {}% match'.format(match_percentage, matching_xsd_values[0], matching_xsd_values[1])

    # print 'No Match'
    # print "===Exiting getMatchingXSD ==="
    return 'No Match'
def getMatchingXSD_90(row):
    match_percentage=90
    input_string = row["Target Entity Name With XSD"]
    if input_string ==None: input_string = 'nan'

    # print "===Entering getMatchingXSD ==="
    # print "Input value:",input_string

    if ((input_string <> 'nan')):
        matching_xsd_values = process.extractOne(input_string,choices=columnValuesWithXSD("Target Entity Name With XSD"),score_cutoff=match_percentage)
        #matching_xsd_values = "Fuzzy"

        if matching_xsd_values == None:
            #print "Process Output is None"
            return 'No Match'

        if matching_xsd_values <> None:
            #return list_of_XSDs[matching_xsd_values[0]]
            # print "Process Value:", matching_xsd_values
            # print type(matching_xsd_values)

            # print "Return Value:",matching_xsd_values[0]
            # print type(str(matching_xsd_values[0]))
            if (matching_xsd_values[1] ==100): return "Exact Match"
            if(matching_xsd_values[1] >= match_percentage):
                #print "===Exiting getMatchingXSD ==="
                #return "Partial Match: {} with {}% match".format(matching_xsd_values[0], matching_xsd_values[1])
                return "{}".format(matching_xsd_values[0])
            else:
                # print "===Exiting getMatchingXSD ==="
                return 'Partial Match - Below Control Value {}%, Returned: {} with {}% match'.format(match_percentage, matching_xsd_values[0], matching_xsd_values[1])

    # print 'No Match'
    # print "===Exiting getMatchingXSD ==="
    return 'No Match'
def getMatchingXSD_By_MatchPercentage(input_string):
    match_percentage=95
    #match_percentage= int(match_percentage_list[0])
    #input_string = row["Target Entity Name With XSD"]

    if input_string ==None: input_string = 'nan'

    # print "===Entering getMatchingXSD ==="
    # print "Input value:",input_string

    if ((input_string <> 'nan')):
        matching_xsd_values = process.extractOne(input_string,choices=columnValuesWithXSD("Target Entity Name With XSD"),score_cutoff=match_percentage)
        #matching_xsd_values = "Fuzzy"

        if matching_xsd_values == None:
            #print "Process Output is None"
            return 'No Match'

        if matching_xsd_values <> None:
            #return list_of_XSDs[matching_xsd_values[0]]
            # print "Process Value:", matching_xsd_values
            # print type(matching_xsd_values)

            # print "Return Value:",matching_xsd_values[0]
            # print type(str(matching_xsd_values[0]))
            if (matching_xsd_values[1] ==100): return "Exact Match"
            if(matching_xsd_values[1] >= match_percentage):
                #print "===Exiting getMatchingXSD ==="
                #return "Partial Match: {} with {}% match".format(matching_xsd_values[0], matching_xsd_values[1])
                return "{}".format(matching_xsd_values[0])
            else:
                # print "===Exiting getMatchingXSD ==="
                return 'Partial Match - Below Control Value {}%, Returned: {} with {}% match'.format(match_percentage, matching_xsd_values[0], matching_xsd_values[1])

    # print 'No Match'
    # print "===Exiting getMatchingXSD ==="
    return 'No Match'

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

def getXSDFields_FromAvaloReport_Delta():
    csv_folder_path_Avaloq_input = "C:\\MDR\\Data\\Avaloq_Report_Export\\Input\\LDM_Flat_Report\\"
    csv_folder_path_Avaloq = "C:\\MDR\\Data\\Avaloq_Report_Export\\Output\\"
    input_filename_1 = "LDM_Flat_Report_1_10_09_2016.xlsx"
    input_filename_2 = "LDM_Flat_Report_2_15_09_2016.xlsx"
    input_filename_3 = "LDM_Flat_Report_3_19_09_2016.xlsx"
    input_filename_4 = "LDM_Flat_Report_4_23_09_2016.xlsx"
    input_filename_5 = "LDM_Flat_Report_5_27_09_2016.xlsx"

    required_columns = ["Interface Name","Source Name","Element Name"]
    output_filename = "ABS_LDM_DELTA_27_09_2016.xlsx"
    output_filename_duplicates = "ABS_LDM_DELTA_27_09_2016_Dup.xlsx"


    df_1 = pd.read_excel(csv_folder_path_Avaloq_input + input_filename_1, sheetname="Flat_Report")
    df_2 = pd.read_excel(csv_folder_path_Avaloq_input + input_filename_2, sheetname="Flat_Report")
    df_3 = pd.read_excel(csv_folder_path_Avaloq_input + input_filename_3, sheetname="Flat_Report")
    df_4 = pd.read_excel(csv_folder_path_Avaloq_input + input_filename_4, sheetname="Flat_Report")
    df_5 = pd.read_excel(csv_folder_path_Avaloq_input + input_filename_5, sheetname="Flat_Report")

    joined_df = pd.concat([df_1,df_2,df_3,df_4,df_5])

    joined_df["Source Name"] =  joined_df["Source Name"].str.upper()
    joined_df["Element Name"] = joined_df["Element Name"].str.upper()

    joined_df_duplicates = joined_df[joined_df.duplicated(subset=["Source Name","Element Name"],keep='first')]

    joined_df.drop_duplicates(subset=["Source Name","Element Name"],keep=False,inplace=True)

    #joined_df_duplicates.sort_values(by=["Source Name","Element Name"], inplace=True)
    joined_df.sort_values(by=["Source Name", "Element Name"], inplace=True)

    joined_df.to_excel(csv_folder_path_Avaloq + output_filename, columns=required_columns,index=False, header=True)
    joined_df_duplicates.to_excel(csv_folder_path_Avaloq + output_filename_duplicates, columns=required_columns,index=False, header=True)

    df_1.info()
    df_2.info()
    df_3.info()
    df_4.info()
    df_5.info()
    joined_df.info()
    joined_df_duplicates.info()

def getABS_XSD_FieldsFromSharepoint():
    reload(sys)
    sys.setdefaultencoding('utf8')
    list_objects = []

    rows = sharepointListRowsByListName("ABS_XSD_FIELDS")

    for row in rows:
        row_object = {}
        row_object["System Name"] = str(row.System_Name).encode("utf-8")
        row_object["Instance Name"] = str(row.Instance_Name).encode("utf-8")
        #row_object["Entity Name"] = str(row.Entity_Name_Duplicate).encode("utf-8")
        row_object["Entity Name"] = str(row.Entity_Name).encode("utf-8").upper()
        row_object["Attribute Name"] = str(row.Attribute_Name).upper()
        row_object["Owner"] = str(row.Owner).encode("utf-8")
        row_object["Parent"] = str(row.Parent).encode("utf-8")
        row_object["Type"] = str(row.Entity_Type).encode("utf-8")
        #row_object["Description"] = str(row.Description).encode("utf-8")
        row_object["Description"] = cleanHTMLTags(row.Description)
        row_object["URL"] = str(row.URL).encode("utf-8")
        row_object["Document Name"] = str(row.Document_Name).encode("utf-8")
        row_object["XPATH"] = cleanHTMLTags(row.XPATH)

        # row_object[""] = row.
        list_objects.append(row_object)

    print "getABS_XSD_Fields('{}') | Count = {} ".format("Mapping_IFS_XSD", len(list_objects))

    return list_objects

def getIFS_XSD_FieldsFromSharepoint():

    reload(sys)
    sys.setdefaultencoding('utf8')
    list_objects = []

    rows = sharepointListRowsByListName("Mapping_IFS_XSD")

    for row in rows:
        row_object = {}


        row_object["Target Entity Name"] = str(row.Target_Entity_Name_Duplicate).upper()
        row_object["Target Attribute Name"] = str(row.Target_Attribute_Name_Duplicate).upper()

        row_object["Target Entity Name ABS"] = str(row.Target_Entity_Name_ABS_Object_D).upper()
        row_object["Target Attribute Name ABS"] = str(row.Target_Attribute_Name_ABS_Object).upper()

        row_object["MDR Phase"] = row.MDR_Phase

        # row_object[""] = row.Title
        list_objects.append(row_object)

    print "getIFS_XSD_Fields('{}') | Count = {} ".format("Mapping_IFS_XSD",len(list_objects))

    return list_objects

def processABS_XSD_Fields():

    output_csv_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"

    columns_objects_csv = ["Entity Name", "Attribute Name"]

    #columns_mappings_abs_csv = ["Target Entity Name", "Target Attribute Name", "Target Entity Name ABS","Target Attribute Name ABS"]

    rows = getABS_XSD_FieldsFromSharepoint()
    df = pd.DataFrame(rows, columns=columns_objects_csv)
    df.sort_values(by=["Entity Name","Attribute Name"],inplace=True)
    df.to_excel(output_csv_folder_path + "ABS_Fields.xlsx",header=True, index=None)
    return df

def processXSDAttribute(input_str):
    #print "\t\t Original Attribute Name: "+ input_str

    if (input_str[-1] == '/'):
	    input_str = input_str[:-1]

    pattern = re.compile(r'\s+')
    input_str = re.sub(pattern, '', input_str)

    if(re.match(r'.*(/val)$', input_str,re.IGNORECASE) ):
		input_str = input_str[:-4]
    if(re.match(r'.*(/key)$', input_str,re.IGNORECASE) ):
		input_str = input_str[:-4]
    if(re.match(r'.*(/annot/ctx/id)$',input_str,re.IGNORECASE)):
        input_str = input_str[:-13]
    output_str =  (input_str.split('/'))[-1]
    #print "\t\t\t Extracted Attribute Name: " + output_str
    return output_str

def getLastElement(input_string):
    output_string = input_string
    print "Input =",input_string


    print "Output=",output_string
    return output_string


def processIFS_XSD_Fields():

    output_csv_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"

    columns_objects_csv = ["Target Entity Name", "Target Attribute Name","Target Entity Name ABS", "Target Attribute Name ABS","MDR Phase"]

    #columns_mappings_abs_csv = ["Target Entity Name", "Target Attribute Name", "Target Entity Name ABS","Target Attribute Name ABS"]

    rows = getIFS_XSD_FieldsFromSharepoint()
    df = pd.DataFrame(rows, columns=columns_objects_csv)
    df = df[((df["Target Entity Name"]) <> '') & ( (df["Target Attribute Name"]) <> '')]
    df.sort_values(by=["Target Entity Name","Target Attribute Name"],inplace=True)
    df.insert(1, "Target Entity Name With XSD", (df["Target Entity Name"] + ".XSD"))
    df.insert(3, "Target Attribute Name Last", "")

    df = df.reset_index();  # df is a dataframe

    for i in range(0, len(df)):
        #print "For", df.loc[i, 'Target Attribute Name']
        if((df.loc[i, 'Target Attribute Name']) <> ''):
            df.loc[i, "Target Attribute Name Last"] = processXSDAttribute(df.loc[i, "Target Attribute Name"])
            #print "If", df.loc[i, 'Target Attribute Name']
            #df.loc[i,"Target Attribute Name Last"] = getLastElement(str(df.loc[i,"Target Attribute Name"]))


    df.to_excel(output_csv_folder_path + "XSD_Fields.xlsx",header=True, index=None)
    return df

def processMatching(join_how,include_fuzzy_columns):

    output_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
    output_filename = "XSD_Matching.xlsx"
    required_columns_level_all = ["Target Entity Name","Target Entity Name With XSD", "Target Attribute Name","Target Attribute Name Last", "Target Entity Name ABS","Target Attribute Name ABS","MDR Phase"]
    required_columns_level_1 = ["Target Entity Name","Target Entity Name With XSD", "Target Attribute Name", "Target Entity Name ABS","Target Attribute Name ABS"]
    required_columns_level_2 = ["Target Entity Name", "Target Entity Name With XSD", "Target Attribute Name",
                        "Target Attribute Name Last", "Target Entity Name ABS", "Target Attribute Name ABS"]

    merge_left_by_level_1 = ["Target Entity Name With XSD", "Target Attribute Name"]
    merge_left_by_level_2 = ["Target Entity Name With XSD", "Target Attribute Name Last"]

    merge_right_by = ["Entity Name", "Attribute Name"]

    ifs_xsd_fields = processIFS_XSD_Fields()
    abs_xsd_fields = processABS_XSD_Fields()
    ifs_xsd_fields_unique = ifs_xsd_fields

    #Straight Join Entity Name Attribute - Both Match
    merged_df_level_1 = pd.merge(left=ifs_xsd_fields,right=abs_xsd_fields,left_on=merge_left_by_level_1,right_on=merge_right_by,how=join_how,sort=True)
    merged_df_level_1 = merged_df_level_1[merged_df_level_1["Target Attribute Name ABS"] == ""]

    # Modified Attribute Name (Last part) Join - Both Match
    merged_df_level_2 = pd.merge(left=ifs_xsd_fields, right=abs_xsd_fields, left_on=merge_left_by_level_2,right_on=merge_right_by, how=join_how, sort=True)
    merged_df_level_2 = merged_df_level_2[merged_df_level_2["Target Attribute Name ABS"] == ""]

    merged = pd.concat([merged_df_level_1,merged_df_level_2])

    merged.drop_duplicates(subset=["Target Entity Name","Target Attribute Name"],keep=False,inplace=True)


    writer = pd.ExcelWriter(output_folder_path + output_filename)

    df_ifs_xsd_unique = pd.DataFrame(ifs_xsd_fields_unique, columns=required_columns_level_1)
    df_ifs_xsd_unique.drop_duplicates(subset=["Target Entity Name","Target Attribute Name"],inplace=True,keep='first')
    print "Unique Entities"
    df_ifs_xsd_unique.to_excel(writer, sheet_name="IFS Unique XSD Fields", columns=required_columns_level_1, index=False)

    #Sheet 1
    merged_df_level_1.to_excel(writer, sheet_name="Entity_Name.XSD", columns=required_columns_level_1, index=False)
    # Sheet 2
    merged_df_level_2.to_excel(writer, sheet_name="Attribute_Name_Last_Element", columns=required_columns_level_2, index=False)

    ################### Entity Counts##############################
    print "Processing Entity Counts"
    stats_list = []
    #merged_df_level_1,merged_df_level_2
    merged_no_match = pd.concat([ifs_xsd_fields])
    merged_no_match.drop_duplicates(subset=["Target Entity Name", "Target Attribute Name"], keep='first', inplace=True)
    merged_no_match.to_excel(writer, sheet_name="XSD_Fields_All", columns=required_columns_level_all,index=False)
    xsd_fields_all = len(merged_no_match)
    stats_list.append(addRow('XSD Fields - All',xsd_fields_all))
    print "XSD Fields - All: {}".format(xsd_fields_all)

    merged_no_match_xsd_match = merged_no_match[((merged_no_match["Target Entity Name ABS"]) <> '') & ((merged_no_match["Target Attribute Name ABS"]) <> '')]
    merged_no_match_xsd_match.to_excel(writer, sheet_name="XSD_Fields_Match", columns=required_columns_level_all, index=False)
    xsd_fields_match = len(merged_no_match_xsd_match)
    stats_list.append(addRow('XSD Fields - Match', xsd_fields_match))
    print "XSD Fields - Match: {}".format(xsd_fields_match)

    merged_no_match = merged_no_match[((merged_no_match["Target Entity Name ABS"]) == '') | ((merged_no_match["Target Attribute Name ABS"]) == '')]
    merged_no_match.to_excel(writer, sheet_name="XSD_Fields_No_Match", columns=required_columns_level_all, index=False)
    xsd_fields_no_match = len(merged_no_match)
    xsd_fields_match_per = round(xsd_fields_match/xsd_fields_all,2)*100
    print "XSD Fields - No Match: {}".format(xsd_fields_no_match)
    print "Percentage Match {}%".format(xsd_fields_match_per)
    stats_list.append(addRow('XSD Fields - No Match', xsd_fields_no_match))
    stats_list.append(addRow('XSD Fields - Match Percentage', str(xsd_fields_match_per) + "%"))


    stats = pd.DataFrame(stats_list)
    stats.to_excel(writer, sheet_name="Stats",index=False)


    #ifs_xsd_fields.reset_index()

    ################### Entity Level Fuzzy Matching##############################
    #print "Processing Entity Fuzzy Matching"
    ifs_xsds = ifs_xsd_fields
    ifs_xsds.drop_duplicates(subset=["Target Entity Name With XSD"], keep='first', inplace=True)

    abs_xsds = abs_xsd_fields
    abs_xsds.drop_duplicates(subset=["Entity Name"], keep='first', inplace=True)

    xsd_merge = pd.merge(left=ifs_xsds, right=abs_xsds, left_on=["Target Entity Name With XSD"],
                         right_on=["Entity Name"], how='outer',sort=True)

    # Text Match Percentage
    P1 = 88
    P2 = 90
    P3 = 95

    xsd_merge.insert(2,"FuzzyWuzzy_"+str(P1), "")
    xsd_merge.insert(3,"FuzzyWuzzy_"+str(P2), "")
    xsd_merge.insert(4,"FuzzyWuzzy_"+str(P3), "")

    if(include_fuzzy_columns):
        print "\t\t Doing XSD Entity Matching [IFS vs ABS] - Using Fuzzing Logic: {}%, {}%, {}% thresholds".format(P1,P2,P2)
        xsd_merge["FuzzyWuzzy_"+str(P1)] = xsd_merge.apply(getMatchingXSD_By_MatchPercent,axis=1,p=P1,input_column_name="Target Entity Name With XSD",lookup_field_type="E")
        xsd_merge["FuzzyWuzzy_"+str(P2)] = xsd_merge.apply(getMatchingXSD_By_MatchPercent, axis=1,p=P2,input_column_name="Target Entity Name With XSD",lookup_field_type="E")
        xsd_merge["FuzzyWuzzy_"+str(P3)] = xsd_merge.apply(getMatchingXSD_By_MatchPercent, axis=1, p=P3,input_column_name="Target Entity Name With XSD",lookup_field_type="E")

    # #xsd_merge["FuzzyWuzzy_3"] = map(getMatchingXSD_By_MatchPercentage,xsd_merge["Target Entity Name With XSD"])

    xsd_merge = xsd_merge[xsd_merge["FuzzyWuzzy_"+str(P1)] <> 'Exact Match']
    xsd_merge.rename(columns={"Target Entity Name With XSD": "IFS_XSD_NAME","Entity Name": "Avaloq_XSD_NAME"}, inplace=True)
    xsd_merge.to_excel(writer, sheet_name="XSD Match", columns=["IFS_XSD_NAME","Avaloq_XSD_NAME","FuzzyWuzzy_"+str(P1),"FuzzyWuzzy_"+str(P2),"FuzzyWuzzy_"+str(P3)], index=False)

    #############Attribute Level Fuzzy Matching##########################
    #print "Processing Attributes Fuzzy Matching"
    ifs_xsd_attributes = processIFS_XSD_Fields()
    ifs_xsd_attributes.drop_duplicates(subset=["Target Entity Name With XSD","Target Attribute Name"], keep='first', inplace=True)
    # ifs_xsd_attributes.info()

    abs_xsd_attributes = processABS_XSD_Fields()
    abs_xsd_attributes.drop_duplicates(subset=["Entity Name","Attribute Name"], keep='first', inplace=True)
    # abs_xsd_attributes.info()

    xsd_merge_attributes = pd.merge(left=ifs_xsd_attributes, right=abs_xsd_attributes, left_on=["Target Entity Name With XSD","Target Attribute Name"],
                         right_on=["Entity Name","Attribute Name"], how='left', sort=True)

    # xsd_merge_attributes.info()

    xsd_merge_attributes.insert(2,"FuzzyWuzzy_"+str(P1), "")
    xsd_merge_attributes.insert(3,"FuzzyWuzzy_"+str(P2), "")
    xsd_merge_attributes.insert(4,"FuzzyWuzzy_"+str(P3), "")

    if (include_fuzzy_columns):
        print "\t\t Doing XSD Attribute Matching [IFS vs ABS] - Using Fuzzing Logic: {}%, {}%, {}% thresholds".format(P1,P2,P2)
        xsd_merge_attributes["FuzzyWuzzy_"+str(P1)] = xsd_merge_attributes.apply(getMatchingXSD_By_MatchPercent, axis=1,p=P1,input_column_name="Target Attribute Name",lookup_field_type="A")
        xsd_merge_attributes["FuzzyWuzzy_"+str(P2)] = xsd_merge_attributes.apply(getMatchingXSD_By_MatchPercent, axis=1,p=P2,input_column_name="Target Attribute Name Last",lookup_field_type="A")
        xsd_merge_attributes["FuzzyWuzzy_"+str(P3)] = xsd_merge_attributes.apply(getMatchingXSD_By_MatchPercent, axis=1,p=P3,input_column_name="Target Attribute Name Last",lookup_field_type="A")

    xsd_merge_attributes.rename(columns={"Target Entity Name With XSD": "IFS_XSD_NAME", "Entity Name": "Avaloq_XSD_NAME"},inplace=True)

    xsd_merge_attributes.to_excel(writer, sheet_name="XSD Attribute Match",
                       columns=["IFS_XSD_NAME","Target Attribute Name","Target Attribute Name Last", "Avaloq_XSD_NAME","Attribute Name", "FuzzyWuzzy_" + str(P1), "FuzzyWuzzy_" + str(P2),
                                "FuzzyWuzzy_" + str(P3)], index=False)

    writer.save()

def read_CSV(input_path,input_file,input_req_cols):


    if (checkFileName(input_path + input_file)):
        print "\n Excel File '{}' located".format(input_filename)
        print "\n Reading CSV file {}, please wait.....\n".format(input_path+input_file,)

        df = pd.read_csv(input_path + input_file, sep=",",usecols=input_req_cols)
        df.sort_values(by=input_req_cols, inplace=True, na_position='first')
        print df.head()


        return df



def getEntityNameByAttribute():
    '''
    Get the Entity Name for the given list of Attribute Name (where the Entities are incorrectly tagged).
    Pre-Condition: T_E_A - file exist - generated by the MetadataExtractor process.
    Left Side: List of Attributes (from T_E_A)
    Right: List of ABS XSD Fields
    :return:
    '''
    output_csv_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
    output_filename = "ABS_EntityName_T_E_A_Correct.xlsx"
    output_filename_Join = "ABS_EntityName_T_E_A_Correct_Join.xlsx"
    input_csv_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
    input_filename = "Mapping_Fields_Missing_T_E_A.csv"

    input_filename_2 = "Objects_xsd_from_abs_phases_all.csv"

    required_columns_left  = ["Target Entity Name", "Target Attribute Name"]
    required_columns_right = ["Entity Name", "Attribute Name"]

    writer = pd.ExcelWriter(output_csv_folder_path + output_filename)

    #Left

    # get the data from the latest report
    if (checkFileName(input_csv_folder_path + input_filename)):
        print "\n Excel File '{}' located".format(input_filename)
        print "\n Generating CSV file, please wait.....\n"

        createFolderPath(output_csv_folder_path)
        createFolderPath(input_csv_folder_path)

        df_left = pd.read_csv(input_csv_folder_path + input_filename, sep=",",usecols=required_columns_left)

        # ignore the rows with blank Entity Name
        #df_left = df_left[df_left["Target Entity Name"].notnull()]

        # df = pd.read_excel('./data/input/raw/'+input_excel_filename,sheetname="export0",index_col=None)
        df_left["Target Entity Name"]    = str(df_left["Target Entity Name"]).upper()
        df_left["Target Attribute Name"] = df_left["Target Attribute Name"].str.upper()



        #df_left.rename(columns={"LDM Object": "Entity Name", "LDM Field": "Attribute Name", "LDM Text": "Description"},inplace=True)

        print "Target E A :", df_left.info()
        print df_left.head()
        df_left.sort_values(by=["Target Attribute Name"], inplace=True, na_position='first',ascending=[True])


        df_left.to_excel(writer, sheet_name="Latest Report", index=False, columns=required_columns_left)

    #Right
    df_right = read_CSV(input_csv_folder_path,input_filename_2,required_columns_right)

    #Merge

    df_merge = pd.merge(left=df_left, right=df_right,left_on=["Target Attribute Name"],right_on=["Attribute Name"], how='left', sort=True)
    df_merge.info()

    df_merge.to_excel(writer, sheet_name="Join", index=False)

    print "getEntityNameByAttribute()"







# getABS_XSD_FieldsFromSharepoint()
# getIFS_XSD_FieldsFromSharepoint()

#getSeries(csv_folder_path_Avaloq+input_filename,"Flat Layout","Source Name",csv_folder_path_Avaloq+output_filename)

#getXSDFields_FromAvaloReport_Delta()

# processABS_XSD_Fields()
# processIFS_XSD_Fields()

#graphviz
graphviz_output_folder = 'c:/apps/apps/graphviz/output/'
graphviz = GraphvizOutput()
graphviz.output_file = graphviz_output_folder+'XSD_Fields_Matching.png'
config = Config()
config.max_depth = 10
config.trace_filter = GlobbingFilter(exclude=[
    'pycallgraph.*',
    'foo',
])

#pr = cProfile.Profile()
start = time.time()
localtime_start = time.asctime(time.localtime(start))
localtime_end = time.asctime(time.localtime(start+1200))
print "Start time: {}".format(localtime_start)
print "ETA: 20 mins i.e. {} ".format(localtime_end)
#pr.enable()
#with PyCallGraph(output=graphviz,config=None):

processMatching('inner',False)
getEntityNameByAttribute()
#processMatching('inner',False)
#getXSDFields_FromAvaloReport_Delta()
#pr.disable()

end = time.time()
print "Execution time: {} mins".format((end - start)/60)

#print "cProfile Stats"
#pr.print_stats(sort="calls")
#getLastElement('repayment_frequency')
# processXSDAttribute('repayment_frequency/key')
# processXSDAttribute('repayment_frequency/val')
# processXSDAttribute('/data')
# processXSDAttribute('/data')
# processXSDAttribute('/data/adhoc_fee')
# processXSDAttribute('/data/adhoc_fee/book_kind_list')

#columnValuesWithXSD()
# getMatchingXSD('BTFG$UI_SCD_TRX_LIST.POS_TRX.XSD')
# getMatchingXSD('BTFG$UI_SCD_TRX_LIST.POS_TRX')
# getMatchingXSD('BTFG$UI_SCD_TRX_LIST')