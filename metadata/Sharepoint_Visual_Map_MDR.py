import urllib2
from sharepoint import SharePointSite
from ntlm import HTTPNtlmAuthHandler
from getpass import getpass
import xlsxwriter
import sys
import os
import base64
import re


os.system('cls')  # for Windows

print "\n \n \t \t \t ##### Metadata Repository ##### \n \n"

#print base64.b64encode("")
#print base64.b64decode("VENTIzMxNjA=")


#reload(sys)
#sys.setdefaultencoding('utf8')

""""Sharepoint Details """

site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"
list_name = "Visual Map Master"
#list_name = "Mapping_VisualMap_IFS"
#list_name = "Mapping: IFS - XSD"
#list_name= "Mapping: Screen - Visual Map Fields"

""""Windows credentials """
#username ='AUAUTD0001\L083646'
username ='L083646'
#username = sys.argv[1]

#password = sys.argv[2]
password = base64.b64decode("VENTIzMxNjA=")
#password = getpass() # get the password. Enter the password when the prompt comes up

# an opener for the NTLM authentication
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, site_url, username, password)
auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

# create and install the opener
opener = urllib2.build_opener(auth_NTLM)
urllib2.install_opener(opener)


""""Variables Details """
rows_length = 1

""""Output Excel Sheet Details """
workbook_MDR = xlsxwriter.Workbook("Visual_Map_MDR_List.xlsx")
worksheet_MDR    = workbook_MDR.add_worksheet("MDR - Visual Map Documents")
bold = workbook_MDR.add_format({'bold': 1});
worksheet_MDR.write('A1', 'Visual Map Document Name', bold);



# create a SharePointSite object
site_MDR = SharePointSite(site_url, opener)
sp_list_MDR = site_MDR.lists[list_name]

visual_map_count = 0
visual_map_count_extended = 0


for row in sp_list_MDR.rows:
            visual_map_count = visual_map_count + 1
            #print row.Title
            print row.Title,row.Matchs_x0020_Sharepoint_x0020_VM
            #print row.BaseName, ",",row.Modified,",",row._DCDateModified,",",row.File_x0020_Type,",",row.ServerUrl
            #print row.Created,row.Modified,row._DCDateModified
            #print row.is_file,row.Title,
            #print "Nones: ",row.Date,row.Date_x0020_stamp,row.Dateof_x0020_mod
            #print row.BaseName,row._IsCurrentVersion,row._SourceUrl,row.Created_x0020_Date
            #print row.fields

            worksheet_MDR.write_string(visual_map_count, 0, row.Title)
            # worksheet.write_string(rows_length, 1, row.Entity_x0020_Type)

print visual_map_count

workbook_MDR.close();
