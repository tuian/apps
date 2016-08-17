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


#reload(sys)
#sys.setdefaultencoding('utf8')

""""Sharepoint Details """

list_name_screen_master = "Screen Master"
list_name_screen_fields = "Screen Fields"

""""Output Excel Sheet Details """
workbook = xlsxwriter.Workbook("GapReport.xlsx")

worksheet_Screen_Master = workbook.add_worksheet("Screen Master")
worksheet_Screen_Fields = workbook.add_worksheet("Screen Fields")
worksheet_Screen_Master_vs_Fields = workbook.add_worksheet("Screen Master vs Fields")
worksheet_Screen_Fields_vs_Master = workbook.add_worksheet("Screen Fields vs Master")
worksheet_Screen_Master_vs_Mapping_UX_VM = workbook.add_worksheet("Screen Master vs M_Screen_VM")

bold = workbook.add_format({'bold': 1});

worksheet_Screen_Master.write('A1', 'Screen Entity Name', bold);
worksheet_Screen_Master.write('B1', 'MDR Phase', bold);
worksheet_Screen_Master.write('C1', 'Harvest Status', bold);


worksheet_Screen_Fields.write('A1', 'Screen Entity Name', bold);
worksheet_Screen_Fields.write('B1', 'Screen Attribute', bold);
worksheet_Screen_Fields.write('C1', 'MDR Phase', bold);
#worksheet_Source.write('B1', 'Attribute Name', bold)

worksheet_Screen_Master_vs_Fields.write('A1', 'Screen Entity Name', bold);
worksheet_Screen_Master_vs_Fields.write('B1', 'Match Results', bold);
worksheet_Screen_Master_vs_Fields.write('C1', 'MDR Phase', bold);
worksheet_Screen_Master_vs_Fields.write('D1', 'Harvest Status', bold);

worksheet_Screen_Fields_vs_Master.write('A1', 'Screen Entity Name', bold);
worksheet_Screen_Fields_vs_Master.write('B1', 'Screen Attribute', bold);
worksheet_Screen_Fields_vs_Master.write('C1', 'MDR Phase', bold);

worksheet_Screen_Master_vs_Mapping_UX_VM.write('A1', 'Screen Entity Name', bold);
worksheet_Screen_Master_vs_Mapping_UX_VM.write('B1', 'Screen Attribute', bold);
worksheet_Screen_Master_vs_Mapping_UX_VM.write('C1', 'MDR Phase', bold);


worksheet_row_count_screen_master = 0
worksheet_row_count_screen_fields = 0
worksheet_row_count_screen_master_vs_fields = 0
H_Status = ""
list_screen_master = []
list_screen_fields = []

for row_screen_master in mdr_util.sharepointListRowsByListName(list_name_screen_master):
    worksheet_row_count_screen_master = worksheet_row_count_screen_master + 1

    if(row_screen_master.Harvest_Status == None): H_Status = "None"
    else: H_Status = row_screen_master.Harvest_Status

    #print row.fields
    if(str(row_screen_master.MDR_x0020_Scope == 'True')):
        #print "Scope Yes"
        pass

    list_screen_master.append(row_screen_master.Entity_x0020_Name)
    worksheet_Screen_Master.write_string(worksheet_row_count_screen_master, 0, row_screen_master.Entity_x0020_Name)
    worksheet_Screen_Master.write_string(worksheet_row_count_screen_master, 1, row_screen_master.MDR_x0020_Release)
    worksheet_Screen_Master.write_string(worksheet_row_count_screen_master, 2, H_Status)
    worksheet_Screen_Master.write_string(worksheet_row_count_screen_master, 3, str(row_screen_master.MDR_x0020_Scope))


for row_screen_field in mdr_util.sharepointListRowsByListName(list_name_screen_fields):
    worksheet_row_count_screen_fields = worksheet_row_count_screen_fields + 1

    #print row.fields
    list_screen_fields.append(row_screen_field.Entity_Name_D)
    worksheet_Screen_Fields.write_string(worksheet_row_count_screen_fields, 0, row_screen_field.Entity_Name_D)
    worksheet_Screen_Fields.write_string(worksheet_row_count_screen_fields, 1, row_screen_field.Attribute_Name)
    worksheet_Screen_Fields.write_string(worksheet_row_count_screen_fields, 2, row_screen_field.MDR_Phase)

'''
#for row_screen_master_vs_fields in mdr_util.sharepointListRowsByListName(list_name_screen_master):
for row_screen_master_vs_field in mdr_util.UniqueListItems(list_screen_master):
    worksheet_row_count_screen_master_vs_fields = worksheet_row_count_screen_master_vs_fields + 1

    if (row_screen_master_vs_field in mdr_util.UniqueListItems(list_screen_fields)):
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 0, row_screen_master_vs_field)
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 1, "Match Found")
    else:
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 0,row_screen_master_vs_field)
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 1, "Match Not Found")
'''

for row_screen_master_vs_fields in mdr_util.sharepointListRowsByListName(list_name_screen_master):
    worksheet_row_count_screen_master_vs_fields = worksheet_row_count_screen_master_vs_fields + 1

    if (row_screen_master_vs_fields.Harvest_Status == None):
        H_Status = "None"
    else:
        H_Status = row_screen_master_vs_fields.Harvest_Status

    if (row_screen_master_vs_fields.Entity_x0020_Name in mdr_util.UniqueListItems(list_screen_fields)):
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 0, row_screen_master_vs_fields.Entity_x0020_Name)
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 1, "Match Found")
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 2, row_screen_master_vs_fields.MDR_x0020_Release)
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 3, H_Status)
    else:
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 0,row_screen_master_vs_fields.Entity_x0020_Name)
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 1, "Match Not Found")
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 2,row_screen_master_vs_fields.MDR_x0020_Release)
        worksheet_Screen_Master_vs_Fields.write_string(worksheet_row_count_screen_master_vs_fields, 3, H_Status)

worksheet_row_count_screen_fields_vs_master = 0

for row_screen_fields_vs_master in mdr_util.UniqueListItems(list_screen_fields):
    worksheet_row_count_screen_fields_vs_master = worksheet_row_count_screen_fields_vs_master + 1

    if (row_screen_fields_vs_master in mdr_util.UniqueListItems(list_screen_master)):
        worksheet_Screen_Fields_vs_Master.write_string(worksheet_row_count_screen_fields_vs_master, 0, row_screen_fields_vs_master)
        worksheet_Screen_Fields_vs_Master.write_string(worksheet_row_count_screen_fields_vs_master, 1, "Match Found")
    else:
        worksheet_Screen_Fields_vs_Master.write_string(worksheet_row_count_screen_fields_vs_master, 0,row_screen_fields_vs_master)
        worksheet_Screen_Fields_vs_Master.write_string(worksheet_row_count_screen_fields_vs_master, 1, "Match Not Found")

''' SCREEN MASTER vs Mapping_Screen_VisualMap '''
worksheet_row_count = 0
#list_name_screen_master
#Mapping_Screen_VisualMap

list_mapping_screen_visualmap = mdr_util.UniqueListItemsByListName_AttributeName("Mapping_Screen_VisualMap","Source_Entity_Name_D")

for row_screen_master in mdr_util.sharepointListRowsByListName(list_name_screen_master):
    worksheet_row_count = worksheet_row_count + 1

    if (row_screen_master.Harvest_Status == None):
        H_Status = "None"
    else:
        H_Status = row_screen_master.Harvest_Status

    if (row_screen_master.Entity_x0020_Name in list_mapping_screen_visualmap):
        worksheet_Screen_Master_vs_Mapping_UX_VM.write_string(worksheet_row_count, 0, row_screen_master.Entity_x0020_Name)
        worksheet_Screen_Master_vs_Mapping_UX_VM.write_string(worksheet_row_count, 1, "Match Found")
        worksheet_Screen_Master_vs_Mapping_UX_VM.write_string(worksheet_row_count, 2, row_screen_master.MDR_x0020_Release)
        worksheet_Screen_Master_vs_Mapping_UX_VM.write_string(worksheet_row_count, 3, H_Status)
    else:
        worksheet_Screen_Master_vs_Mapping_UX_VM.write_string(worksheet_row_count, 0,row_screen_master.Entity_x0020_Name)
        worksheet_Screen_Master_vs_Mapping_UX_VM.write_string(worksheet_row_count, 1, "Match Not Found")
        worksheet_Screen_Master_vs_Mapping_UX_VM.write_string(worksheet_row_count, 2,row_screen_master.MDR_x0020_Release)
        worksheet_Screen_Master_vs_Mapping_UX_VM.write_string(worksheet_row_count, 3, H_Status)


""" """

workbook.close();
print "Unique Items: Screen Master ", len(mdr_util.UniqueListItems(list_screen_master))
print "Unique Items: Screen Fields ", len(mdr_util.UniqueListItems(list_screen_fields))

print "Matching program completed successfully."

print "\n"


print "Sharepoint Screen Master count:",worksheet_row_count_screen_master," array length ",list_screen_master.__len__()
print "Sharepoint Screen Fields count:",worksheet_row_count_screen_fields," array length",list_screen_fields.__len__()

end_time = datetime.datetime.now()
print "Start Time:", start_time
print "End Time:  ",end_time
print "Execution time:", end_time - start_time
