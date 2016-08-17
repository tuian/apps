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

#site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"
site_url = "http://sharepoint.btfin.com/sites/trans/tech/architecture"
#site_url = "http://sharepoint.btfin.com/sites/trans/tech/architecture/Solution Design/Investment Platform/Web UI To Avaloq Integration/IFS/Visual Map/"
#site_url = "http%3A%2F%2Fsharepoint.btfin.com%2Fsites%2Ftrans%2Ftech%2Farchitecture%2FSolution%20Design%2FInvestment%20Platform%2FWeb%20UI%20To%20Avaloq%20Integration%2FIFS%2FVisual%20Map%2F"
list_name = "Solution Design"

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
workbook = xlsxwriter.Workbook("Visual_Map_Master_List.xlsx")

worksheet_Source = workbook.add_worksheet("Source - Visual Map Documents")
bold = workbook.add_format({'bold': 1});
worksheet_Source.write('A1', 'Visual Map Document Name', bold);
#worksheet_Source.write('B1', 'Attribute Name', bold)



# create a SharePointSite object
site = SharePointSite(site_url, opener)
sp_list = site.lists[list_name]

#file_path = '/sites/trans/tech/architecture/Solution Design/'
file_path = '/sites/trans/tech/architecture/Solution Design/Investment Platform/Web UI To Avaloq Integration/IFS/Visual Map/'
file_path_excluded = '/sites/trans/tech/architecture/Solution Design/Investment Platform/Web UI To Avaloq Integration/IFS/Visual Map/Archive'

visual_map_count = 0
visual_map_count_extended = 0


for row in sp_list.rows:
     if (bool(re.search(file_path, row.ServerUrl))):
         if(bool(re.search(file_path_excluded, row.ServerUrl))):
             visual_map_count_extended = visual_map_count_extended + 1
         else:
            visual_map_count = visual_map_count + 1
            print row.BaseName
            #print row.BaseName, ",",row.Modified,",",row._DCDateModified,",",row.File_x0020_Type,",",row.ServerUrl
            #print row.Created,row.Modified,row._DCDateModified
            #print row.is_file,row.Title,
            #print "Nones: ",row.Date,row.Date_x0020_stamp,row.Dateof_x0020_mod
            #print row.BaseName,row._IsCurrentVersion,row._SourceUrl,row.Created_x0020_Date
            #print row.fields

            worksheet_Source.write_string(visual_map_count, 0, row.BaseName)
            # worksheet.write_string(rows_length, 1, row.Entity_x0020_Type)

print visual_map_count

workbook.close();
"""
workbook_MDR = xlsxwriter.Workbook("Visual_Map_MDR_List.xlsx")

worksheet_MDR    = workbook_MDR.add_worksheet("MDR - Visual Map Documents")
bold = workbook_MDR.add_format({'bold': 1});
worksheet_MDR.write('A1', 'Visual Map Document Name', bold);


site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"
list_name = "Visual Map Master"

site_MDR = SharePointSite(site_url, opener)
sp_list_MDR = site_MDR.lists[list_name]


visual_map_count = 0

for row in sp_list_MDR.rows:
    visual_map_count = visual_map_count + 1
    print row.Title
    worksheet_MDR.write_string(visual_map_count, 0, row.Title)

print visual_map_count

   #sp_list = site.lists[list_name]

#print sp_list.id, sp_list.meta['Title']

#for row in sp_list.rows:

 #   print row.id, row.Title , row.Created,row.Author['name'],row.Entity_x0020_Type,row.L1
    #if (row.id==1):
        #print row.fields
  #  print row.Title ,row.Entity_x0020_Type , row._x004c_1 ,row._x004c_2 ,row._x004c_3
    #worksheet.write_string(rows_length, 0, row.Title)
    #worksheet.write_string(rows_length, 1, row.Entity_x0020_Type)

    #rows_length = rows_length + 1

    #for row in sp_list.rows:
     #print "Hello"

#print rows_length-1
workbook.close();



#for sp_list in site.lists:
#    print sp_list.id, sp_list.meta['Title']
# if current_project in row.Filename:
# basecase_rev = row.Rev

"""
