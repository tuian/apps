#encoding=utf8
import sys,time
import csv
import numpy as np
import pandas as pd
from pandas import DataFrame, read_csv
from mdr_util import *
from Phase1_2_Duplicates import *
# print('Python version ' + sys.version)
# print('Pandas version ' + pd.__version__)
reload(sys)
sys.setdefaultencoding('utf8')

#Global Parameter to define the Metadata Project Phase

GP_PHASE_NO = "Phase 2"

output_csv_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"


list_name_screen_master = "Screen Master"
list_name_screen_fields = "Screen Fields"

list_name_visualmap_master = "Visual Map Master"
list_name_visualmap_fields = "Visual Map Fields"

list_name_ifs_mater = "IFS Master"
list_name_ifs_fields = "IFS Fields"

list_name_xsd_master = "XSD Master"
list_name_xsd_fields = "XSD Fields"
list_name_xsd_fields_abs = "ABS_XSD_FIELDS"

list_name_ldm_master = "ABS_LDM_Master"
list_name_ldm_fields = "LDM_Fields"

#BT ICC & GESB - related objects list
list_name_bt_icc_xsd_fields = "ESB_IFS_Fields"
list_name_gesb_ifs_fields = "ESB_XSD_Fields"

list_name_mapping_ifs_xsd = "Mapping_IFS_XSD"
list_name_mapping_screen_visualmap = "Mapping_Screen_VisualMap"
list_name_mapping_visualmap_ifs = "Mapping_VisualMap_IFS"
list_name_mapping_xsd_ldm = "Mapping_XSD_LDM"

#BT ICC & GESB - related mappings list
list_name_mapping_VM_ESB_IFS = "Mapping_VM_ESB_IFS"
list_name_mapping_VM_ESB_XSD = "Mapping_VM_ESB_XSD"
list_name_mapping_BTICC_XSD_ABS_XSD = "Mapping_BTICC_XSD_ABS_XSD"

def getURL(url_object):

    if(url_object <> None) : url = url_object['href']
    else: url = ""
    #print "URL Object: {} | URL: {} ".format(url_object, url)
    return url

totals_list_objects_global = []

def getBatchDetails(status):
    list_batch_no = []

    folder = "C:/MDR/Data/Repository/CSV_Sharepoint_Output/control/"

    df = pd.read_excel(folder + 'MDR_LOADING.xlsx', sheetname="Batch_Info")
    df = df[df["Status"].str.upper() == status.upper()]

    if(df.empty):
        print("\nERROR: No Records Found for Status '{}'").format(status)
        exit("Exiting the program. Check the Load Control input excel spreadsheet.")

    list_batch_no = df["Batch No"]
    #print list_batch_no
    #print "Batch No [{}] = {}".format(status,list(list_batch_no))

    return list(list_batch_no)

def getBatchDetails_WIP():
    current_batch_no = getBatchDetails("WIP")[0]
    #print "Batch No for [WIP] = {}".format(current_batch_no)
    return current_batch_no

def setTotal(list_name,total,displayOrder):
    #create a temp object
    totals_dict = {}
    #set the values
    totals_dict["Entity Name"] = list_name
    totals_dict["Total"] = total
    totals_dict["DisplayOrder"] = displayOrder

    #append to the global variable
    totals_list_objects_global.append(totals_dict)


#Screen Master - Object
def getObject_ScreenMaster(list_name,mdr_phase_no):
    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)
    #print rows[0].fields

    for row in rows:
        if((row.MDR_x0020_Release).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = row.System_x0020_Name
            row_object["Instance Name"] = row.Instance_x0020_Name
            row_object["Entity Name"] = row.Entity_x0020_Name.upper()
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = row.Entity_x0020_Type
            row_object["Description"] = ""

            row_object["URL"] = ""
            row_object["Document Name"] = ""
            row_object["XPATH"] = ""

            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_ScreenMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)

    setTotal(list_name,len(list_objects),1)

    return list_objects

#Screen Fields - Object
def getObject_ScreenFields(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)
    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = str(row.System_Name).encode("utf-8")
            row_object["Instance Name"] = str(row.Instance_Name).encode("utf-8")
            row_object["Entity Name"] = str(row.Entity_Name_D).encode("utf-8").upper()
            row_object["Attribute Name"] = str(row.Attribute_Name).upper()
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = str(row.Entity_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Description)

            row_object["URL"] = ""
            row_object["Document Name"] = ""
            row_object["XPATH"] = ""

            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_ScreenFields('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 2)
    return list_objects

#VisualMap Master - Object
def getObject_VisualMapMaster(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_x0020_Release_x0020_Period).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = "Visual Map"
            row_object["Instance Name"] = "Default"
            row_object["Entity Name"] = str(row.Entity_Name).encode("utf-8").upper()
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = "Visual Map"
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Funtionality)

            row_object["URL"] = getURL(row.Visual_x0020_Map_x0020_Document_0)
            row_object["Document Name"] = row.Title
            row_object["XPATH"] = ""

            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_VisualMapMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 3)
    return list_objects

#Visual Map Fields - Object
def getObject_VisualMapFields(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)
    for row in rows:
        if ((row.MDR_x0020_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = str(row.System_x0020_Name).encode("utf-8")
            row_object["Instance Name"] = str(row.Instance_x0020_Name).encode("utf-8")
            row_object["Entity Name"] = str(row.Title).encode("utf-8").upper() #Entity Name Duplicate
            row_object["Attribute Name"] = cleanHTMLTags(row.Attribute_x0020_Name).upper()
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = str(row.Entity_x0020_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Description)
            row_object["URL"] = ""
            row_object["Document Name"] = ""
            row_object["XPATH"] = ""
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_VisualMapFields('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 4)
    return list_objects

#IFS Master - Object
def getObject_IFSMaster(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_x0020_Release_x0020_Period).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = str(row.System_Name).encode("utf-8")
            row_object["Instance Name"] = str(row.Instance_Name).encode("utf-8")
            row_object["Entity Name"] = str(row.Title).encode("utf-8").upper()
            row_object["Attribute Name"] = ""
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = "Interface"
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Notes)

            row_object["URL"] = getURL(row.IFS_x0020_Document_x0020_Link)
            row_object["Document Name"] = row.Title
            row_object["XPATH"] = ""

            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_IFSMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 5)
    return list_objects

#IFS Fields - Object
def getObject_IFSFields(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = str(row.System_Name).encode("utf-8")
            row_object["Instance Name"] = str(row.Instance_Name).encode("utf-8")
            row_object["Entity Name"] = str(row.Entity_Name_Duplicate).encode("utf-8").upper()
            row_object["Attribute Name"] = str(row.Attribute_Name).upper()
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = str(row.Entity_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Description)
            row_object["URL"] = ""
            row_object["Document Name"] = ""
            row_object["XPATH"] = cleanHTMLTags(row.XPATH)

            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_IFSFields('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 6)
    return list_objects

#XSD Master - Object
def getObject_XSDMaster(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_x0020_Release_x0020_Period).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = "ABS Dev"
            row_object["Instance Name"] = "Default"
            row_object["Entity Name"] = str(row.Title).encode("utf-8").upper()
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = str(row.Entity_x0020_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Functionality)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_XSDMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 7)
    return list_objects

#XSD Fields - Object
def getObject_XSDFields(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = str(row.System_Name).encode("utf-8")
            row_object["Instance Name"] = str(row.Instance_Name).encode("utf-8")
            row_object["Entity Name"] = str(row.Entity_Name_Duplicate).encode("utf-8").upper()
            row_object["Attribute Name"] = str(row.Attribute_Name).upper()
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = str(row.Entity_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Description)
            row_object["URL"] = ""
            row_object["Document Name"] = ""
            row_object["XPATH"] = cleanHTMLTags(row.XPATH)

            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_XSDFields('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 8)
    return list_objects

#Generic getObjects method
def getObjects(list_name):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

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

    print "getObjects('{}','{}') = ".format(list_name, "All Phases"), len(list_objects)
    setTotal(list_name, len(list_objects), 8)
    return list_objects

def getObjectsByPhase(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
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
    print "getObjectsByPhase('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 8)
    return list_objects


def getObject_XSDFields_All_Phases(list_name):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)
    rows_mappings = sharepointListRowsByListName("Mapping_IFS_XSD")

    for row in rows:
        if (True):
            row_object = {}
            row_object["System Name"] = str(row.System_Name).encode("utf-8")
            row_object["Instance Name"] = str(row.Instance_Name).encode("utf-8")
            row_object["Entity Name"] = str(row.Entity_Name_Duplicate).encode("utf-8").upper()
            row_object["Attribute Name"] = str(row.Attribute_Name).upper()
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = str(row.Entity_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Description)
            row_object["URL"] = ""
            row_object["Document Name"] = ""
            row_object["XPATH"] = ""
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_XSDFields_All_Phases('{}') = ".format(list_name), len(list_objects)
    #setTotal(list_name, len(list_objects), 8)

    for row_mapping in rows_mappings:
        if(row_mapping.Target_Attribute_Name_ABS_D <> ""):
            row_object = {}
            row_object["System Name"] = str(row_mapping.Target_System_Name).encode("utf-8")
            row_object["Instance Name"] = str(row_mapping.Target_Instance_Name).encode("utf-8")
            row_object["Entity Name"] = str(row_mapping.Target_Entity_Name_ABS_D).encode("utf-8").upper()
            row_object["Attribute Name"] = str(row_mapping.Target_Attribute_Name_ABS_D).encode("utf-8").upper()
            row_object["Owner"] = "Mapping"
            row_object["Parent"] = "Mapping"
            row_object["Type"] = "Attribute"
            # row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row_mapping.Attribute_x0020_Description)
            row_object["URL"] = ""
            row_object["Document Name"] = ""
            row_object["XPATH"] = ""
            # row_object[""] = row.
            list_objects.append(row_object)

    print "getObject_XSDFields_All_Phases('{}') = ".format("Mapping_IFS_XSD"), len(list_objects)

    return list_objects

#LDM Master - Object
def getObject_LDMMaster(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_x0020_Release_x0020_Period).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = row.System_Name #"ABS Dev"
            row_object["Instance Name"] = row.Instance_Name #"Default"
            row_object["Entity Name"] = str(row.Title).encode("utf-8").upper()
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = str(row.Entity_x0020_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Functionality)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_XSDMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 9)
    return list_objects

#LDM Fields - Object
def getObject_LDMFields(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = row.System_Name #"ABS Dev"
            row_object["Instance Name"] = row.Instance_Name #"Default"
            row_object["Entity Name"] = row.Entity_Name.upper()
            row_object["Attribute Name"] = row.Attribute_Name.upper()
            row_object["Owner"] = row.Owner
            row_object["Parent"] = row.Parent
            row_object["Type"] = row.Attribute_Type
            row_object["Description"] = cleanHTMLTags(row.Description)
            row_object["URL"] = ""
            row_object["Document Name"] = ""
            row_object["XPATH"] = ""
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_LDMFields('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 10)
    return list_objects

# "Mapping_Screen_VisualMap"
def getMapping_UX_VM(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}

            row_object["Source System Name"] = row.Source_System_Name
            row_object["Source Instance Name"] = "Default"
            row_object["Source Entity Name"] = (row.Source_Entity_Name_D).upper()
            row_object["Source Attribute Name"] = cleanHTMLTags(row.Source_Attribute_Name0).upper()
            row_object["Target System Name"] = row.Target_System_Name
            row_object["Target Instance Name"] = row.Target_Instance_Name
            row_object["Target Entity Name"] = row.Target_Entity_Name_D.upper()
            row_object["Target Attribute Name"] = cleanHTMLTags(row.Target_Attribute_Name_D).upper()
            row_object["Attribute Description"] = row.Attribute_Description
            row_object["Business Rule"] = cleanHTMLTags(row.Business_Rule)
            row_object["Transformation_Mapping rule"] = cleanHTMLTags(row.Transformation_Mapping_Rule)
            row_object["Comments"] = row.Comments
            row_object["Mapping Name"] = row.Mapping_Name
            row_object["Action"] = row.Action
            row_object["Last_Update_Date"] = row.Last_Update_Date
            row_object["Modified_By"] = row.Modified_By

            # row_object[""] = row.Title
            list_objects.append(row_object)
    print "getMapping_UX_VM('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 11)
    return list_objects

# "Mapping_VisualMap_IFS"
def getMapping_VM_IFS(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}

            row_object["Source System Name"] = row.Source_System_Name
            row_object["Source Instance Name"] = row.Source_Instance_Name #"Default"
            row_object["Source Entity Name"] = row.Source_Entity_Name_D.upper()
            row_object["Source Attribute Name"] = cleanHTMLTags(row.Source_Attribute_Name_Duplicate).upper()
            row_object["Target System Name"] = row.Target_System_Name
            row_object["Target Instance Name"] = row.Target_Instance_Name
            row_object["Target Entity Name"] = cleanHTMLTags(row.Target_Entity_Name_D).upper()
            row_object["Target Attribute Name"] = cleanHTMLTags(row.Target_Attribute_Name_Duplicate).upper()
            row_object["Attribute Description"] = row.Attribute_Description
            row_object["Business Rule"] = cleanHTMLTags(row.Business_Rule)
            row_object["Transformation_Mapping rule"] = cleanHTMLTags(row.Transformation_Mapping_Rule)
            row_object["Comments"] = row.Comments
            row_object["Mapping Name"] = row.Mapping_Name
            row_object["Action"] = row.Action
            row_object["Last_Update_Date"] = row.Last_Update_Date
            row_object["Modified_By"] = row.Modified_By

            # row_object[""] = row.Title
            list_objects.append(row_object)
    print "getMapping_VM_IFS('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 12)
    return list_objects

#"Mapping_IFS_XSD"
def getMapping_IFS_XSD(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}

            row_object["Source System Name"] = row.Source_System_Name
            row_object["Source Instance Name"] = row.Title
            row_object["Source Entity Name"] = row.Source_Entity_Name_Duplicate.upper()
            row_object["Source Attribute Name"] = cleanHTMLTags(row.Source_Attribute_Name_Duplicate).upper()
            row_object["Target System Name"] = row.Target_System_Name
            row_object["Target Instance Name"] = row.Target_Instance_Name
            row_object["Target Entity Name"] = row.Target_Entity_Name_Duplicate.upper()
            row_object["Target Attribute Name"] = row.Target_Attribute_Name_Duplicate.upper()

            row_object["Target_Entity_Name_ABS_D"] = row.Target_Entity_Name_ABS_Object_D.upper()
            row_object["Target_Attribute_Name_ABS_D"] = cleanHTMLTags(row.Target_Attribute_Name_ABS_Object).upper()

            row_object["Attribute Description"] = cleanHTMLTags(row.Attribute_x0020_Description)
            row_object["Business Rule"] = cleanHTMLTags(row.Business_x0020_Rule)
            row_object["Transformation_Mapping rule"] = cleanHTMLTags(row.Transformation_Mapping_Rule)
            row_object["Comments"] = cleanHTMLTags(row.Comments)
            row_object["Mapping Name"] = cleanHTMLTags(row.Mapping_x0020_Name)
            row_object["Action"] = row.Action
            row_object["Last_Update_Date"] = row.Last_Update_Date
            row_object["Modified_By"] = row.Modified_By

            # row_object[""] = row.Title
            list_objects.append(row_object)
    print "getMapping_IFS_XSD('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 13)
    return list_objects

#"Mapping_IFS_XSD - All"

def getMapping_IFS_XSD_All(list_name):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:

        row_object = {}

        row_object["Source System Name"] = row.Source_System_Name
        row_object["Source Instance Name"] = row.Title
        row_object["Source Entity Name"] = row.Source_Entity_Name_Duplicate.upper()
        row_object["Source Attribute Name"] = cleanHTMLTags(row.Source_Attribute_Name_Duplicate).upper()
        row_object["Target System Name"] = row.Target_System_Name
        row_object["Target Instance Name"] = row.Target_Instance_Name
        row_object["Target Entity Name"] = row.Target_Entity_Name_Duplicate.upper()
        row_object["Target Attribute Name"] = cleanHTMLTags(row.Target_Attribute_Name_Duplicate).upper()

        row_object["Target_Entity_Name_ABS_D"] = row.Target_Entity_Name_ABS_D.upper()
        row_object["Target_Attribute_Name_ABS_D"] = row.Target_Attribute_Name_ABS_D.upper()

        row_object["Attribute Description"] = row.Attribute_x0020_Description
        row_object["Business Rule"] = cleanHTMLTags(row.Business_x0020_Rule)
        row_object["Transformation_Mapping rule"] = cleanHTMLTags(row.Transformation_Mapping_Rule)
        row_object["Comments"] = row.Comments
        row_object["Mapping Name"] = row.Mapping_x0020_Name
        row_object["Action"] = row.Action
        row_object["Last_Update_Date"] = row.Last_Update_Date
        row_object["Modified_By"] = row.Modified_By

        # row_object[""] = row.Title
        list_objects.append(row_object)

    print "getMapping_IFS_XSD('{}','{}') = ".format(list_name, "All"), len(list_objects)
    #setTotal(list_name, len(list_objects), 13)
    return list_objects

# "Mapping_XSD_LDM"
def getMapping_XSD_LDM(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}

            row_object["Source System Name"] = row.Source_System_Name
            row_object["Source Instance Name"] = row.Source_Instance_Name
            row_object["Source Entity Name"] = row.Source_Entity_Name.upper()
            row_object["Source Attribute Name"] = (row.Source_Attribute_Name).upper()
            row_object["Target System Name"] = row.Target_System_Name
            row_object["Target Instance Name"] = row.Target_Instance_Name
            row_object["Target Entity Name"] = row.Target_Entity_Name_D.upper()
            row_object["Target Attribute Name"] = (row.Target_Attribute_Name_D).upper()



            row_object["Attribute Description"] = cleanHTMLTags(row.Attribute_Description)
            row_object["Business Rule"] = cleanHTMLTags(row.Business_Rule)
            row_object["Transformation_Mapping rule"] = cleanHTMLTags(row.Transformation_Mapping_Rule)
            row_object["Comments"] = cleanHTMLTags(row.Comments)
            row_object["Mapping Name"] = cleanHTMLTags(row.Mapping_Name)
            row_object["Action"] = row.Action
            row_object["Last_Update_Date"] = row.Last_Update_Date
            row_object["Modified_By"] = row.Modified_By

            # row_object[""] = row.Title
            list_objects.append(row_object)
    print "getMapping_XSD_LDM('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    setTotal(list_name, len(list_objects), 14)
    return list_objects

# "Mapping_XSD_LDM All"
def getMapping_XSD_LDM_All(list_name):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:

        row_object = {}

        row_object["Source System Name"] = row.Source_System_Name
        row_object["Source Instance Name"] = row.Source_Instance_Name
        row_object["Source Entity Name"] = row.Source_Entity_Name.upper()
        row_object["Source Attribute Name"] = cleanHTMLTags(row.Source_Attribute_Name).upper()
        row_object["Target System Name"] = row.Target_System_Name
        row_object["Target Instance Name"] = row.Target_Instance_Name
        row_object["Target Entity Name"] = row.Target_Entity_Name_D.upper()
        row_object["Target Attribute Name"] = cleanHTMLTags(row.Target_Attribute_Name_D).upper()



        row_object["Attribute Description"] = row.Attribute_Description
        row_object["Business Rule"] = cleanHTMLTags(row.Business_Rule)
        row_object["Transformation_Mapping rule"] = cleanHTMLTags(row.Transformation_Mapping_Rule)
        row_object["Comments"] = row.Comments
        row_object["Mapping Name"] = row.Mapping_Name
        row_object["Action"] = row.Action
        row_object["Last_Update_Date"] = row.Last_Update_Date
        row_object["Modified_By"] = row.Modified_By

        # row_object[""] = row.Title
        list_objects.append(row_object)

    print "getMapping_XSD_LDM('{}','{}') = ".format(list_name, "All"), len(list_objects)
    #setTotal(list_name, len(list_objects), 14)
    return list_objects

# get Mappings By Phase - Generic Method
def getMappingsByPhase(list_name,mdr_phase_no,xsd_from_abs_report_flag):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_Phase).upper() == mdr_phase_no.upper()):
            row_object = {}

            row_object["Source System Name"]   = row.Source_System_Name
            row_object["Source Instance Name"] = row.Source_Instance_Name
            row_object["Target System Name"]   = row.Target_System_Name
            row_object["Target Instance Name"] = row.Target_Instance_Name

            row_object["Source Entity Name"]    = row.Source_Entity_Name_D.upper()
            row_object["Source Attribute Name"] = (row.Source_Attribute_Name_D).upper()


            if(xsd_from_abs_report_flag == 1):
                row_object["Target Entity Name"] = row.Target_Entity_Name_ABS_Object_D.upper()
                row_object["Target Attribute Name"] = row.Target_Attribute_Name_ABS_Object.upper()
            else:
                row_object["Target Entity Name"] = row.Target_Entity_Name_D.upper()
                row_object["Target Attribute Name"] = (row.Target_Attribute_Name_D).upper()

            row_object["Attribute Description"] = cleanHTMLTags(row.Attribute_Description)
            row_object["Comments"] = cleanHTMLTags(row.Comments)
            row_object["Business Rule"] = cleanHTMLTags(row.Business_Rule)
            row_object["Transformation_Mapping rule"] = cleanHTMLTags(row.Transformation_Mapping_Rule)
            row_object["Mapping Name"] = cleanHTMLTags(row.Mapping_Name)

            row_object["Action"] = row.Action
            row_object["Last_Update_Date"] = row.Last_Update_Date
            row_object["Modified_By"] = row.Modified_By

            row_object["MDR_Phase"] = row.MDR_Phase
            # row_object[""] = row.Title
            list_objects.append(row_object)

    print "getMappingsByPhase('{}','{}','xsd_from_abs_report_flag:{}') | Count = {}".format(list_name, mdr_phase_no,xsd_from_abs_report_flag, len(list_objects))
    setTotal(list_name, len(list_objects), 14)
    return list_objects

def buidObjects(phase):




    createFolderPath(output_csv_folder_path)

    ''' '''

    #Objects Start

    # row_objects_ux  = getObject_ScreenMaster(list_name_screen_master,GP_PHASE_NO)
    # row_objects_ux  = getObject_ScreenFields(list_name_screen_fields,GP_PHASE_NO)
    row_objects_ux  = getObject_ScreenMaster(list_name_screen_master,GP_PHASE_NO) + getObject_ScreenFields(list_name_screen_fields,GP_PHASE_NO)

    #row_objects_vm  = getObject_VisualMapMaster(list_name_visualmap_master,GP_PHASE_NO)
    #row_objects_vm  = getObject_VisualMapFields(list_name_visualmap_fields,GP_PHASE_NO)
    row_objects_vm  = getObject_VisualMapMaster(list_name_visualmap_master,GP_PHASE_NO) + getObject_VisualMapFields(list_name_visualmap_fields,GP_PHASE_NO)

    #row_objects_ifs = getObject_IFSMaster(list_name_ifs_mater,GP_PHASE_NO)
    #row_objects_ifs = getObject_IFSFields(list_name_ifs_fields,GP_PHASE_NO)
    row_objects_ifs = getObject_IFSMaster(list_name_ifs_mater,GP_PHASE_NO) + getObject_IFSFields(list_name_ifs_fields,GP_PHASE_NO)

    #row_objects_xsd = getObject_XSDMaster(list_name_xsd_master,GP_PHASE_NO)
    row_objects_xsd = getObject_XSDFields(list_name_xsd_fields,GP_PHASE_NO) # containts both class and attribute
    #row_objects_xsd = getObject_XSDMaster(list_name_xsd_master,GP_PHASE_NO) + getObject_XSDFields(list_name_xsd_fields,GP_PHASE_NO)

    row_objects_xsd_all_phases = getObject_XSDFields_All_Phases(list_name_xsd_fields)

    row_objects_xsd_fields_from_abs = getObjects(list_name_xsd_fields_abs)

    # row_objects_ldm = getObject_LDMMaster(list_name_ldm_master,GP_PHASE_NO) # No LDM Master, Only LDM Fields
    row_objects_ldm = getObject_LDMFields(list_name_ldm_fields,GP_PHASE_NO)
    #row_objects_ldm = getObject_LDMMaster(list_name_ldm_master,GP_PHASE_NO) + getObject_LDMFields(list_name_ldm_fields,GP_PHASE_NO)

    #getObject_BT_ICC_XSD_Fields
    #getObject_GESB_IFS_Fields

    # BT ICC XSD Fields
    row_objects_bt_icc_xsd = getObjectsByPhase(list_name_bt_icc_xsd_fields, GP_PHASE_NO)
    # GCM IFS Fields
    row_objects_gesb_ifs = getObjectsByPhase(list_name_gesb_ifs_fields, GP_PHASE_NO)

    #columns required in the output csv file [Objects]
    columns_objects_csv = ["System Name","Instance Name","Entity Name","Attribute Name","Owner","Parent","Type","Description","URL","Document Name","XPATH"]

    #  UX Objects
    df_ux = pd.DataFrame(row_objects_ux,columns=columns_objects_csv)
    df_ux.to_csv(output_csv_folder_path + "Objects_ux.csv",sep=",",header=True,index=None)

    # VM Objects
    df_vm = pd.DataFrame(row_objects_vm,columns=columns_objects_csv)
    df_vm.to_csv(output_csv_folder_path + "Objects_vm.csv",sep=",",header=True,index=None)

    # IFS Objects
    df_ifs = pd.DataFrame(row_objects_ifs,columns=columns_objects_csv)
    df_ifs.to_csv(output_csv_folder_path + "Objects_ifs.csv",sep=",",header=True,index=None)

    # XSD Objects
    df_xsd = pd.DataFrame(row_objects_xsd,columns=columns_objects_csv)
    df_xsd.to_csv(output_csv_folder_path + "Objects_xsd_from_ifs_phases_2.csv",sep=",",header=True,index=None)

    #XSD Objects [From IFS] = All phases
    df_xsd_all_phases = pd.DataFrame(row_objects_xsd_all_phases, columns=columns_objects_csv)
    df_xsd_all_phases.to_csv(output_csv_folder_path + "Objects_xsd_from_ifs_phases_all.csv", sep=",", header=True, index=None)

    # XSD Objects [From Avaloq Report] = All phases
    df_xsd_from_abs_all_phases = pd.DataFrame(row_objects_xsd_fields_from_abs, columns=columns_objects_csv)
    df_xsd_from_abs_all_phases.to_csv(output_csv_folder_path + "Objects_xsd_from_abs_phases_all.csv", sep=",", header=True, index=None)

    #  LDM Objects
    df_ldm = pd.DataFrame(row_objects_ldm,columns=columns_objects_csv)
    df_ldm.to_csv(output_csv_folder_path + "Objects_ldm.csv",sep=",",header=True,index=None)

    # BT ICC XSD Fields
    df_bticc_xsd = pd.DataFrame(row_objects_bt_icc_xsd, columns=columns_objects_csv)
    df_bticc_xsd.to_csv(output_csv_folder_path + "Objects_bt_icc_xsd.csv", sep=",", header=True, index=None)

    # GESB IFS Fields
    df_gesb_ifs = pd.DataFrame(row_objects_gesb_ifs, columns=columns_objects_csv)
    df_gesb_ifs.to_csv(output_csv_folder_path + "Objects_gesb_ifs.csv", sep=",", header=True, index=None)

    # control what objects you want. Edit the df_frames[] list below

    df_frames = [df_ux,df_vm,df_ifs,df_xsd_from_abs_all_phases,df_ldm,df_bticc_xsd,df_gesb_ifs]
    df = pd.concat(df_frames)

    #sort
    sort_by_columns = ["System Name","Entity Name", "Attribute Name","Type"]
    df.sort_values(by=sort_by_columns, inplace=True, na_position='first', ascending=[False, True,True,True])

    #find duplicates and sort it in a new dataframe
    duplicated_by_columns = ["System Name","Entity Name", "Attribute Name","Type"]
    df_duplicates = df[df.duplicated(subset=duplicated_by_columns, keep=False)]

    # drop the duplicates in the original dataframe
    df.drop_duplicates(subset=duplicated_by_columns, keep='first', inplace=True)

    df.to_csv(output_csv_folder_path + "Objects.csv",sep=",",header=True,index=None)
    df_duplicates.to_csv(output_csv_folder_path + "Objects_duplicates.csv", sep=",", header=True, index=None)

    # df.info()
    # df.describe()
    # print df.head().to_string()
    # print df.tail().to_string()
    sendSharepointListTotals_To_CSV_File()
    #Objects End

def processMapping(list_name,abs_flag,GP_PHASE_NO,columns_mappings_csv,sort_columns,duplicated_by_columns,output_folder_path,output_csv_file_name):

    # "Mapping_XSD_LDM"
            ### get the records from sharepoint
    row_mappings = getMappingsByPhase(list_name, GP_PHASE_NO,abs_flag)
    df = pd.DataFrame(row_mappings, columns=columns_mappings_csv)

     #sort values
    df.sort_values(by=sort_columns, inplace=True, na_position='first', ascending=[True, True])

            ###Make a new df to hold the duplicates (keep=False -> flag the first row as well as duplicate)
    df_duplicate = df[df.duplicated(subset=duplicated_by_columns,keep=False)]

            ###drop the duplicate rows, keep first and inplace=True
    df.drop_duplicates(subset=duplicated_by_columns, keep='first', inplace=True)

            ###send to CSV file
    df.to_csv(output_folder_path + output_csv_file_name+".csv",sep=",",header=True,index=None)
    df_duplicate.to_csv(output_folder_path +output_csv_file_name +"_duplicate.csv", sep=",", header=True, index=None)
    #print df.head()
    #print df_duplicate
    return df

def buildMapings(phase):

    createFolderPath(output_csv_folder_path)

    #columns required in the output csv file [Objects]
    columns_mappings_csv     = ["Source System Name","Source Instance Name","Source Entity Name","Source Attribute Name","Target System Name","Target Instance Name","Target Entity Name","Target Attribute Name","Attribute Description","Business Rule","Transformation_Mapping rule","Comments","Mapping Name","Action","Last_Update_Date","Modified_By"]
    columns_mappings_abs_csv = ["Source System Name","Source Instance Name","Source Entity Name","Source Attribute Name","Target System Name","Target Instance Name","Target Entity Name","Target Attribute Name","Target_Entity_Name_ABS_D","Target_Attribute_Name_ABS_D","Attribute Description","Business Rule","Transformation_Mapping rule","Comments","Mapping Name","Action","Last_Update_Date","Modified_By"]

    # sort dataframe by columns ["Source Entity Name","Source Attribute Name"]
    sort_columns = ["Source Entity Name", "Source Attribute Name"]
    duplicated_by_columns = ["Source Entity Name", "Source Attribute Name","Target Entity Name", "Target Attribute Name"]

    #"Mapping_Screen_VisualMap"
            ### get the records from sharepoint
    row_mappings_ux_vm = getMapping_UX_VM(list_name_mapping_screen_visualmap, GP_PHASE_NO)
    df_mapping_ux_vm = pd.DataFrame(row_mappings_ux_vm, columns=columns_mappings_csv)

            ### df_mapping_ifs_xsd.sort(columns=sort_columns,inplace=True) #depricated, use sort_values(by=)
    df_mapping_ux_vm.sort_values(by=sort_columns, inplace=True, na_position='first', ascending=[True, True])

            ###Make a new df to hold the duplicates (keep=False -> flag the first row as well as duplicate)
    df_mapping_ux_vm_duplicates = df_mapping_ux_vm[df_mapping_ux_vm.duplicated(subset=duplicated_by_columns,keep=False)]

            ###drop the duplicate rows, keep first and inplace=True
    df_mapping_ux_vm.drop_duplicates(subset=duplicated_by_columns, keep='first', inplace=True)

    # df_mapping_ux_vm.drop_duplicates(["Source Entity Name", "Source Attribute Name"])
    # df_mapping_ux_vm.drop_duplicates(["Target Entity Name", "Target Attribute Name"])

    ###send to CSV file
    df_mapping_ux_vm.to_csv(output_csv_folder_path + "Mapping_ux_vm.csv",sep=",",header=True,index=None)
    df_mapping_ux_vm_duplicates.to_csv(output_csv_folder_path + "Mapping_ux_vm_duplicates.csv", sep=",", header=True, index=None)

    #"Mapping_VisualMap_IFS"

            ### get the records from sharepoint
    row_mappings_vm_ifs = getMapping_VM_IFS(list_name_mapping_visualmap_ifs, GP_PHASE_NO)
    df_mapping_vm_ifs            = pd.DataFrame(row_mappings_vm_ifs, columns=columns_mappings_csv)

            ### df_mapping_ifs_xsd.sort(columns=sort_columns,inplace=True) #depricated, use sort_values(by=)
    df_mapping_vm_ifs.sort_values(by=sort_columns, inplace=True, na_position='first', ascending=[True, True])

            ###Make a new df to hold the duplicates (keep=False -> flag the first row as well as duplicate)
    df_mapping_vm_ifs_duplicates = df_mapping_vm_ifs[df_mapping_vm_ifs.duplicated(subset=duplicated_by_columns,keep=False)]

            ###drop the duplicate rows, keep first and inplace=True
    df_mapping_vm_ifs.drop_duplicates(subset=duplicated_by_columns, keep='first', inplace=True)

            ###send to CSV file
    df_mapping_vm_ifs.to_csv(output_csv_folder_path + "Mapping_vm_ifs.csv",sep=",",header=True,index=None)
    df_mapping_vm_ifs_duplicates.to_csv(output_csv_folder_path + "Mapping_vm_ifs_duplicates.csv", sep=",", header=True, index=None)

    #"Mapping_IFS_XSD"
            ### get the records from sharepoint
    row_mappings_ifs_xsd  = getMapping_IFS_XSD(list_name_mapping_ifs_xsd,GP_PHASE_NO)
    df_mapping_ifs_xsd = pd.DataFrame(row_mappings_ifs_xsd,columns=columns_mappings_abs_csv)

            ### df_mapping_ifs_xsd.sort(columns=sort_columns,inplace=True) #depricated, use sort_values(by=)
    df_mapping_ifs_xsd.sort_values(by=sort_columns, inplace=True, na_position='first', ascending=[True, True])

            ###Make a new df to hold the duplicates (keep=False -> flag the first row as well as duplicate)
    df_mapping_ifs_xsd_duplicate = df_mapping_ifs_xsd[df_mapping_ifs_xsd.duplicated(subset=duplicated_by_columns,keep=False)]

            ###drop the duplicate rows, keep first and inplace=True
    df_mapping_ifs_xsd.drop_duplicates(subset=duplicated_by_columns,keep='first',inplace=True)

            ###send to CSV file
    df_mapping_ifs_xsd.to_csv(output_csv_folder_path + "Mapping_ifs_xsd.csv",sep=",",header=True,index=None)
    df_mapping_ifs_xsd_duplicate.to_csv(output_csv_folder_path + "Mapping_ifs_xsd_duplicate.csv", sep=",", header=True, index=None)

    # "Mapping_XSD_LDM"
            ### get the records from sharepoint
    row_mappings_xsd_ldm = getMapping_XSD_LDM(list_name_mapping_xsd_ldm, GP_PHASE_NO)
    df_mapping_xsd_ldm = pd.DataFrame(row_mappings_xsd_ldm, columns=columns_mappings_csv)

            ### df_mapping_ifs_xsd.sort(columns=sort_columns,inplace=True) #depricated, use sort_values(by=)
    df_mapping_xsd_ldm.sort_values(by=sort_columns, inplace=True, na_position='first', ascending=[True, True])

            ###Make a new df to hold the duplicates (keep=False -> flag the first row as well as duplicate)
    df_mapping_xsd_ldm_duplicate = df_mapping_xsd_ldm[df_mapping_xsd_ldm.duplicated(subset=duplicated_by_columns,keep=False)]

            ###drop the duplicate rows, keep first and inplace=True
    df_mapping_xsd_ldm.drop_duplicates(subset=duplicated_by_columns, keep='first', inplace=True)

            ###send to CSV file
    df_mapping_xsd_ldm.to_csv(output_csv_folder_path + "Mapping_xsd_ldm.csv",sep=",",header=True,index=None)
    df_mapping_xsd_ldm_duplicate.to_csv(output_csv_folder_path + "Mapping_xsd_ldm_duplicate.csv", sep=",", header=True, index=None)

    # Mapping Mapping_VM_ESB_XSD
    df_mapping_vm_esb_xsd = processMapping(list_name_mapping_VM_ESB_XSD,0, GP_PHASE_NO, columns_mappings_csv,sort_columns, duplicated_by_columns, output_csv_folder_path,list_name_mapping_VM_ESB_XSD)

    # Mapping Mapping_VM_ESB_IFS
    df_mapping_vm_esb_ifs = processMapping(list_name_mapping_VM_ESB_IFS,0,GP_PHASE_NO,columns_mappings_csv,sort_columns,duplicated_by_columns,output_csv_folder_path,list_name_mapping_VM_ESB_IFS)

    # Mapping Mapping_BTICC_XSD_ABS_XSD
    df_mapping_bt_icc_abs_xsd = processMapping(list_name_mapping_BTICC_XSD_ABS_XSD,1,GP_PHASE_NO,columns_mappings_csv,sort_columns,duplicated_by_columns,output_csv_folder_path,list_name_mapping_BTICC_XSD_ABS_XSD)

    # Combined Mapping file
    df_mapping_ifs_xsd_abs = df_mapping_ifs_xsd
    df_mapping_ifs_xsd_abs.drop(labels=["Target Entity Name","Target Attribute Name"],inplace=True,axis=1)
    df_mapping_ifs_xsd_abs.rename(columns={"Target_Entity_Name_ABS_D":"Target Entity Name","Target_Attribute_Name_ABS_D":"Target Attribute Name"},inplace=True)

    df_frames = [df_mapping_ux_vm, df_mapping_vm_ifs, df_mapping_ifs_xsd_abs, df_mapping_xsd_ldm,df_mapping_vm_esb_xsd,df_mapping_vm_esb_ifs,df_mapping_bt_icc_abs_xsd]
    df = pd.concat(df_frames)

    df.to_csv(output_csv_folder_path + "Mappings.csv", sep=",", header=True, index=None,columns=columns_mappings_csv)

    # filter and get the rows we are interested to load

    #df_load = df[df["Source Entity Name"] in ["Advice_Fees"]]
    #df_load.to_csv(output_csv_folder_path + "Mappings_load.csv", sep=",", header=True, index=None, columns=columns_mappings_csv)

    # df.info()
    # df.describe()
    # print df.head().to_string()
    # print df.tail().to_string()
    sendSharepointListTotals_To_CSV_File()
    # Mapping Builder End

def checkAttributes():
    print "\n####################   checkAttributes()  ####################\n"

    input_excel_folder_path_phase1 = "C:\MDR\Data\Repository\Input\Phase1"
    input_excel_filename_phase1 = "\Phase1_Objects_Mappings.xlsx"

    df_phase1_objects =  pd.read_excel(input_excel_folder_path_phase1 + input_excel_filename_phase1, sheetname="Objects",index_col=None)
    df_phase2_objects  = pd.read_csv(output_csv_folder_path + 'BTP_Phase2_Objects.csv', sep=",")

    df_phase1_objects["Entity Name"] = df_phase1_objects["Entity Name"].str.upper()
    df_phase1_objects["Attribute Name"] = df_phase1_objects["Attribute Name"].str.upper()

    df_objects = pd.concat([df_phase1_objects,df_phase2_objects])
    df_objects.to_csv(output_csv_folder_path + "BTP_Phase1_2_Objects.csv", sep=",")

    df_mappings = pd.read_csv(output_csv_folder_path + 'BTP_Phase2_Mappings.csv', sep=",")



    #df_mappings = df_mappings[df_mappings["Source Attribute Name"] <> '' | df_mappings["Target Attribute Name"] <> '']
    df_mappings.dropna(subset=["Source Attribute Name"],inplace=True)
    df_mappings = df_mappings.reset_index();  # http://www.sirhamy.com/blog/2016/03/troubleshoot-pandas-label-not-in-index/

    #df_mappings = df_mappings[np.isfinite(df_mappings['Source Attribute Name'])]
    #df = df[pd.notnull(df['EPS'])]
    #print df_objects.head()
    #print df_mappings.head()

    #if mapping Source Atribute Name or Target Attribute Name - is not in Object - then Error
    #print df_mappings["Source Attribute Name"],df_mappings["Target Attribute Name"]

    print "Source Attribute Count is:",len(df_mappings)
    df_mappings_s_missing = df_mappings[~df_mappings["Source Attribute Name"].isin(df_objects["Attribute Name"])]
    print df_mappings_s_missing["Source Attribute Name"]
    print "Source Attributes Missing count is:",len(df_mappings_s_missing)
    df_mappings_s_missing.to_csv(output_csv_folder_path + "Mapping_Fields_Missing_SA.csv", sep=",")
    '''
    for row in range(1,len(df_mappings)):
       #print df_mappings.loc[row, "Source Attribute Name"]
       if (df_mappings.loc[row,"Source Attribute Name"].isin(df_objects["Attribute Name"])):
            print "Error {}".format(df_mappings.loc[row,"Source Attribute Name"])
    '''


    df_mappings.dropna(subset=["Target Attribute Name"], inplace=True)
    df_mappings = df_mappings.reset_index();  # http://www.sirhamy.com/blog/2016/03/troubleshoot-pandas-label-not-in-index/

    print "Target Attribute Count is:", len(df_mappings)

    df_mappings_t_missing = df_mappings[~df_mappings["Target Attribute Name"].isin(df_objects["Attribute Name"])]
    print df_mappings_t_missing["Target Attribute Name"]
    print "Target Attributes Missing count is:", len(df_mappings_t_missing)
    df_mappings_t_missing.to_csv(output_csv_folder_path+"Mapping_Fields_Missing_TA.csv",sep=",")
    '''
    for row in range(1,len(df_mappings)):
     print df_mappings.loc[row, "Target Attribute Name"]
    '''

def checkAttributesByJoin(join_type):
    '''

    :param join_type:
    :return:
    '''
    print "\n####################   checkAttributesByJoin({})  ####################\n".format(join_type)

    input_excel_folder_path_phase1 = "C:\MDR\Data\Repository\Input\Phase1"
    input_excel_filename_phase1 = "\Phase1_Objects_Mappings.xlsx"

    df_phase1_objects =  pd.read_excel(input_excel_folder_path_phase1 + input_excel_filename_phase1, sheetname="Objects",index_col=None)
    df_phase2_objects  = pd.read_csv(output_csv_folder_path + 'BTP_Phase2_Objects.csv', sep=",")

    df_phase1_objects["Entity Name"] = df_phase1_objects["Entity Name"].str.upper()
    df_phase1_objects["Attribute Name"] = df_phase1_objects["Attribute Name"].str.upper()

    df_objects = pd.concat([df_phase1_objects,df_phase2_objects])
    df_objects.to_csv(output_csv_folder_path + "BTP_Phase1_2_Objects_ByJoin.csv", sep=",")

    df_mappings = pd.read_csv(output_csv_folder_path + 'BTP_Phase2_Mappings.csv', sep=",")


    #df_mappings = df_mappings[df_mappings["Source Attribute Name"] <> '' | df_mappings["Target Attribute Name"] <> '']
    df_mappings.dropna(subset=["Source Attribute Name"],inplace=True)
    df_mappings = df_mappings.reset_index();  # http://www.sirhamy.com/blog/2016/03/troubleshoot-pandas-label-not-in-index/

    #df_mappings = df_mappings[np.isfinite(df_mappings['Source Attribute Name'])]
    #df = df[pd.notnull(df['EPS'])]
    #print df_objects.head()
    #print df_mappings.head()

    #if mapping Source Atribute Name or Target Attribute Name - is not in Object - then Error
    #print df_mappings["Source Attribute Name"],df_mappings["Target Attribute Name"]

    print "Source Attribute Count is:",len(df_mappings)
    df_mappings_s_missing = pd.merge(left=df_mappings,right=df_objects,left_on=["Source Entity Name","Source Attribute Name"],right_on=["Entity Name","Attribute Name"],how=join_type)
    df_mappings_s_missing_count = df_mappings_s_missing[(df_mappings_s_missing["Entity Name"].isnull() ) & (df_mappings_s_missing["Attribute Name"].isnull())]
    #df_mappings_s_missing = df_mappings[~df_mappings["Source Attribute Name"].isin(df_objects["Attribute Name"])]
    #print df_mappings_s_missing["Source Attribute Name"]
    print "Source Attributes Join Row is:", len(df_mappings_s_missing)
    print "Source Attributes Join Missing count is:",len(df_mappings_s_missing_count)
    df_mappings_s_missing = df_mappings_s_missing[(df_mappings_s_missing["Entity Name"].isnull()) & (df_mappings_s_missing["Attribute Name"].isnull())]
    df_mappings_s_missing.to_csv(output_csv_folder_path + "Mapping_Fields_Missing_S_E_A.csv", sep=",",columns=["Source System Name","Source Instance Name","Source Entity Name","Source Attribute Name"],index=None)
    '''
    for row in range(1,len(df_mappings)):
       #print df_mappings.loc[row, "Source Attribute Name"]
       if (df_mappings.loc[row,"Source Attribute Name"].isin(df_objects["Attribute Name"])):
            print "Error {}".format(df_mappings.loc[row,"Source Attribute Name"])
    '''


    df_mappings.dropna(subset=["Target Attribute Name"], inplace=True)
    df_mappings = df_mappings.reset_index();  # http://www.sirhamy.com/blog/2016/03/troubleshoot-pandas-label-not-in-index/

    print "Target Attribute Count is:", len(df_mappings)

    #df_mappings_t_missing = df_mappings[~df_mappings["Target Attribute Name"].isin(df_objects["Attribute Name"])]
    #print df_mappings_t_missing["Target Attribute Name"]
    df_mappings_t_missing = pd.merge(left=df_mappings, right=df_objects,left_on=["Target Entity Name", "Target Attribute Name"],right_on=["Entity Name", "Attribute Name"], how=join_type)
    df_mappings_t_missing_count = df_mappings_t_missing[(df_mappings_t_missing["Entity Name"].isnull()) & (df_mappings_t_missing["Attribute Name"].isnull())]
    print "Target Attributes Join Row is:", len(df_mappings_t_missing)
    print "Target Attributes Join Missing count is:", len(df_mappings_t_missing_count)
    df_mappings_t_missing = df_mappings_t_missing[(df_mappings_t_missing["Entity Name"].isnull()) & (df_mappings_t_missing["Attribute Name"].isnull())]
    df_mappings_t_missing.to_csv(output_csv_folder_path+"Mapping_Fields_Missing_T_E_A.csv",sep=",",columns=["Target System Name","Target Instance Name","Target Entity Name","Target Attribute Name"],index=None)
    '''
    for row in range(1,len(df_mappings)):
     print df_mappings.loc[row, "Target Attribute Name"]
    '''
def getPreviouslyLoadedResources(resouce_type,list):
    if(len(list)>0):

        folder = "C:/MDR/Data/Repository/CSV_Sharepoint_Output/loading/Batch_"
            #     "+resouce_type+"_Load_"

        list_dfs = []
        for i in list:
            file_name = folder+str(i)+"/BTP_MDR_"+resouce_type+"_Load_"+str(i)+".csv"
            #print file_name
            if(os.path.exists(file_name)):
                #print "Found file:",file_name
                #df.append(pd.read_csv(file_name,sep=","))
                #df = pd.read_csv(file_name, sep=",")
                #list_dfs.append(df)
                pass
            else:
                # print "ERROR: \n FILE_NAME: {} does not exist. Please check and run the program.".format(file_name)
                # print "Exiting the program."
                exit("Check file: "+file_name)

            df = pd.read_csv(file_name, sep=",")
            list_dfs.append(df)


        df_container = pd.concat(list_dfs)

        '''
        if(resouce_type == "Objects"):
            df_container["Entity Name"]     = df_container["Entity Name"].str.upper()
            df_container["Attribute Name"]  = df_container["Attribute Name"].str.upper()

        if (resouce_type == "Mappings"):
            df_container["Source Entity Name"]    = df_container["Source Entity Name"].str.upper()
            df_container["Source Attribute Name"] = df_container["Source Attribute Name"].str.upper()
            df_container["Target Entity Name"]    = df_container["Target Entity Name"].str.upper()
            df_container["Target Attribute Name"] = df_container["Target Attribute Name"].str.upper()
        '''

        #print "Total {} items from previous load: {} ".format(resouce_type,len(df_container))

        return df_container
    else:
        df_container = pd.DataFrame()
        return df_container

def getPreviouslyLoadedMappings(list):

    for i in list:
        print "BTP_MDR_Mappings_Load_"+str(i)+".csv"


def getObjectsForLoad(load_batch_number):
    print "\n####################   getObjectsForLoad({})  ####################\n".format(load_batch_number)
    # columns required in the output csv file [Objects]
    columns_objects_csv = ["System Name", "Instance Name", "Entity Name", "Attribute Name", "Owner", "Parent", "Type","Description","URL","Document Name","XPATH"]

    # read the Mapping file
    #df = pd.read_csv(output_csv_folder_path + 'Objects.csv', sep=",")
    df = pd.read_csv(output_csv_folder_path + 'BTP_Phase2_Objects.csv', sep=",")
    df_count_full_set = len(df)

    # do the filtering
        # get the list of items we want
    df_filter = pd.read_excel(output_csv_folder_path + 'control\\MDR_LOADING.xlsx',sheetname="Objects")
    df_filter = df_filter[df_filter["Status"].str.upper() == "Open".upper()]

    #entity_names_list = df_filter["Entity Name"]
    entity_names_list = df_filter["System Name"]

    print df_filter
    ## previous load batch numbers
    print "Objects [Phase 2 Full set] = {} ".format(df_count_full_set)
    ## Batch 1 - lower case, so reloaded in Batch 4. Batch 2 and 3 - does not exist.
    #df_objects_prev = getPreviouslyLoadedResources("Objects", [])
    df_objects_prev = getPreviouslyLoadedResources("Objects", getBatchDetails("Completed"))

    print "Objects [Phase 2 Previously Loaded] = {} ".format(len(df_objects_prev))
    ## concat Full set(df) and Previous sets (df_objects_prev)
    ## drop duplicates - All (keep=False)
    object_duplicated_by_columns = ["System Name", "Entity Name", "Attribute Name", "Type"]
    #object_duplicated_by_columns = ["Entity Name", "Attribute Name","Type"]

        #contacted dataframe
    df_delta = pd.concat([df,df_objects_prev])

        #cache duplicates
    df_delta_duplicates = df_delta[df_delta.duplicated(subset=object_duplicated_by_columns, keep=False)]
    print "Duplicates [All Phase 2] - [Phase 2.1] = {} ".format(len(df_delta_duplicates))
        #drop duplicates
    #df_delta_dropped = df_delta.drop_duplicates(subset=object_duplicated_by_columns, keep=False,inplace=True)
    df_delta.drop_duplicates(subset=object_duplicated_by_columns, keep=False, inplace=True)
    #df_delta.reset_index()
    print "Objects Delta [All in Phase 2] - [Phase 1] - [Phase 2.1] = {} ".format(len(df_delta))

    #use the Full set - Previous Load = For Loading

        #filer by the load control settings
    #df_load = df[df["System Name"].isin(entity_names_list)]
    df_load = df_delta[df_delta["System Name"].isin(entity_names_list)]
    #df_load = df_delta_dropped[df_delta_dropped["System Name"].isin(entity_names_list)]

    # write to a csv file - that is ready for MDR loading
    load_file_name = output_csv_folder_path + "loading\\BTP_MDR_Objects_Load_"+str(load_batch_number)+".csv"
    df_load.to_csv(load_file_name, sep=",", header=True, index=None,columns=columns_objects_csv)
    print "Objects For New Load (Batch {}) [Controlled] = {} ".format(load_batch_number, len(df_load))
    print "\n\nLoad File Generated: {}".format(load_file_name)

def getMappingsForLoad(load_batch_number):
    print "\n####################   getMappingsForLoad({})  ####################\n".format(load_batch_number)
    columns_mappings_csv = ["Source System Name", "Source Instance Name", "Source Entity Name", "Source Attribute Name",
                            "Target System Name", "Target Instance Name", "Target Entity Name", "Target Attribute Name",
                            "Attribute Description", "Business Rule", "Transformation_Mapping rule", "Comments",
                            "Mapping Name", "Action", "Last_Update_Date", "Modified_By"]

    # read the Mapping file
    #df = pd.read_csv(output_csv_folder_path + 'Mappings.csv', sep=",")
    df = pd.read_csv(output_csv_folder_path + 'BTP_Phase2_Mappings.csv', sep=",")
    df_count_full_set = len(df)

    df.dropna(subset=["Target Attribute Name"],inplace=True)
    # do the filtering
        # get the list of items we want
    df_filter = pd.read_excel(output_csv_folder_path + 'control\\MDR_LOADING.xlsx',sheetname="Mappings")
    df_filter = df_filter[df_filter["Status"].str.upper() == "Open".upper()]

    entity_names_list_source = df_filter["Source System Name"]
    entity_names_list_target = df_filter["Target System Name"]

    print df_filter

    print "Mappings [Phase 2 Full set] = {} ".format(df_count_full_set)
        ## Batch 1 - lower case, so reloaded in Batch 4. Batch 2 and 3 - does not exist.
    #df_mappings_prev = getPreviouslyLoadedResources("Mappings", [])
    df_mappings_prev = getPreviouslyLoadedResources("Mappings", getBatchDetails("Completed"))
    print "Mappings [Phase 2 Previously Loaded] = {} ".format(len(df_mappings_prev))

    ## concat Full set(df) and Previous sets (df_objects_prev)
    ## drop duplicates - All (keep=False)
    mapping_duplicated_by_columns = ["Source Entity Name", "Source Attribute Name", "Target Entity Name","Target Attribute Name"]

        #contacted dataframe
    df_delta = pd.concat([df,df_mappings_prev])

        #cache duplicates
    df_delta_duplicates = df_delta[df_delta.duplicated(subset=mapping_duplicated_by_columns, keep=False)]
    print "Duplicates [All Phase 2] - [Phase 2.1] = {} ".format(len(df_delta_duplicates))
        #drop duplicates
    df_delta.drop_duplicates(subset=mapping_duplicated_by_columns, keep=False,inplace=True)
    print "Mappings Delta [All in Phase 2] - [Phase 1] - [Phase 2.1] = {} ".format(len(df_delta))


    #use the Full set - Previous Load = For Loading

        #filer by the load control settings

    #df_load = df[df["Source System Name"].isin(entity_names_list_source) & df["Target System Name"].isin(entity_names_list_target)]
    df_load = df_delta[df_delta["Source System Name"].isin(entity_names_list_source) & df_delta["Target System Name"].isin(entity_names_list_target)]

    # remove the mappings with blank Target Entity Name
    df_load = df_load[df_load["Target Entity Name"].notnull()]

    print "Mappings For New Load (Batch {}) [Controlled] = {} ".format(load_batch_number, len(df_load))

    # write to a csv file - that is ready for MDR loading
    load_file_name = output_csv_folder_path + "loading\\BTP_MDR_Mappings_Load_"+str(load_batch_number)+".csv"
    df_load.to_csv(load_file_name, sep=",", header=True, index=None,columns=columns_mappings_csv)
    print "\n\n Load File Generated: {}".format(load_file_name)

def getSharepointList_Totals_From_Sharepoint_AllPhases():
    totals_dict = {}

    #totals_dict[] = 100
    totals_dict[list_name_screen_master] = len(sharepointListRowsByListName(list_name_screen_master))
    totals_dict[list_name_screen_fields] = len(sharepointListRowsByListName(list_name_screen_fields))
    totals_dict[list_name_visualmap_master] = len(sharepointListRowsByListName(list_name_visualmap_master))
    totals_dict[list_name_visualmap_fields] = len(sharepointListRowsByListName(list_name_visualmap_fields))
    totals_dict[list_name_ifs_mater] = len(sharepointListRowsByListName(list_name_ifs_mater))
    totals_dict[list_name_ifs_fields] = len(sharepointListRowsByListName(list_name_ifs_fields))
    totals_dict[list_name_xsd_master] = len(sharepointListRowsByListName(list_name_xsd_master))
    totals_dict[list_name_xsd_fields] = len(sharepointListRowsByListName(list_name_xsd_fields))

    # totals_dict[list_name_ldm_master] = len(sharepointListRowsByListName(list_name_ldm_master))
    # totals_dict[list_name_ldm_fields] = len(sharepointListRowsByListName(list_name_ldm_fields))
    #
    totals_dict[list_name_mapping_ifs_xsd] = len(sharepointListRowsByListName(list_name_mapping_ifs_xsd))
    totals_dict[list_name_mapping_screen_visualmap] = len(sharepointListRowsByListName(list_name_mapping_screen_visualmap))
    totals_dict[list_name_mapping_visualmap_ifs] = len(sharepointListRowsByListName(list_name_mapping_visualmap_ifs))

    #totals_dict[list_name_mapping_xsd_ldm] = len(sharepointListRowsByListName(list_name_mapping_xsd_ldm))

    # for key,value in totals_dict.items():
    #     print " Key = {} and Value = {} ".format(key,value)
    #
    df = pd.DataFrame(totals_dict.items(),columns=["Entity Name","Total"])
    df.to_csv(output_csv_folder_path + "Sharepoint_Rows_Total.csv",sep=",",header=True,index=None)
    #return df
    return totals_dict

def sendSharepointListTotals_To_CSV_File():

    #totals_dict_global
    # print type(totals_dict_global)
    # print totals_dict_global
    # df = pd.DataFrame(totals_dict_global.items(), columns=["Entity Name", "Total"])
    #
    #totals_list_objects_global = []

    # setTotal("Screen kdjfdk 4", 10,4)
    # setTotal("Screen dfldh 2", 10,2)
    # setTotal("Screen dfkdjfdk 5", 10,5)

    #totals_object_1 = {"Entity Name":"Screen 1", "Total":10,"DisplayOrder":2}
    #totals_object_2 = {"Entity Name":"Screen 2", "Total":10,"DisplayOrder":1}
    #totals_object_3 = {"Entity Name":"Screen 3", "Total":10,"DisplayOrder":3}
    #totals_list_objects_global.append(totals_object_1)
    #totals_list_objects_global.append(totals_object_2)
    #totals_list_objects_global.append(totals_object_3)


    df = pd.DataFrame(totals_list_objects_global, columns=["Entity Name", "Total","DisplayOrder"])
    df.sort_values(by=['DisplayOrder'],inplace=True)

    df.to_csv(output_csv_folder_path + "Sharepoint_Rows_Phase_2_Total.csv", sep=",", header=True, index=None)

def getSharepointListTotals_From_CSV_File(phase):
    totals_dict = {"Entity Name":"-","Total":"-","DisplayOrder":"1"}

    totals_list = []

    try:

        if (phase == 0):
            totals_df = pd.read_csv(output_csv_folder_path + "Sharepoint_Rows_Total.csv", sep=",")
        if (phase == 1):
            totals_df = pd.read_csv(output_csv_folder_path + "Sharepoint_Rows_Phase_1_Total.csv", sep=",")
        if (phase == 2):
            totals_df = pd.read_csv(output_csv_folder_path + "Sharepoint_Rows_Phase_2_Total.csv", sep=",")

        totals_list = totals_df.to_dict(orient='records')

        total = 0
        for item in totals_list:
            #print "\n {}. Sharepoint List Name and Total Records: {} #{}".format(item["DisplayOrder"],item["Entity Name"],item["Total"])
            total = total + item["Total"]

        print "\n Sharepoint Records for Phase 2 - Total Records = {}".format(total)

        total = {"Entity Name": "Overall Total", "Total": total}
        totals_list.append(total)

        return totals_list

    except:
        print "IO Error \n"
        print "Check whether the CSV file 'Sharepoint_Rows_Phase_2_Total.csv' exists in the below folder\n"
        print "Folder Name: C:\MDR\Data\Repository\CSV_Sharepoint_Output\n"
        totals_list.append(totals_dict)
        return totals_list

def joinDF():
    df_mapping_ux_vm = pd.read_csv(output_csv_folder_path+"Mapping_ux_vm.csv",sep=",")
    print df_mapping_ux_vm.head()

    mapping_vm_ifs = pd.read_csv(output_csv_folder_path + "Mapping_vm_ifs.csv", sep=",")
    print mapping_vm_ifs.head()

    mapping_ifs_xsd = pd.read_csv(output_csv_folder_path + "Mapping_ifs_xsd.csv", sep=",")
    print mapping_ifs_xsd.head()

    mapping_xsd_ldm = pd.read_csv(output_csv_folder_path + "Mapping_xsd_ldm.csv", sep=",")
    print mapping_xsd_ldm.head()

    left_columns_target    = ["Target Entity Name","Target Attribute Name"]
    left_columns_abs_target = ["Target_Entity_Name_ABS_D", "Target_Attribute_Name_ABS_D"]
    right_columns_source   = ["Source Entity Name","Source Attribute Name"]
    left_columns_target_y  = ["Target Entity Name_y","Target Attribute Name_y"]

    join_how = 'inner'

    print "################## {} JOIN - Level 1 ##############################################".format(join_how)
    merged_ux_vm_vm_ifs = pd.merge(left=df_mapping_ux_vm, right=mapping_vm_ifs, left_on=left_columns_target, right_on=right_columns_source, how=join_how,sort=True)
    merged_ux_vm_vm_ifs = merged_ux_vm_vm_ifs.fillna('-')
    print merged_ux_vm_vm_ifs.head()
    merged_ux_vm_vm_ifs.to_csv(output_csv_folder_path + "Merged_ux_vm_vm_ifs_" +join_how+".csv", sep=",", index=False, header=True)

    print "################## {} JOIN - Level 2 ##############################################".format(join_how)

    merged_ux_vm_vm_ifs_ifs_xsd = pd.merge(left=merged_ux_vm_vm_ifs, right=mapping_ifs_xsd, left_on=left_columns_target_y, right_on=right_columns_source, how=join_how,sort=True)
    merged_ux_vm_vm_ifs_ifs_xsd = merged_ux_vm_vm_ifs_ifs_xsd.fillna('-')
    print merged_ux_vm_vm_ifs_ifs_xsd.head()
    merged_ux_vm_vm_ifs_ifs_xsd.to_csv(output_csv_folder_path + "Merged_ux_vm_vm_ifs_ifs_xsd_" +join_how+".csv", sep=",", index=False, header=True)

    print "################## {} JOIN - Level 3 ##############################################".format(join_how)

    merged_ux_vm_vm_ifs_ifs_xsd_xsd_ldm = pd.merge(left=merged_ux_vm_vm_ifs_ifs_xsd, right=mapping_xsd_ldm, left_on=left_columns_abs_target, right_on=right_columns_source, how=join_how,sort=True)
    merged_ux_vm_vm_ifs_ifs_xsd_xsd_ldm = merged_ux_vm_vm_ifs_ifs_xsd_xsd_ldm.fillna('-')
    print merged_ux_vm_vm_ifs_ifs_xsd_xsd_ldm.head()
    merged_ux_vm_vm_ifs_ifs_xsd_xsd_ldm.to_csv(output_csv_folder_path + "Merged_ux_vm_vm_ifs_ifs_xsd_xsd_ldm_" +join_how+".csv", sep=",", index=False, header=True)

def MatchXSD():

    # columns required in the output csv file [Objects]
    control_limit = 0.80
    columns_mappings_csv = ["Source System Name", "Source Instance Name", "Source Entity Name", "Source Attribute Name",
                            "Target System Name", "Target Instance Name", "Target Entity Name", "Target Attribute Name",
                            "Attribute Description", "Business Rule", "Transformation_Mapping rule", "Comments",
                            "Mapping Name", "Action", "Last_Update_Date", "Modified_By"]
    columns_mappings_csv_subset = ["Source System Name", "Source Instance Name", "Source Entity Name", "Source Attribute Name","Business Rule", "Comments"]

    columns_mappings_abs_csv = ["Source System Name", "Source Instance Name", "Source Entity Name",
                                "Source Attribute Name", "Target System Name", "Target Instance Name",
                                "Target Entity Name", "Target Attribute Name", "Target_Entity_Name_ABS_D",
                                "Target_Attribute_Name_ABS_D", "Attribute Description", "Business Rule",
                                "Transformation_Mapping rule", "Comments", "Mapping Name", "Action", "Last_Update_Date",
                                "Modified_By"]
    columns_mappings_abs_csv_subset = [
                                "Target Entity Name", "Target Attribute Name", "Target_Entity_Name_ABS_D",
                                "Target_Attribute_Name_ABS_D", "Attribute Description", "Business Rule",
                                "Transformation_Mapping rule", "Comments", "Mapping Name","Action"]

    # "Mapping_IFS_XSD All"
    row_mappings_ifs_xsd_all = getMapping_IFS_XSD_All(list_name_mapping_ifs_xsd)
    #df_mapping_ifs_xsd = pd.DataFrame(row_mappings_ifs_xsd_all, columns=columns_mappings_abs_csv)
    #df_mapping_ifs_xsd.to_csv(output_csv_folder_path + "Mapping_ifs_xsd_all.csv", sep=",", header=True, index=None)

    df_mapping_ifs_xsd_subset = pd.DataFrame(row_mappings_ifs_xsd_all, columns=columns_mappings_abs_csv_subset)
    #df_mapping_ifs_xsd_subset.to_csv(output_csv_folder_path + "Mapping_ifs_xsd_all_subset.csv", sep=",", header=True, index=None)
    df_mapping_ifs_xsd_subset.insert(0,"Cleansed Entity Name","")

    # "Mapping_XSD_LDM All"
    row_mappings_xsd_ldm_all = getMapping_XSD_LDM_All(list_name_mapping_xsd_ldm)
    #df_mapping_xsd_ldm = pd.DataFrame(row_mappings_xsd_ldm_all, columns=columns_mappings_csv)
    #df_mapping_xsd_ldm.to_csv(output_csv_folder_path + "Mapping_xsd_ldm_all.csv", sep=",", header=True, index=None)

    df_mapping_xsd_ldm_subset = pd.DataFrame(row_mappings_xsd_ldm_all, columns=columns_mappings_csv_subset)
    #df_mapping_xsd_ldm_subset.to_csv(output_csv_folder_path + "Mapping_xsd_ldm_all_subset.csv", sep=",", header=True, index=None)

    # for j in range(0, len(df_mapping_xsd_ldm_subset)):
    #     print df_mapping_xsd_ldm_subset.loc[j, "Source Entity Name"]
    #
    list_of_strings = df_mapping_xsd_ldm_subset["Source Entity Name"]

    for i in range(0,len(df_mapping_ifs_xsd_subset)):
        #print df_mapping_ifs_xsd_subset.loc[i,"Target Entity Name"]
        if(i<3000):
            output_list_sequence_match = SeqMatch(df_mapping_ifs_xsd_subset.loc[i,"Target Entity Name"], list_of_strings, control_limit)
            df_mapping_ifs_xsd_subset.loc[i,"Cleansed Entity Name"] = output_list_sequence_match
            #print output_list_sequence_match


    df_mapping_ifs_xsd_subset.to_csv(output_csv_folder_path + "Mapping_ifs_xsd_all_subset.csv", sep=",", header=True, index=None)

if __name__ == "__main__":

    start = time.time()
    localtime_start = time.asctime(time.localtime(start))
    localtime_end = time.asctime(time.localtime(start + 1200))
    print "Start time: {}".format(localtime_start)
    print "ETA: 20 mins i.e. {} ".format(localtime_end)

    #######################START LOADING################################
    print "Batch status 'Completed' = {}".format(getBatchDetails("Completed"))
    print "Batch status 'WIP' = {}".format(getBatchDetails("WIP")[0])

        #extract Objects & Mappings for a given MDR Phase (i.e. Phase 1, Phase 2)
    buidObjects(GP_PHASE_NO)
    buildMapings(GP_PHASE_NO)

        #check and remove duplicates between Phase 1 and Phase 2 - Should be called before getObjectsForLoad() and getMappingsForLoad()
        #Output: BTP_Phase2_Objects.csv / BTP_Phase2_Mappings.csv
    checkPhase1_2_Duplicates()

    #check if the attributes in the mapping sheet has been defined in the object sheet, as
    # if the mapping attributes are not in objects - the MDR loading will fail.
        ##Check just the attributes. But this is dangerous, as the same attribute will be there in multiple entities.
    checkAttributes()

        ##So, Check just the attributes. But this is dangerous, as the same attribute will be there in multiple entities.
    checkAttributesByJoin('left')

    #extract Objects & Mappings for Dataloading based on the load control settings
    getObjectsForLoad(getBatchDetails("WIP")[0])
    getMappingsForLoad(getBatchDetails("WIP")[0])
    ####################### END LOADING################################

    end = time.time()
    print "Execution time: {} mins".format((end - start) / 60)

    ###Testing
# getObjectsByPhase(list_name_bt_icc_xsd_fields,GP_PHASE_NO)
# getObjectsByPhase(list_name_gesb_ifs_fields,GP_PHASE_NO)
# getObjects(list_name_xsd_fields_abs)

# getMappingsByPhase(list_name_mapping_VM_ESB_XSD,GP_PHASE_NO,0)
# getMappingsByPhase(list_name_mapping_VM_ESB_IFS,GP_PHASE_NO,0)
#getMappingsByPhase(list_name_mapping_BTICC_XSD_ABS_XSD,GP_PHASE_NO,1)

#Join all the Mapping Files to get the Lineage
#joinDF()

#Match Mapping_IFS_XSD (from IFS) with Mapping_XSD_LDM (from Avaloq report)
    #Takes more time as it matches each of the XSD field from IFS with a possible value from Avaloq. So run this only when needed
# MatchXSD()

### Get the previouslyloaded resources in Phase 2 i.e. 2.1, 2.2 etc (Batch)
# getPreviouslyLoadedResources("Objects",[1])
# getPreviouslyLoadedResources("Mappings",[1])


#getPreviouslyLoadedMappings([1])

#sharepointTotal_list = getSharepointListTotals_From_CSV_File(2)
#sendSharepointListTotals_To_CSV_File()



#print type(sharepointTotal_list)

#sharepointTotal_dict = getSharepointList_Totals_From_Sharepoint_AllPhases()

# DataFrame -
#sharepointTotal_df = getSharepointList_Totals_From_Sharepoint_AllPhases()
# sharepointTotal_df.info()
# print sharepointTotal_df.head()

# print sharepointTotal_df[0][0], sharepointTotal_df[0][1]
# print sharepointTotal_df[0][0], sharepointTotal_df[1][0]

#print sharepointTotal_df.loc[sharepointTotal_df['Total'] == sharepointTotal_df['Entity Name'] == "XSD Master"]
#print sharepointTotal_df.get_value(sharepointTotal_df['Entity Name'] == 'XSD Master','Total')
#getBatchDetails("Open")
# print getBatchDetails("Completed")
# print getBatchDetails("WIP")[0]
#getBatchDetails_WIP()