#encoding=utf8
import sys

import csv
import pandas as pd
from pandas import DataFrame, read_csv
from mdr_util import *


# print('Python version ' + sys.version)
# print('Pandas version ' + pd.__version__)
reload(sys)
sys.setdefaultencoding('utf8')

#Global Parameter to define the Metadata Project Phase

GP_PHASE_NO = "Phase 2"

list_name_screen_master = "Screen Master"
list_name_screen_fields = "Screen Fields"

list_name_visualmap_master = "Visual Map Master"
list_name_visualmap_fields = "Visual Map Fields"

list_name_ifs_mater = "IFS Master"
list_name_ifs_fields = "IFS Fields"

list_name_xsd_master = "XSD Master"
list_name_xsd_fields = "XSD Fields"

list_name_ldm_master = "ABS_LDM_Master"
list_name_ldm_fields = "ABS_LDM_Fields"

list_name_mapping_ifs_xsd = "Mapping_IFS_XSD"
list_name_mapping_screen_visualmap = "Mapping_Screen_VisualMap"
list_name_mapping_visualmap_ifs = "Mapping_VisualMap_IFS"
list_name_mapping_xsd_ldm = ""

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
            row_object["Entity Name"] = row.Entity_x0020_Name
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = row.Entity_x0020_Type
            row_object["Description"] = ""
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_ScreenMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["Entity Name"] = str(row.Entity_Name_D).encode("utf-8")
            row_object["Attribute Name"] = str(row.Attribute_Name)
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = str(row.Entity_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Description)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_ScreenFields('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["Entity Name"] = str(row.Entity_Name).encode("utf-8")
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = "Visual Map"
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Funtionality)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_VisualMapMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["Entity Name"] = str(row.Title).encode("utf-8") #Entity Name Duplicate
            row_object["Attribute Name"] = str(row.Attribute_x0020_Name)
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = str(row.Entity_x0020_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Description)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_VisualMapFields('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["Instance Name"] = "Default" # static text default
            row_object["Entity Name"] = str(row.Title).encode("utf-8")
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = "Interface"
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Notes)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_IFSMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["Entity Name"] = str(row.Entity_Name_Duplicate).encode("utf-8")
            row_object["Attribute Name"] = str(row.Attribute_Name)
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = str(row.Entity_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Description)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_IFSFields('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["Entity Name"] = str(row.Title).encode("utf-8")
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = str(row.Entity_x0020_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Functionality)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_XSDMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["Entity Name"] = str(row.Entity_Name_Duplicate).encode("utf-8")
            row_object["Attribute Name"] = str(row.Attribute_Name)
            row_object["Owner"] = str(row.Owner).encode("utf-8")
            row_object["Parent"] = str(row.Parent).encode("utf-8")
            row_object["Type"] = str(row.Entity_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Description)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_XSDFields('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["System Name"] = "ABS Dev"
            row_object["Instance Name"] = "Default"
            row_object["Entity Name"] = str(row.Title).encode("utf-8")
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = str(row.Entity_x0020_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Functionality)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_XSDMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    return list_objects

#LDM Fields - Object
def getObject_LDMFields(list_name,mdr_phase_no):

    reload(sys)
    sys.setdefaultencoding('utf8')

    list_objects = []

    rows = sharepointListRowsByListName(list_name)

    for row in rows:
        if ((row.MDR_x0020_Release_x0020_Period).upper() == mdr_phase_no.upper()):
            row_object = {}
            row_object["System Name"] = "ABS Dev"
            row_object["Instance Name"] = "Default"
            row_object["Entity Name"] = str(row.Title).encode("utf-8")
            row_object["Attribute Name"] = ""
            row_object["Owner"] = ""
            row_object["Parent"] = ""
            row_object["Type"] = str(row.Entity_x0020_Type).encode("utf-8")
            #row_object["Description"] = str(row.Description).encode("utf-8")
            row_object["Description"] = cleanHTMLTags(row.Functionality)
            # row_object[""] = row.
            list_objects.append(row_object)
    print "getObject_XSDMaster('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["Source Entity Name"] = row.Source_Entity_Name_D
            row_object["Source Attribute Name"] = row.Source_Attribute_Name0
            row_object["Target System Name"] = row.Target_System_Name
            row_object["Target Instance Name"] = row.Target_Instance_Name
            row_object["Target Entity Name"] = row.Target_Entity_Name_D
            row_object["Target Attribute Name"] = row.Target_Attribute_Name_D
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
            row_object["Source Instance Name"] = row.Title
            row_object["Source Entity Name"] = row.Source_Entity_Name_D
            row_object["Source Attribute Name"] = row.Source_Attribute_Name_Duplicate
            row_object["Target System Name"] = row.Target_System_Name
            row_object["Target Instance Name"] = row.Target_Instance_Name
            row_object["Target Entity Name"] = row.Target_Entity_Name_D
            row_object["Target Attribute Name"] = row.Target_Attribute_Name_Duplicate
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
            row_object["Source Entity Name"] = row.Source_Entity_Name_Duplicate
            row_object["Source Attribute Name"] = row.Source_Attribute_Name_Duplicate
            row_object["Target System Name"] = row.Target_System_Name
            row_object["Target Instance Name"] = row.Target_Instance_Name
            row_object["Target Entity Name"] = row.Target_Entity_Name_Duplicate
            row_object["Target Attribute Name"] = row.Target_Attribute_Name_Duplicate
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
    print "getMapping_IFS_XSD('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
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
            row_object["Source Instance Name"] = row.Title
            row_object["Source Entity Name"] = row.Source_Entity_Name_Duplicate
            row_object["Source Attribute Name"] = row.Source_Attribute_Name_Duplicate
            row_object["Target System Name"] = row.Target_System_Name
            row_object["Target Instance Name"] = row.Target_Instance_Name
            row_object["Target Entity Name"] = row.Target_Entity_Name_Duplicate
            row_object["Target Attribute Name"] = row.Target_Attribute_Name_Duplicate
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
    print "getMapping_XSD_LDM('{}','{}') = ".format(list_name, mdr_phase_no), len(list_objects)
    return list_objects

def buidObjects():
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

    # row_objects_ldm = getObject_LDMMaster(list_name_ldm_master,GP_PHASE_NO)
    # row_objects_ldm = getObject_LDMFields(list_name_ldm_fields,GP_PHASE_NO)
    #row_objects_ldm = getObject_LDMMaster(list_name_ldm_master,GP_PHASE_NO) + getObject_LDMFields(list_name_ldm_fields,GP_PHASE_NO)

    #columns required in the output csv file [Objects]
    columns_objects_csv = ["System Name","Instance Name","Entity Name","Attribute Name","Owner","Parent","Type","Description"]



    df_ux = pd.DataFrame(row_objects_ux,columns=columns_objects_csv)
    df_ux.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Objects_ux.csv",sep=",",header=True,index=None)

    df_vm = pd.DataFrame(row_objects_vm,columns=columns_objects_csv)
    df_vm.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Objects_vm.csv",sep=",",header=True,index=None)

    df_ifs = pd.DataFrame(row_objects_ifs,columns=columns_objects_csv)
    df_ifs.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Objects_ifs.csv",sep=",",header=True,index=None)


    df_xsd = pd.DataFrame(row_objects_xsd,columns=columns_objects_csv)
    df_xsd.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Objects_xsd.csv",sep=",",header=True,index=None)

    #df_ldm = pd.DataFrame(row_objects_ldm,columns=columns_objects_csv)
    #df_ldm.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Objects_ldm.xsd",sep=",",header=True,index=None)

    df_frames = [df_ux,df_vm,df_ifs,df_xsd]
    df = pd.concat(df_frames)

    df.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Objects.csv",sep=",",header=True,index=None)

    # df.info()
    # df.describe()
    # print df.head().to_string()
    # print df.tail().to_string()

    #Objects End


def buildMapings():

    #columns required in the output csv file [Objects]
    columns_mappings_csv = ["Source System Name","Source Instance Name","Source Entity Name","Source Attribute Name","Target System Name","Target Instance Name","Target Entity Name","Target Attribute Name","Attribute Description","Business Rule","Transformation_Mapping rule","Comments","Mapping Name","Action","Last_Update_Date","Modified_By"]

    #"Mapping_Screen_VisualMap"
    row_mappings_ux_vm = getMapping_UX_VM(list_name_mapping_screen_visualmap, GP_PHASE_NO)
    df_mapping_ux_vm = pd.DataFrame(row_mappings_ux_vm, columns=columns_mappings_csv)
    df_mapping_ux_vm.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Mapping_ux_vm.csv",sep=",",header=True,index=None)

    #"Mapping_VisualMap_IFS"
    row_mappings_vm_ifs = getMapping_VM_IFS(list_name_mapping_visualmap_ifs, GP_PHASE_NO)
    df_mapping_vm_ifs = pd.DataFrame(row_mappings_vm_ifs, columns=columns_mappings_csv)
    df_mapping_vm_ifs.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Mapping_vm_ifs.csv",sep=",",header=True,index=None)

    #"Mapping_IFS_XSD"
    row_mappings_ifs_xsd  = getMapping_IFS_XSD(list_name_mapping_ifs_xsd,GP_PHASE_NO)
    df_mapping_ifs_xsd = pd.DataFrame(row_mappings_ifs_xsd,columns=columns_mappings_csv)
    df_mapping_ifs_xsd.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Mapping_ifs_xsd.csv",sep=",",header=True,index=None)

    # "Mapping_XSD_LDM"
    # row_mappings_xsd_ldm = getMapping_XSD_LDM(list_name_mapping_xsd_ldm, GP_PHASE_NO)
    # df_mapping_ifs_xsd = pd.DataFrame(row_mappings_xsd_ldm, columns=columns_mappings_csv)
    # df_mapping_ifs_xsd.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Mapping_ifs_xsd.csv",sep=",",header=True,index=None)

    df_frames = [df_mapping_ux_vm, df_mapping_vm_ifs, df_mapping_ifs_xsd]
    df = pd.concat(df_frames)

    df.to_csv("C:\\01 BT\\00 MDR\\Phase2\\Loading\\Mappings.csv", sep=",", header=True, index=None)

    # df.info()
    # df.describe()
    # print df.head().to_string()
    # print df.tail().to_string()

    # Mapping Builder End

buidObjects()
buildMapings()
