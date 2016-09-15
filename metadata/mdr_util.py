#encoding=utf8
from __future__ import division
import pandas as pd
import difflib as diff
import Levenshtein as L
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
"""
List of functions:
------------------
createFolder(folder_path,folder_name,flag_timestamp)
    #Usage:
    #createFolder('C:\TEST\\', 'Ragha', 'True')
    #createFolder('C:\TEST\\', 'Ragha', 'False')

createExcelSheet(output_excel_folder_path,output_excel_file_name,worksheet_name,headerElements)
setHeaderRow(workbook,worksheet,headerElements)

insertRows_Objects(worksheet,row_position,rows)
insertRows_Mappings(worksheet,row_position,rows)

sharepointListRows(site_url,list_name,username,password)
displayRowFields(site_url,listname,username,password)

cleanHTMLTags(input_string)
cleanDescription(input_string)

"""

def createExcelSheet(output_excel_folder_path,output_excel_file_name,worksheet_name,headerElements):
    # Excel sheet details: Excel Folder Path, File Name, Worksheet Name

    import xlsxwriter

    workbook = xlsxwriter.Workbook(output_excel_folder_path+output_excel_file_name)
    worksheet = workbook.add_worksheet(worksheet_name)

    return worksheet

def createFolder(folder_path,folder_name,flag_timestamp):

    import os
    import datetime

    #Usage:
    #createFolder('C:\TEST\\', 'Ragha', 'True')
    #createFolder('C:\TEST\\', 'Ragha', 'False')

    #date and time - time stamp
    if (flag_timestamp == 'True'):
        #Timestamp Format is YYYYMMDD_HHMMSS
        dt_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        mdr_dir = folder_path + folder_name + '_' + dt_timestamp
    else:
        dt_timestamp = ''
        mdr_dir = folder_path + folder_name + dt_timestamp

    try:
        os.makedirs(mdr_dir)

    except IOError:
        print "ERROR: Unable to create the folder " + mdr_dir

def createFolderPath(folder_path):

    import os
    #Usage:
    #createFolderPath('C:\TEST\\')

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except IOError:
        print "ERROR: Unable to create the folder " + folder_path


def json_sharepointListRowsByListName(list_name):
    from flask import jsonify
    import json
    Screen_Rows = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        screen_object = {}

        screen_object['Functionality']      = row.Functionality
        screen_object['Entity_x0020_Name']  = row.Entity_x0020_Name
        screen_object['MDR_x0020_Release']  = row.MDR_x0020_Release
        screen_object['Harvest_Status']     = row.Harvest_Status


        screen_object['Onboarding']         = processYesNo(row.Onboarding)
        screen_object['Direct']             = processYesNo(row.Direct_x0020_Investor)
        screen_object['ASIM']               = processYesNo(row.ASIM)

        #print row.MDR_x0020_Scope
        if(str(row.MDR_x0020_Scope) == 'True'):
            #print "MDR Scope = Yes, so added to json list",row.Entity_x0020_Name
            Screen_Rows.append(screen_object)

    #s1 = Screen("Payments","Make a payment","Phase 1")
    #s2 = Screen("Payments", "Make a payment", "Phase 1")
    #s3 = Screen("Payments", "Make a payment", "Phase 1")

    #s1 = {'functionality' : 'Mercury', 'screen_name': 0.4,'phase' : 0.055}
    #s2 = {'functionality':  'Jupiter', 'screen_name': 0.4, 'phase': 0.055}
    #s3 = {'functionality': 'Earth',    'screen_name': 0.4, 'phase': 0.055}
    #s4 = {}
    #s4['functionality'] = 'Pluto'

    #Screen_Rows.append(s1)
    #Screen_Rows.append(s2)
    #Screen_Rows.append(s3)
    #Screen_Rows.append(s4)

    return json.dumps(Screen_Rows)
    #return "Hello World, Ragha"



def sharepointListRowsByListName(list_name):

    import urllib2

    from sharepoint import SharePointSite
    from ntlm import HTTPNtlmAuthHandler

    site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"
    username = getUsername()
    password = getPassword()

    # an opener for the NTLM authentication
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, site_url, username, password)
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

    try:
        # create and install the sharepoint site opener
        opener = urllib2.build_opener(auth_NTLM)
        urllib2.install_opener(opener)

        # create a SharePointSite object
        site = SharePointSite(site_url, opener)
        sp_list = site.lists[list_name]
        return sp_list.rows

    except:
        print "ERROR in fetching data from sharepoint. Check Username and Password"
        exit()

def sharepointListRows(site_url,list_name,username,password):

    import urllib2
    from sharepoint import SharePointSite
    from ntlm import HTTPNtlmAuthHandler

    # an opener for the NTLM authentication
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, site_url, username, password)
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

    try:
        # create and install the sharepoint site opener
        opener = urllib2.build_opener(auth_NTLM)
        urllib2.install_opener(opener)

        # create a SharePointSite object
        site = SharePointSite(site_url, opener)
        sp_list = site.lists[list_name]
        return sp_list.rows

    except:
        print "ERROR in fetching data from sharepoint. Check Username and Password"
        exit()

def sharepointListRowsbyOpener(site_url,list_name,opener):

    import urllib2
    from sharepoint import SharePointSite
    from ntlm import HTTPNtlmAuthHandler

    # an opener for the NTLM authentication
    #passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    #passman.add_password(None, site_url, username, password)
    #auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

    try:
        # create and install the sharepoint site opener
        #opener = urllib2.build_opener(auth_NTLM)
        urllib2.install_opener(opener)

        # create a SharePointSite object
        site = SharePointSite(site_url, opener)
        sp_list = site.lists[list_name]
        return sp_list.rows

    except:
        print "ERROR in fetching data from sharepoint. Check Username and Password"
        exit()


def displayRowFields(site_url,listname,username,password):

    rows = sharepointListRows(site_url,listname,username,password)
    row_dict = rows[0].fields

    #print "Entity Name: ", rows[0].Entity_Name, ' | ' , "Entity Name Duplicate: ", rows[0].Entity_Name_Duplicate

    #print len(row_dict.keys())
    #print len(rows[0].fields)
    """
    count = 0
    for i in range(0,len(row_dict.keys())):
        print (row_dict.keys())[i]
        count = count + 1
    print "Total Fields Count : ", count

    """
    count = 0
    for keys, values in row_dict.items():
        print "Key: ",keys,",", "Value: ",values
        count = count + 1
    print "Total Fields Count : ", count


    """
    for row in sharepointListRows('','','Username','Password')  :
        if (row.id == 1):
            print row.fields
    """


def setHeaderRow(workbook,worksheet,headerElements):

    bold = workbook.add_format({'bold': 1});
    for key,value in headerElements.items():
        #worksheet.write('A1', 'Screen Name', bold)
        worksheet.write(key, value, bold);
"""
def setHeaderRow(worksheet,headerElements):
    print
    #bold = workbook.add_format({'bold': 1});
    #for key,value in headerElements.items():
        #worksheet.write('A1', 'Screen Name', bold)
        #worksheet.write(key, value, bold);
"""

def cleanHTMLTags(input_string):

    reload(sys)
    sys.setdefaultencoding('utf8')

    import re
    # strip the leading and trailing spaces / whitespaces
    #input_string = "<div><df><strong><font face=Calibri size=\"10' if=yu>Hi</font></strong></div>"
    output_string = input_string.strip()

    pattern = re.compile(r'</?\w+(\s+[a-zA-Z0-9=\'\"]+){0,20}(\s+)?>')
    output_string = pattern.sub('', output_string)

    output_string = output_string.replace('<font face=Calibri size=2 style=\"background-color:#FDE9D9\">',"")
    output_string = output_string.replace('<font face=Calibri size=2 style=\"background-color:#DBE5F1\">', "")
    output_string = output_string.replace('<font face=Calibri size=2 style=\"background-color:#DBEEF3\">', "")
    output_string = output_string.replace('<font face=Calibri size=2 style=\"background-color:#FFFF00\">', "")

    output_string = output_string.replace('&nbsp;', " ")
    output_string = output_string.replace(',', "|")
    output_string = output_string.replace("'", "")
    output_string = output_string.encode("utf-8").replace("’", " ")
    output_string = output_string.encode("utf-8").replace("‘", " ")
    output_string = output_string.encode("utf-8").replace("•", " ")
    output_string = output_string.encode("utf-8").replace("“", " ")
    output_string = output_string.encode("utf-8").replace("”", " ")
    output_string = output_string.encode("utf-8").replace("–", " ")



    #print output_string

    return output_string



def cleanDescription(input_string):
    import re

    # strip the leading and trailing spaces / whitespaces
    output_string = input_string.strip()

    pattern = re.compile(r'(<div>)|(</div>)|(<strong>)|(</strong>)|(<font face=Calibri size=.>)|(</font>)')

    """
    pattern1 = re.compile(r'<div>')
    pattern2 = re.compile(r'</font>')
    pattern3 = re.compile(r'</div>')
    pattern4 = re.compile(r'<font face=Calibri size=2>')
    pattern5 = re.compile(r'<font face=Calibri size=3>')
    pattern6 = re.compile(r'<div align=center>')
    pattern7 = re.compile(r'(<strong>)|(</strong>)')
    #pattern8 = re.compile(r'</strong>')

    output_string = pattern1.sub('', output_string)
    output_string = pattern2.sub('', output_string)
    output_string = pattern3.sub('', output_string)
    output_string = pattern4.sub('', output_string)
    output_string = pattern5.sub('', output_string)
    output_string = pattern6.sub('', output_string)
    output_string = pattern7.sub('', output_string)
    #output_string = pattern8.sub('', output_string)
    """
    output_string = pattern.sub('', output_string)

    return output_string


def insertRows_Objects(worksheet,row_position,rows):

    for row in rows:
        worksheet.write_string(row_position, 0, row.System_Name)
        worksheet.write_string(row_position, 1, row.Instance_Name)
        worksheet.write_string(row_position, 2, row.Entity_Name_Duplicate)
        worksheet.write_string(row_position, 3, row.Attribute_Name)
        worksheet.write_string(row_position, 4, row.Owner)
        worksheet.write_string(row_position, 5, row.Parent)
        worksheet.write_string(row_position, 6, row.Entity_Type)
        worksheet.write_string(row_position, 7, cleanDescription(row.Description))
        worksheet.write_string(row_position, 8, cleanDescription(row.URL))
        worksheet.write_string(row_position, 9, cleanDescription(row.XPATH))
        worksheet.write_string(row_position, 10, row.MDR_Phase)

        row_position = row_position + 1

def getUsername():
    return "L083646"

def getPassword():
    import base64
    return base64.b64decode("VENTIzIzMDU=")


def insertRows_Mappings(worksheet,row_position,rows):

    for row in rows:
        worksheet.write_string(row_position, 0, row.Source_System_Name)
        worksheet.write_string(row_position, 1, row.Title)
        #lookup fields
        worksheet.write_string(row_position, 2, row.Source_Entity_Name_Duplicate)
        worksheet.write_string(row_position, 3, row.Source_Attribute_Name_Duplicate)

        worksheet.write_string(row_position, 4, row.Target_System_Name)
        worksheet.write_string(row_position, 5, row.Target_Instance_Name)

        # lookup fields
        worksheet.write_string(row_position, 6, row.Target_Entity_Name_Duplicate)
        worksheet.write_string(row_position, 7, row.Target_Attribute_Name_Duplicate)

        worksheet.write_string(row_position, 8, cleanDescription(row.Attribute_x0020_Description))
        worksheet.write_string(row_position, 9, cleanDescription(row.Business_x0020_Rule))
        worksheet.write_string(row_position, 10, row.Transformation_Mapping_Rule)
        worksheet.write_string(row_position, 11, row.Comments)
        worksheet.write_string(row_position, 12, row.Mapping_x0020_Name)
        worksheet.write_string(row_position, 13, row.Action)
        worksheet.write_string(row_position, 14, str(row.Last_Update_Date))
        worksheet.write_string(row_position, 15, row.Modified_By)
        worksheet.write_string(row_position, 16, row.MDR_Phase)

        row_position = row_position + 1



def UniqueListItems(seq):
   # Not order preserving
   keys = {}
   for e in seq:
       keys[e] = 1
   return keys.keys()

# get the list of unique items in a given column (i.e. attribute name)
def UniqueListItemsByListName_AttributeName(list_name,attribute_name):
   # Not order preserving
   keys = {}
   rows = sharepointListRowsByListName(list_name)
   for row in rows:
       #get attribute by the attribute name
       keys[getattr(row,attribute_name)] = 1
   return keys.keys()

def getAttributesbyEntity(list_name,entity_name):

    list_attributes = []

    #get the rows
    rows = sharepointListRowsByListName(list_name)
    #print "Row Count", len(rows)
    #print "entity_name: ", entity_name

    # get the attributes for the given entity name
    for row in rows:

         #print "Entity Name: ", row.Entity_Name_D
        # Use duplicate entity name (as the actual is a lookup field
        if(row.Entity_Name_D == (entity_name).strip()):
            #print "Match Found"
            #list_attributes.append(row.Attribute_Name)
            list_attributes.append(row)

    return list_attributes


def displayLineage(screen_entity_name,screen_attribute_name):
   print "--------------------Metadata Lineage-------------------"
   print "Screen Name:",screen_entity_name.upper()
   print "Field Name:",screen_attribute_name.upper()

   mapping_screen_vm = "Mapping_Screen_VisualMap"
   mapping_vm_ifs    = "Mapping_VisualMap_IFS"
   mapping_ifs_xsd   = "Mapping_IFS_XSD"

   rows_ux_vm = sharepointListRowsByListName(mapping_screen_vm)
   rows_vm_ifs = sharepointListRowsByListName(mapping_vm_ifs)
   rows_ifs_xsd = sharepointListRowsByListName(mapping_ifs_xsd)

    #Source_Entity_Name_D
    #Source_Attribute_Name0

   for row_ux_vm in rows_ux_vm:
    #get attribute by the attribute name
    if((row_ux_vm.Source_Entity_Name_D.upper() == screen_entity_name.upper()) & (row_ux_vm.Source_Attribute_Name0.upper() == screen_attribute_name.upper())):
        print "\t Visual Map Entity Name:",row_ux_vm.Target_Entity_Name_D.upper()
        print "\t Visual Map Attribute Name:", row_ux_vm.Target_Attribute_Name_D.upper()
        for row_vm_ifs in rows_vm_ifs:
            if (( row_vm_ifs.Source_Entity_Name_D.upper() == row_ux_vm.Target_Entity_Name_D.upper() ) & (row_vm_ifs.Source_Attribute_Name_Duplicate.upper() == row_ux_vm.Target_Attribute_Name_D.upper()) ):
                print "\t\t IFS Entity Name:", row_vm_ifs.Target_Entity_Name_D.upper()
                print "\t\t IFS Attribute Name:", row_vm_ifs.Target_Attribute_Name_Duplicate.upper()
                for row_ifs_xsd in rows_ifs_xsd:
                    if((row_ifs_xsd.Source_Entity_Name_Duplicate.upper() == row_vm_ifs.Target_Entity_Name_D.upper()) & (row_ifs_xsd.Source_Attribute_Name_Duplicate.upper() == row_vm_ifs.Target_Attribute_Name_Duplicate.upper() ) ):
                        print "\t\t\t XSD Entity Name: ", row_ifs_xsd.Target_Entity_Name_Duplicate.upper()
                        print "\t\t\t XSD Attribute Name: ", row_ifs_xsd.Target_Attribute_Name_Duplicate.upper()


def displayLineageByScreenEntityName(screen_entity_name):

    mapping_screen_vm = "Mapping_Screen_VisualMap"
    rows_ux_vm = sharepointListRowsByListName(mapping_screen_vm)

    for row_ux_vm in rows_ux_vm:
        if( (row_ux_vm.Source_Entity_Name_D.upper() == screen_entity_name.upper() ) ):
            print row_ux_vm.Source_Entity_Name_D.upper() ," : ",row_ux_vm.Source_Attribute_Name0.upper()
            displayLineage(row_ux_vm.Source_Entity_Name_D,row_ux_vm.Source_Attribute_Name0)

def getMDRLineageRowsFromCSV(entity_name,attribute_name):
    #lineage_object = []
    #from csv file

    input_excel_folder_path_phase2 = "C:\MDR\Data\Repository\CSV_Sharepoint_Output"
    input_excel_filename_phase2_object = "\Objects.csv"
    input_excel_filename_phase2_mappings = "\Mappings.csv"

    #df_phase2_objects = pd.read_csv(input_excel_folder_path_phase2 + input_excel_filename_phase2_object, sep=",")
    df_phase2_mappings = pd.read_csv(input_excel_folder_path_phase2 + input_excel_filename_phase2_mappings, sep=",")
    #print df_phase2_mappings.info()

    df_phase2_mappings = df_phase2_mappings[(df_phase2_mappings["Source Entity Name"] == entity_name) & (df_phase2_mappings["Source Attribute Name"] == attribute_name)]

    #print df_phase2_mappings.info()
    #dict key with values = []
    df_dict_list =  df_phase2_mappings.to_dict(orient='list')
    #print df_dict_list
    # for i in range(0,len(df_dict_list["Target Attribute Name"])):
    #     print df_dict_list["Target System Name"][i],"|",df_dict_list["Target Entity Name"][i],"|",df_dict_list["Target Attribute Name"][i],"|",df_dict_list["Business Rule"][i],"|",df_dict_list["Transformation_Mapping rule"][i]

    return df_dict_list

def getObjectsFromCSV(system_name,entity_name,attribute_name,entity_type):

    input_excel_folder_path_phase2 = "C:\MDR\Data\Repository\CSV_Sharepoint_Output"
    input_excel_filename_phase2_object = "\Objects.csv"

    df_phase2_objects = pd.read_csv(input_excel_folder_path_phase2 + input_excel_filename_phase2_object, sep=",")

    #print df_phase2_objects.info()

    #System_Name , Entity Type
    if((system_name <> '') & (entity_name == '')):
        df_phase2_objects = df_phase2_objects[(df_phase2_objects["System Name"] == system_name) & (df_phase2_objects["Type"] == entity_type)]

    # Entity and Attribute
    if((entity_name <> "") & (attribute_name <> "")):
        df_phase2_objects = df_phase2_objects[(df_phase2_objects["Entity Name"] == entity_name) & (df_phase2_objects["Attribute Name"] == attribute_name)]

    #Entity Name, Entity Type
    if((entity_name <> '') & (attribute_name == "")):
        df_phase2_objects = df_phase2_objects[(df_phase2_objects["Entity Name"] == entity_name) & (df_phase2_objects["Type"] == entity_type)]
        #df_phase2_objects = df_phase2_objects[(df_phase2_objects["Entity Name"] == entity_name) & (df_phase2_objects["Type"] == "UI Field")]

    #print df_phase2_mappings.info()
    #dict key with values = []
    df_dict_list =  df_phase2_objects.to_dict(orient='list')
    #print df_dict_list
    for i in range(0,len(df_dict_list["Attribute Name"])):
         print df_dict_list["System Name"][i],"|",df_dict_list["Entity Name"][i],"|",df_dict_list["Attribute Name"][i]

    return df_dict_list

def getTargetAttributesBySourceAttributes(list_dict_item,system_name):
    #print len(dict_item)

    lineage_mappings = []
    ''''''

    #print item
    #print "[",item["Source System Name"],"|",item["Source Entity Name"],"|",item["Source Attribute Name"],"],[",item["Target System Name"],"|",item["Target Entity Name"],"|",item["Target Attribute Name"],"]"
    for item in list_dict_item:
        #print "Count: Target Attribute Name= ",len(item["Target Attribute Name"])
        for j in range(0,len(item["Target Attribute Name"])):
            if(system_name.upper() == "UX Sitemap".upper()):
                print "[",item["Target System Name"][j],"|",item["Target Entity Name"][j],"|",item["Target Attribute Name"][j],"]"
            else:
                print "[", item["Source System Name"][j], "|", item["Source Entity Name"][j], "|", item["Source Attribute Name"][j], "],[", item["Target System Name"][j], "|", item["Target Entity Name"][j], "|", item["Target Attribute Name"][j], "]"

            lineage_mappings.append(getMDRLineageRowsFromCSV(item["Target Entity Name"][j],item["Target Attribute Name"][j]))
        ''''''
    return lineage_mappings

def printList(list):
    for item in list:
        for i in range(0,len(item["Target Attribute Name"])):
            print item["Source System Name"][i],"|",item["Source Entity Name"][i],"|",item["Source Attribute Name"][i],"|", item["Target System Name"][i],"|",item["Target Entity Name"][i],"|",item["Target Attribute Name"][i]

def getMDRLineageFromCSV(screen_entity_name,screen_attribute_name):
    #Final return
    lineage_object = []

    #lineage_object_vm  = [{"Target_System_Name":"Visual Map","Target_Entity_Name_Duplicate":"VM Name","Target_Attribute_Name_Duplicate":"VM Attribute Name","Business_Rule":"-","Transformation_Mapping_Rule":"-"}]
    #lineage_object_ifs = [{"Target_System_Name":"IFS","Target_Entity_Name_Duplicate":"IFS Name","Target_Attribute_Name_Duplicate":"IFS Attribute Name ","Business_Rule":"-","Transformation_Mapping_Rule":"-"}]
    #lineage_object_xsd = [{"Target_System_Name":"XSD","Target_Entity_Name_Duplicate":"XSD Name","Target_Attribute_Name_Duplicate":"XSD Attribute Name","Business_Rule":"-","Transformation_Mapping_Rule":"-"}]
    #lineage_object_ldm = [{"Target_System_Name":"ABS LDM", "Target_Entity_Name_Duplicate": "LDM Name","Target_Attribute_Name_Duplicate": "LDM Attribute Name", "Business_Rule": "TBC","Transformation_Mapping_Rule": "TBC"}]

    system_name_list = []
    system_name_list.append("UX Sitemap")

    entity_name_list = []
    entity_name_list.append(screen_entity_name)

    attribute_name_list = []
    attribute_name_list.append(screen_attribute_name)



    initial_dict = {"Target System Name":system_name_list,"Target Entity Name":entity_name_list,"Target Attribute Name":attribute_name_list}

    screen_objects_list = []
    screen_objects_list.append(initial_dict)

    #print initial_dict
    #print object_list

    #lineage_object_vm = getMDRLineageRowsFromCSV("Account - Overview", "Amount")
    lineage_object_ux  = getTargetAttributesBySourceAttributes(screen_objects_list, "UX Sitemap")
    lineage_object_vm  = getTargetAttributesBySourceAttributes(lineage_object_ux,   "Visual Map")
    lineage_object_ifs = getTargetAttributesBySourceAttributes(lineage_object_vm,   "IFS")
    lineage_object_xsd = getTargetAttributesBySourceAttributes(lineage_object_ifs,  "XSD")
    #lineage_object_ldm = getMDRLineageFromCSVByTargetSystem(lineage_object_xsd,  "LDM")


    # for i in range(0,len(lineage_object_vm["Target Attribute Name"])):
    #     print lineage_object_vm["Target System Name"][i],"|",lineage_object_vm["Target Entity Name"][i],"|",lineage_object_vm["Target Attribute Name"][i],"|",lineage_object_vm["Business Rule"][i],"|",lineage_object_vm["Transformation_Mapping rule"][i]

    #print lineage_object_vm
    '''
    for i in range(0,len(lineage_object_vm["Target Attribute Name"])):
        print "[",lineage_object_vm["Source System Name"][i],"|",lineage_object_vm["Source Entity Name"][i],"|",lineage_object_vm["Source Attribute Name"][i],"],[",lineage_object_vm["Target System Name"][i],"|",lineage_object_vm["Target Entity Name"][i],"|",lineage_object_vm["Target Attribute Name"][i],"]"
        lineage_object_ifs.append(getMDRLineageRowsFromCSV(lineage_object_vm["Target Entity Name"][i],lineage_object_vm["Target Attribute Name"][i]))

    print lineage_object_ifs

    for item in lineage_object_ifs:
        #print item
        #print "[",item["Source System Name"],"|",item["Source Entity Name"],"|",item["Source Attribute Name"],"],[",item["Target System Name"],"|",item["Target Entity Name"],"|",item["Target Attribute Name"],"]"
        for j in range(0,len(item["Target Attribute Name"])):
            print "[",item["Source System Name"][j],"|",item["Source Entity Name"][j],"|",item["Source Attribute Name"][j],"],[",item["Target System Name"][j],"|",item["Target Entity Name"][j],"|",item["Target Attribute Name"][j],"]"
            lineage_object_xsd.append(getMDRLineageRowsFromCSV(item["Target Entity Name"][j],item["Target Attribute Name"][j]))

    #print lineage_object_xsd

    for item in lineage_object_xsd:
        #print item
        #print "[",item["Source System Name"],"|",item["Source Entity Name"],"|",item["Source Attribute Name"],"],[",item["Target System Name"],"|",item["Target Entity Name"],"|",item["Target Attribute Name"],"]"
        for k in range(0,len(item["Target Attribute Name"])):
            print "[",item["Source System Name"][k],"|",item["Source Entity Name"][k],"|",item["Source Attribute Name"][k],"],[",item["Target System Name"][k],"|",item["Target Entity Name"][k],"|",item["Target Attribute Name"][k],"]"
            lineage_object_ldm.append(getMDRLineageRowsFromCSV(item["Target Entity Name"][k],item["Target Attribute Name"][k]))

    #print lineage_object_ldm

    for item in lineage_object_ldm:
        #print item
        #print "[",item["Source System Name"],"|",item["Source Entity Name"],"|",item["Source Attribute Name"],"],[",item["Target System Name"],"|",item["Target Entity Name"],"|",item["Target Attribute Name"],"]"
        for m in range(0,len(item["Target Attribute Name"])):
            print "[",item["Source System Name"][m],"|",item["Source Entity Name"][m],"|",item["Source Attribute Name"][m],"],[",item["Target System Name"][m],"|",item["Target Entity Name"][m],"|",item["Target Attribute Name"][m],"]"
            #lineage_object_ldm.append(getMDRLineageRowsFromCSV(item["Target Entity Name"][m],item["Target Attribute Name"][m]))

    '''
    lineage_object.append(lineage_object_vm)
    lineage_object.append(lineage_object_ifs)
    lineage_object.append(lineage_object_xsd)
    #lineage_object.append(lineage_object_ldm)

    print "---Lineage Object---"
    #print lineage_object
    for i in range(0,len(lineage_object)):
        printList(lineage_object[i])
        # printList(lineage_object[0])
        # printList(lineage_object[1])
        # printList(lineage_object[2])

    return lineage_object

def getMDRLineage(screen_entity_name,screen_attribute_name):

    lineage_object = []

    #lineage_object_vm = [{"Name":"VM_Name"},{"Name":"VM_Name"},{"Name":"VM_Name"}]
    #lineage_object_ifs = [{"Name":"IFS_Name"},{"Name":"VM_Name"},{"Name":"VM_Name"},{"Name":"VM_Name"}]
    #lineage_object_xsd = [{"Name":"XSD_Name"},{"Name":"VM_Name"},{"Name":"VM_Name"},{"Name":"VM_Name"},{"Name":"VM_Name"}]
    lineage_object_ldm = [{"Target_System_Name": "ABS LDM", "Target_Entity_Name_Duplicate": "TBC", "Target_Attribute_Name_Duplicate": "TBC", "Business_x0020_Rule": "TBC","Transformation_Mapping_Rule": "TBC"}]

    lineage_object_vm = []
    lineage_object_ifs = []
    lineage_object_xsd = []
    #lineage_object_ldm = []
    #lineage_object_ldm.append(lineage_object_ldm)

    mapping_screen_vm = "Mapping_Screen_VisualMap"
    mapping_vm_ifs = "Mapping_VisualMap_IFS"
    mapping_ifs_xsd = "Mapping_IFS_XSD"

    rows_ux_vm = sharepointListRowsByListName(mapping_screen_vm)
    rows_vm_ifs = sharepointListRowsByListName(mapping_vm_ifs)
    rows_ifs_xsd = sharepointListRowsByListName(mapping_ifs_xsd)

    # Source_Entity_Name_D
    # Source_Attribute_Name0

    for row_ux_vm in rows_ux_vm:
        # get attribute by the attribute name
        if ((row_ux_vm.Source_Entity_Name_D.upper() == screen_entity_name.upper()) & (
            row_ux_vm.Source_Attribute_Name0.upper() == screen_attribute_name.upper())):

            #print "\t Visual Map Entity Name:", row_ux_vm.Target_Entity_Name_D.upper()
            #print "\t Visual Map Attribute Name:", row_ux_vm.Target_Attribute_Name_D.upper()
            vm_object = {"Entity_Name":row_ux_vm.Target_Entity_Name_D.upper(),"Attribute":row_ux_vm.Target_Attribute_Name_D.upper(),"Remarks":"No Remarks"}

            lineage_object_vm.append(row_ux_vm)

            for row_vm_ifs in rows_vm_ifs:
                if ((row_vm_ifs.Source_Entity_Name_D.upper() == row_ux_vm.Target_Entity_Name_D.upper()) & (
                    row_vm_ifs.Source_Attribute_Name_Duplicate.upper() == row_ux_vm.Target_Attribute_Name_D.upper())):

                    #print "\t\t IFS Entity Name:", row_vm_ifs.Target_Entity_Name_D.upper()
                    #print "\t\t IFS Attribute Name:", row_vm_ifs.Target_Attribute_Name_Duplicate.upper()

                    ifs_object = {"Entity_Name": row_vm_ifs.Target_Entity_Name_D.upper(),
                                 "Attribute": row_vm_ifs.Target_Attribute_Name_Duplicate.upper(), "Remarks": "No Remarks"}

                    lineage_object_ifs.append(row_vm_ifs)

                    for row_ifs_xsd in rows_ifs_xsd:
                        if ((
                                row_ifs_xsd.Source_Entity_Name_Duplicate.upper() == row_vm_ifs.Target_Entity_Name_D.upper()) & (
                            row_ifs_xsd.Source_Attribute_Name_Duplicate.upper() == row_vm_ifs.Target_Attribute_Name_Duplicate.upper())):
                            #print "\t\t\t XSD Entity Name: ", row_ifs_xsd.Target_Entity_Name_Duplicate.upper()
                            #print "\t\t\t XSD Attribute Name: ", row_ifs_xsd.Target_Attribute_Name_Duplicate.upper()
                            xsd_object = {"Entity_Name": row_ifs_xsd.Target_Entity_Name_Duplicate.upper(),
                                         "Attribute": row_ifs_xsd.Target_Attribute_Name_Duplicate.upper(),
                                         "Remarks": "No Remarks"}
                            lineage_object_xsd.append(row_ifs_xsd)


    lineage_object.append(lineage_object_vm)
    lineage_object.append(lineage_object_ifs)
    lineage_object.append(lineage_object_xsd)
    lineage_object.append(lineage_object_ldm)

    return lineage_object

def list_screen_master_sort(list_item):
    return list_item.Functionality


def getScreenStatus():

    status_arrary = []
    status_arrary.append(getScreenStatusByPhase('Phase 1'))
    status_arrary.append(getScreenStatusByPhase('Phase 2'))

    return status_arrary


def getScreenStatusByPhase(phase):

    list_name = "Screen Master"
    rows = sharepointListRowsByListName(list_name)
    total = open = wip = review = completed = 0

    for row in rows:
        if(row.MDR_x0020_Release == phase):
            total = total + 1
            if ((row.Harvest_Status == 'Open') | (row.Harvest_Status == 'Not in Scope') |(row.Harvest_Status == 'Issue') ) : open = open + 1
            if (row.Harvest_Status == 'For Review'): review = review + 1
            if (row.Harvest_Status == 'Ready'): wip = wip + 1
            if (row.Harvest_Status == 'Completed'): completed = completed + 1

    # status = {"Total": "100", "Open": "20", "WIP": "30", "Completed": "40", "Review": "10", "Review_Percentage": "50","Open_Percentage": "20", "WIP_Percentage": "30", "Completed_Percentage": "40"}
    status = {}
    #total = total
    status["Total"] = total
    status["Open"] = open
    status["WIP"] = wip
    status["Review"] = review
    status["Completed"] = completed

    if(total==0): total = 1

    status["Open_Percentage"]       = int(round(open / total,2) * 100)
    status["WIP_Percentage"]        = int(round(wip / total,2) * 100)
    status["Review_Percentage"]     = int(round(review / total,2) * 100)
    status["Completed_Percentage"]  = int(round(completed / total,2) * 100)
    # print "----------------------------------"
    # print "Completed {},Total {}, Completed / Total {}".format(completed,total,completed / total)
    # print round(completed / total, 2)
    # print int(round(completed / total, 2) * 100)
    # print "Open  | Completed  ", open, completed
    # print "Open % | Completed % ",status["Open_Percentage"], status["Completed_Percentage"]
    # print total
    # print "----------------------------------"
    return status


class Screen:
    def __init__(self, functionality, entity_name, phase):
        self.Functionality = functionality
        self.Entity_Name = entity_name
        self.MDR_Project_Phase = phase

def processYesNo(input_value):
    output_string = "No"
    if(input_value == True):
        output_string = "Yes"
    else:
        output_string = "No"

    #print "Type is %s and Value is %s" % (type(input_value), output_string)
    #print "Type is {} and Value is {} ".format(type(input_value), output_string)

    return output_string

def checkFileName(filename):

    result_boolean = False
    #print "File Name: ", filename

    if os.path.exists(filename):
        result_boolean = True

    return result_boolean


def addMatchedString(algorithm, orphaned_string,matched_string,control_limit,score):

    output_dict = {}

    output_dict["Algorithm"] = algorithm
    output_dict["Orphaned_String"] = orphaned_string
    output_dict["Match_String"] = matched_string
    output_dict["Control_Limit"] = control_limit
    output_dict["Match_Percentage"] = score

    return output_dict

def SeqMatch(orphaned_string,list_of_strings,control_limit):
    output_list = []
    output_dict_list = []

    xsd_str = orphaned_string + ".XSD"
    #print "String with .XSD", xsd_str

    if(xsd_str in list_of_strings):
        print "Exact Match with .XSD suffix. Orphaned String {} | Matched String {}".format(orphaned_string, xsd_str)
        output_list.append(xsd_str)
        output_dict_list.append(addMatchedString("SequenceMatch", orphaned_string, xsd_str, control_limit, 1.0))
    else:

        for str in list_of_strings:
            # use the Sequence Matcher Ratio
            s = diff.SequenceMatcher(None, orphaned_string,str ).ratio()
            #print str, s
            if (s == 1.00):
                #print "score is 1.0"
                output_list.append(str)
                output_dict_list.append(addMatchedString("SequenceMatch", orphaned_string, str, control_limit, s))
                break
            else:
                if(s >= control_limit):

                    #print "The string '{}' has {} % match with the orphaned string '{}' ".format(str,s*100,orphaned_string)
                    output_list.append(str)
                    output_dict_list.append(addMatchedString("SequenceMatch",orphaned_string,str,control_limit,s))
                    #if(s == 1.0):
                    #break


    return list(set(output_list))
    #return output_dict_list

def LevenshteinMatch(orphaned_string,list_of_strings,control_limit):
    output_list = []
    output_dict_list = []

    for str in list_of_strings:
        # use the Levenshtein jaro_winkler score
        #j = L.jaro_winkler(orphaned_string, str, control_limit)
        j = L.jaro(orphaned_string, list_of_strings[0])
        if(j >= control_limit):
            #print "The string '{}' has {} % match with the orphaned string '{}' ".format(str,s*100,orphaned_string)
            output_list.append(str)
            output_dict_list.append(addMatchedString("Jaro /Winkler",orphaned_string,str,control_limit,j))



    return output_dict_list


#getMDRLineageRowsFromCSV("Account - Overview","Amount")
#getMDRLineageFromCSV("Account - Overview","Amount")

#getObjectsFromCSV("UX Sitemap","","","Screen")
#getObjectsFromCSV("UX Sitemap","Account - Overview","","UI Field")
#getObjectsFromCSV("UX Sitemap","Account - Overview","Amount","")

#getObjectsFromCSV("Visual Map","","","Visual Map")
#getObjectsFromCSV("Visual Map","Account - Overview_MDR_VM","","UI Field")