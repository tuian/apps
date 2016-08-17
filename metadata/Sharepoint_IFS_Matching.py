import urllib2
from sharepoint import SharePointSite
from ntlm import HTTPNtlmAuthHandler
from getpass import getpass
import xlsxwriter
import sys
import os
import base64
import re
import datetime
import mdr_util


os.system('cls')  # for Windows

print "\n \n \t \t \t ##### Metadata Repository ##### \n \n"
print "Matching program started. Please wait..."
start_time = datetime.datetime.now()
#print "Start Time:", start_time

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
#password = base64.b64decode("VENTIzMxNjA=")
password = mdr_util.getPassword()
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
count_flag_parent = 0
count_flag_child = 0

""""Output Excel Sheet Details """
workbook = xlsxwriter.Workbook("IFS_Comparison.xlsx")

worksheet_Source = workbook.add_worksheet("Sharepoint - IFS Documents")
bold = workbook.add_format({'bold': 1});
worksheet_Source.write('A1', 'IFS Document Name', bold);
worksheet_Source.write('B1', 'Sharepoint Location', bold);
#worksheet_Source.write('B1', 'Attribute Name', bold)
worksheet_Source.set_column(0, 2 ,100)


# create a SharePointSite object
site = SharePointSite(site_url, opener)
sp_list = site.lists[list_name]

#file_path = '/sites/trans/tech/architecture/Solution Design/'
file_path = '/sites/trans/tech/architecture/Solution Design/Investment Platform/Web UI To Avaloq Integration/IFS/'
file_path_excluded = '/sites/trans/tech/architecture/Solution Design/Investment Platform/Web UI To Avaloq Integration/IFS/Visual Map'

ifs_count = 0

parent_list_count = len(sp_list.rows)
sharepoint_ifs_count = 0

for row in sp_list.rows:

    #print row.ServerUrl

    if(re.search(file_path,row.ServerUrl)):
        if(row.ServerUrl.count('/') == 9 ):
            if(re.match(r'.*(.docx)$',row.ServerUrl)):
               sharepoint_ifs_count = sharepoint_ifs_count + 1



for row in sp_list.rows:
     if(re.search(file_path,row.ServerUrl)):
         if(row.ServerUrl.count('/') == 9 ):
            if(re.match(r'.*(.docx)$',row.ServerUrl)):
                ifs_count = ifs_count + 1
                worksheet_Source.write_string(ifs_count, 0, row.BaseName)
                #worksheet_Source.write_string(ifs_count, 1, row.ServerUrl)


parent_list_count = ifs_count
#print visual_map_count


""" """
#workbook_MDR = xlsxwriter.Workbook("Visual_Map_MDR_List.xlsx")
#worksheet_MDR    = workbook_MDR.add_worksheet("MDR - Visual Map Documents")
#bold = workbook.add_format({'bold': 1});

worksheet_MDR    = workbook.add_worksheet("MDR - IFS Documents")
worksheet_MDR.write('A1', 'MDR - IFS Document Name', bold);
worksheet_MDR.set_column(0, 2 ,100)


site_url_MDR = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"
list_name_MDR = "IFS Master"

passman2 = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman2.add_password(None, site_url_MDR, username, password)
auth_NTLM2 = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman2)
opener2 = urllib2.build_opener(auth_NTLM2)
urllib2.install_opener(opener2)

site_MDR = SharePointSite(site_url_MDR, opener2)
sp_list_MDR = site_MDR.lists[list_name_MDR]


MDR_IFS_count = 0

child_list_count = len(sp_list_MDR.rows)

for row in sp_list_MDR.rows:
    MDR_IFS_count = MDR_IFS_count + 1
    #print row.Title
    worksheet_MDR.write_string(MDR_IFS_count, 0, row.IFS_x0020_Object_x0020_Name)

#print visual_map_count

""" Comparison Results"""
worksheet_Results    = workbook.add_worksheet("Comparison Results")
worksheet_Results.write('A1', 'Application Name', bold);
worksheet_Results.write('B1', 'Entity Name', bold);
worksheet_Results.write('C1', 'IFS Document Name', bold);
worksheet_Results.write('D1', 'Phase', bold);
worksheet_Results.write('E1', 'MDR Scope', bold);
worksheet_Results.write('F1', 'URL', bold);
worksheet_Results.write('G1', 'Match Status', bold);

worksheet_Results.set_column(0, 0 ,15)
worksheet_Results.set_column(1, 1 ,15)


worksheet_Results_MDR_Sharepoint    = workbook.add_worksheet("Comparison - MDR to Sharepoint")
worksheet_Results_MDR_Sharepoint.write('A1', 'Document Name', bold);
worksheet_Results_MDR_Sharepoint.write('B1', 'Match Status', bold);
worksheet_Results_MDR_Sharepoint.write('C1', 'Remarks', bold);

worksheet_Results_MDR_Sharepoint.set_column(0, 0 ,120)
worksheet_Results_MDR_Sharepoint.set_column(1, 1 ,15)

ifs_count = 1

# Take items from the parent list i.e. List of Visual Maps from the sharepoint list

Match_Found_Count = 0
Match_NOT_Found_Count = 0
sp_entities_match_not_found = []

for row in sp_list.rows:
  if (re.search(file_path,row.ServerUrl)):
     if (row.ServerUrl.count('/') == 9):
        if(re.match(r'.*(.docx)$',row.ServerUrl)):
            Match_Found_Flag = 0;

            # For each item in parent list, loop through the child list (i.e. MDR IFS Maps List ) and find the match
            #child_rows_length = len(sp_list_MDR.rows)
            #print "Child rows length:",child_rows_length

            for row_MRD in sp_list_MDR.rows:
               #print "Child Document Names",row_MRD.Title
               # Parent == Child
                if (count_flag_parent == 0 & count_flag_child == 0):
                   #print row_MRD.fields
                   #print row_MRD.IFS_x0020_Object_x0020_Name
                   count_flag_parent = 1
                   count_flag_child = 1
                #print "Project file name: ",row.BaseName, " | MDR file name:",row_MRD.IFS_x0020_Object_x0020_Name
                if(row.BaseName == row_MRD.IFS_x0020_Object_x0020_Name):
                    Match_Found_Flag = 1;


            url_full = "http://sharepoint.btfin.com" + row.ServerUrl

            if(Match_Found_Flag == 1):
               Match_Found_Count = Match_Found_Count + 1
               worksheet_Results.write_string(ifs_count, 0, "IP")
               worksheet_Results.write_string(ifs_count, 1, "Entity Name")
               worksheet_Results.write_string(ifs_count, 2, row.BaseName)
               worksheet_Results.write_string(ifs_count, 3, "Phase 2")
               worksheet_Results.write_string(ifs_count, 4, "Yes")
               worksheet_Results.write_string(ifs_count, 5, url_full)
               worksheet_Results.write_string(ifs_count, 6, "Match")
               ifs_count = ifs_count + 1
            else:
                Match_NOT_Found_Count = Match_NOT_Found_Count + 1
                sp_entities_match_not_found.append(row.BaseName)
                worksheet_Results.write_string(ifs_count, 0, "IP")
                worksheet_Results.write_string(ifs_count, 1, "Entity Name")
                worksheet_Results.write_string(ifs_count, 2, row.BaseName)
                worksheet_Results.write_string(ifs_count, 3, "Phase 3")
                worksheet_Results.write_string(ifs_count, 4, "Yes")
                worksheet_Results.write_string(ifs_count, 5, url_full)
                worksheet_Results.write_string(ifs_count, 6, "No Match")
                worksheet_Results.write_string(ifs_count, 7, str(row.Modified))
                worksheet_Results.write_string(ifs_count, 8, "Open")
                ifs_count = ifs_count + 1

            # print row.BaseName, ",",row.Modified,",",row._DCDateModified,",",row.File_x0020_Type,",",row.ServerUrl
            # print row.Created,row.Modified,row._DCDateModified
            # print row.is_file,row.Title,
            # print "Nones: ",row.Date,row.Date_x0020_stamp,row.Dateof_x0020_mod
            # print row.BaseName,row._IsCurrentVersion,row._SourceUrl,row.Created_x0020_Date
            # print row.fields


            # worksheet.write_string(rows_length, 1, row.Entity_x0020_Type)

MDR_ifs_count = 1 # set to 1 as the 0th row as the headers in the excel sheet

Match_Found_Count_MDR_SHAREPOINT = 0
Match_Not_Found_Count_MDR_SHAREPOINT = 0
mdr_entities_match_not_found = []

for row_MRD in sp_list_MDR.rows:

    Match_Found_Flag = 0

    #if(MDR_ifs_count == 1):
        #print row_MRD.fields
        #print row_MRD.MDR_x0020_Scope


    for row in sp_list.rows:
        if (re.search(file_path, row.ServerUrl)):
            if (row.ServerUrl.count('/') == 9):
                if (re.match(r'.*(.docx)$', row.ServerUrl)):
                        if (row_MRD.IFS_x0020_Object_x0020_Name == row.BaseName):
                            Match_Found_Flag = 1

    if (Match_Found_Flag == 1):
          Match_Found_Count_MDR_SHAREPOINT = Match_Found_Count_MDR_SHAREPOINT + 1
          worksheet_Results_MDR_Sharepoint.write_string(MDR_ifs_count, 0, row_MRD.IFS_x0020_Object_x0020_Name)
          worksheet_Results_MDR_Sharepoint.write_string(MDR_ifs_count, 1, "Match")
          worksheet_Results_MDR_Sharepoint.write_string(MDR_ifs_count, 2, row_MRD.MDR_x0020_Scope)
          worksheet_Results_MDR_Sharepoint.write_string(MDR_ifs_count, 2, row_MRD.MDR_x0020_Project_x0020_Notes)
          MDR_ifs_count = MDR_ifs_count + 1
    else:
          Match_Not_Found_Count_MDR_SHAREPOINT = Match_Not_Found_Count_MDR_SHAREPOINT + 1
          mdr_entities_match_not_found.append(row_MRD.IFS_x0020_Object_x0020_Name)
          worksheet_Results_MDR_Sharepoint.write_string(MDR_ifs_count, 0, row_MRD.IFS_x0020_Object_x0020_Name)
          worksheet_Results_MDR_Sharepoint.write_string(MDR_ifs_count, 1, "No Match")
          worksheet_Results_MDR_Sharepoint.write_string(MDR_ifs_count, 2, row_MRD.MDR_x0020_Scope)
          worksheet_Results_MDR_Sharepoint.write_string(MDR_ifs_count, 2, row_MRD.MDR_x0020_Project_x0020_Notes)
          MDR_ifs_count = MDR_ifs_count + 1



workbook.close();

print "Matching program completed.\n"


print "Sharepoint IFS Document Count: ", sharepoint_ifs_count
print "MDR IFS Documents count: ",child_list_count


print "BT Panorama - Solution Design - IFS to Metadata IFS Master List documents [Matches Found]: ",Match_Found_Count
print "BT Panorama - Solution Design - IFS to Metadata IFS Master List documents [Matches Not Found]: ",Match_NOT_Found_Count


if (parent_list_count == Match_Found_Count):
    print "Success: All Sharepoint Visual Map Documents Found in Metadata Respository Master List"
else:
    print "Warning: Not all Sharepoint Documents Found in Metadata Respository Master List"
    for i in range(0,len(sp_entities_match_not_found),1):
        print "IFS Name: "+sp_entities_match_not_found[i]

print '\n'

print "Metadata IFS Master List documents to BT Panorama IFS documents [Matches Found] :",Match_Found_Count_MDR_SHAREPOINT
print "Metadata IFS Master List documents to BT Panorama IFS documents [Matches Not Found] :",Match_Not_Found_Count_MDR_SHAREPOINT

if (child_list_count == Match_Found_Count_MDR_SHAREPOINT):
    print "Success: All MDR documents found in Sharepoint list"
else:
    print "Warning: Not all MDR documents are found in Sharepoint list"
    for i in range(0,len(mdr_entities_match_not_found),1):
        print "IFS Name: "+mdr_entities_match_not_found[i]

print "\n"

end_time = datetime.datetime.now()
print "Start Time:", start_time
print "End Time:  ",end_time
print "Execution time:", end_time - start_time
