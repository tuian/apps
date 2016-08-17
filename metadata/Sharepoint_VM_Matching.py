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

""""Output Excel Sheet Details """
workbook = xlsxwriter.Workbook("Visual_Map_Comparison.xlsx")

worksheet_Source = workbook.add_worksheet("Sharepoint - VM Documents")
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

parent_list_count = len(sp_list.rows)

for row in sp_list.rows:
     if (bool(re.search(file_path, row.ServerUrl))):
         if(bool(re.search(file_path_excluded, row.ServerUrl))):
             visual_map_count_extended = visual_map_count_extended + 1
         else:
            visual_map_count = visual_map_count + 1
            #print row.BaseName
            #print row.BaseName, ",",row.Modified,",",row._DCDateModified,",",row.File_x0020_Type,",",row.ServerUrl
            #print row.Created,row.Modified,row._DCDateModified
            #print row.is_file,row.Title,
            #print "Nones: ",row.Date,row.Date_x0020_stamp,row.Dateof_x0020_mod
            #print row.BaseName,row._IsCurrentVersion,row._SourceUrl,row.Created_x0020_Date
            #print row.fields

            worksheet_Source.write_string(visual_map_count, 0, row.BaseName)
            # worksheet.write_string(rows_length, 1, row.Entity_x0020_Type)

     parent_list_count = visual_map_count
#print visual_map_count


""" """
#workbook_MDR = xlsxwriter.Workbook("Visual_Map_MDR_List.xlsx")
#worksheet_MDR    = workbook_MDR.add_worksheet("MDR - Visual Map Documents")
#bold = workbook.add_format({'bold': 1});

worksheet_MDR    = workbook.add_worksheet("MDR - Visual Map Documents")
worksheet_MDR.write('A1', 'Visual Map Document Name', bold);



site_url_MDR = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"
list_name_MDR = "Visual Map Master"

passman2 = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman2.add_password(None, site_url_MDR, username, password)
auth_NTLM2 = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman2)
opener2 = urllib2.build_opener(auth_NTLM2)
urllib2.install_opener(opener2)

site_MDR = SharePointSite(site_url_MDR, opener2)
sp_list_MDR = site_MDR.lists[list_name_MDR]


visual_map_count = 0

child_list_count = len(sp_list_MDR.rows)

for row in sp_list_MDR.rows:
    visual_map_count = visual_map_count + 1
    #print row.Title
    worksheet_MDR.write_string(visual_map_count, 0, row.Title)

#print visual_map_count

""" Comparison Results - Sharepoint to Metadata"""
worksheet_Results    = workbook.add_worksheet("Comparison Results - Sharepoint")
worksheet_Results.write('A1', 'Visual Map Document Name', bold);
worksheet_Results.write('B1', 'Flag', bold);
worksheet_Results.write('C1', 'URL', bold);

visual_map_count = 0

# Take items from the parent list i.e. List of Visual Maps from the sharepoint list

Match_Found_Count = 0
Match_NOT_Found_Count = 0

for row in sp_list.rows:
    if (bool(re.search(file_path, row.ServerUrl))):
        if (bool(re.search(file_path_excluded, row.ServerUrl))):
            visual_map_count_extended = visual_map_count_extended + 1
        else:
            visual_map_count = visual_map_count + 1

            #print "Matching IFS Document:",row.BaseName


            Match_Found_Flag = 0;

            # For each item in parent list, loop through the child list (i.e. MDR Visual Maps List ) and find the match
            #child_rows_length = len(sp_list_MDR.rows)
            #print "Child rows length:",child_rows_length

            for row_MRD in sp_list_MDR.rows:
               #print "Child Document Names",row_MRD.Title
               # Parent == Child
                if(row.BaseName == row_MRD.Title):
                    Match_Found_Flag = 1;



            if(Match_Found_Flag == 1):
               Match_Found_Count = Match_Found_Count + 1
               worksheet_Results.write_string(visual_map_count, 0, row.BaseName)
               worksheet_Results.write_string(visual_map_count, 1, "Match")
            else:
                Match_NOT_Found_Count = Match_NOT_Found_Count + 1
                worksheet_Results.write_string(visual_map_count, 0, row.BaseName)
                worksheet_Results.write_string(visual_map_count, 1, "No Match")
                worksheet_Results.write_string(visual_map_count, 2, row.EncodedAbsUrl)
                #worksheet_Results.write_string(visual_map_count, 3, "http://sharepoint.btfin.com"+row.ServerUrl)
                #worksheet_Results.write_string(visual_map_count, 4, row.ServerUrl)
                #worksheet_Results.write_string(visual_map_count, 5, row._SourceUrl)
                #worksheet_Results.write_string(visual_map_count, 6, row.TemplateUrl)

            # print row.BaseName, ",",row.Modified,",",row._DCDateModified,",",row.File_x0020_Type,",",row.ServerUrl
            # print row.Created,row.Modified,row._DCDateModified
            # print row.is_file,row.Title,
            # print "Nones: ",row.Date,row.Date_x0020_stamp,row.Dateof_x0020_mod
            # print row.BaseName,row._IsCurrentVersion,row._SourceUrl,row.Created_x0020_Date
            # print row.fields


            # worksheet.write_string(rows_length, 1, row.Entity_x0020_Type)


""" Comparison Results - Metadata to Sharepoint"""
worksheet_Results_MDR    = workbook.add_worksheet("Comparison Results - MDR")
worksheet_Results_MDR.write('A1', 'Visual Map Document Name', bold);
worksheet_Results_MDR.write('B1', 'Flag', bold);
worksheet_Results_MDR.write('C1', 'URL', bold);
worksheet_Results_MDR.write('D1', 'Visual_Map_Release', bold);
worksheet_Results_MDR.write('E1', 'MDR_Project_Notes', bold);

visual_map_count_mdr = 1

# Take items from the parent list i.e. List of Visual Maps from the sharepoint list

Match_Found_Count_mdr = 0
Match_NOT_Found_Count_mdr = 0

for row_MRD in sp_list_MDR.rows:

    if ('A' == 'A'):

                #print "Matching IFS Document:",row.BaseName


            Match_Found_Flag = 0;

            # For each item in parent list, loop through the child list (i.e. MDR Visual Maps List ) and find the match
            #child_rows_length = len(sp_list_MDR.rows)
            #print "Child rows length:",child_rows_length

            for row_Sharepoint in sp_list.rows:
               #print "Child Document Names",row_MRD.Title
               # Parent == Child
                if(row_Sharepoint.BaseName == row_MRD.Title):
                    Match_Found_Flag = 1;



            if(Match_Found_Flag == 1):
               Match_Found_Count_mdr = Match_Found_Count_mdr + 1
               worksheet_Results_MDR.write_string(visual_map_count_mdr, 0, row_MRD.Title)
               worksheet_Results_MDR.write_string(visual_map_count_mdr, 1, "Match")
               worksheet_Results_MDR.write_string(visual_map_count_mdr, 2, row_MRD.Visual_x0020_Map_x0020_Release_x)
               worksheet_Results_MDR.write_string(visual_map_count_mdr, 3, row_MRD.MDR_x0020_Release_x0020_Period)
               visual_map_count_mdr = visual_map_count_mdr + 1
            else:
                Match_NOT_Found_Count_mdr = Match_NOT_Found_Count_mdr + 1
                worksheet_Results_MDR.write_string(visual_map_count_mdr, 0, row_MRD.Title)
                worksheet_Results_MDR.write_string(visual_map_count_mdr, 1, "No Match")
                worksheet_Results_MDR.write_string(visual_map_count_mdr, 2, row_MRD.Visual_x0020_Map_x0020_Release_x)
                worksheet_Results_MDR.write_string(visual_map_count_mdr, 3, row_MRD.MDR_x0020_Release_x0020_Period)
                worksheet_Results_MDR.write_string(visual_map_count_mdr, 4, row_MRD.MDR_Project_Notes)

                visual_map_count_mdr = visual_map_count_mdr + 1


            # print row.BaseName, ",",row.Modified,",",row._DCDateModified,",",row.File_x0020_Type,",",row.ServerUrl
            # print row.Created,row.Modified,row._DCDateModified
            # print row.is_file,row.Title,
            # print "Nones: ",row.Date,row.Date_x0020_stamp,row.Dateof_x0020_mod
            # print row.BaseName,row._IsCurrentVersion,row._SourceUrl,row.Created_x0020_Date
            # print row.fields


            # worksheet.write_string(rows_length, 1, row.Entity_x0020_Type)

workbook.close();

print "Matching program completed successfully."

print "\n"

if (parent_list_count == Match_Found_Count):
    print "Success: All Sharepoint Visual Map Documents Found in Metadata Respository Master List"
else:
    print "Warning: Not all Sharepoint Documents Found in Metadata Respository Master List"

if (child_list_count == Match_Found_Count_mdr):
    print "Success: All Metadata Visual Map Documents Found in Sharepoint Respository Master List"
else:
    print "Warning: Not all Metadata Documents Found in Sharepoint Respository Master List"

print "\n"

print "Sharepoint Visual Map Documents count:",parent_list_count
print "Metadata Repository Visual Map Documents count:",child_list_count

print "Sharepoint matches found in MDR:",Match_Found_Count
print "Sharepoint matches not found in MDR:",Match_NOT_Found_Count

print "Metadata matches found in Sharepoint:",Match_Found_Count_mdr
print "Metadata matches not found in Sharepoint:",Match_NOT_Found_Count_mdr

print "\n"

end_time = datetime.datetime.now()
print "Start Time:", start_time
print "End Time:  ",end_time
print "Execution time:", end_time - start_time

