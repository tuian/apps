from sharepoint import SharePointSite
from ntlm import HTTPNtlmAuthHandler

import base64
import urllib2


# Global Variabls (GV)
GV_SHAREPOINT_URL = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam"
GV_SHAREPOINT_LIST_NAME = "Projection master invoice"
GV_USERNAME = "L083646"
GV_PASSWORD = base64.b64decode("VENTIzIzMDU=")
GV_OUTPUT_FOLDER = "C:/apps/apps/tcsbt/Data/output/"
GV_INPUT_FOLDER = "C:/apps/apps/tcsbt/Data/input/"
GV_INPUT_FILE = "RESOURCE_TEAM_MAPPING.xlsx"

def getSharepointURL():
    return GV_SHAREPOINT_URL

def getPassword(username):
    return GV_PASSWORD

def setPassword():
    print "Enter your username:"
    print "Enter your password:"
    GV_PASSWORD = "ABC"

def getUsername():
    return GV_USERNAME

def setUsername():
    GV_USERNAME = "L083646"

def encode_string(string):
    return base64.b64encode(string)


def decode_string(string):
    return base64.b64decode(string)


def getSharepointListRowsByListName(list_name):

    site_url = getSharepointURL()
    username = getUsername()
    password = getPassword(username)

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


def displayRowFields(rows):

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


def createFolderPath(folder_path):

    import os
    #Usage:
    #createFolderPath('C:\TEST\\')

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except IOError:
        print "ERROR: Unable to create the folder " + folder_path

#default folders setup
createFolderPath(GV_INPUT_FOLDER)
createFolderPath(GV_OUTPUT_FOLDER)

#displayRowFields(getSharepointListRowsByListName(GV_SHAREPOINT_LIST_NAME))