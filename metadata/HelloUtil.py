"""
About the Script:

"""
from mdr_util import *
import xlsxwriter

site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"
list_name = "XSD Fields"
username = 'L083646'
password =  'TCS#3160'

#displayRowFields(site_url,'Visual Map',username,password)

"""
 createFolder('C:\TEST\\', 'Ragha', 'True')
"""


rows_IFS_Fields_Objects = sharepointListRows(site_url,'IFS Fields',username,password)
rows_XSD_Fields_Objects = sharepointListRows(site_url,'XSD Fields',username,password)

# Excel sheet details: Workbook Name, Worksheet Name, Header Columns Needed
output_excel_file_name_objects = 'Objects.xlsx'
workbook_Objects = xlsxwriter.Workbook(output_excel_file_name_objects)
worksheet_Objects = workbook_Objects.add_worksheet("Object Definition")

headerElements_Objects = {
    'A1':'System Name',
    'B1':'Instance Name',
    'C1':'Entity Name',
    'D1':'Attribute Name',
    'E1':'Owner',
    'F1':'Parent',
    'G1':'Type',
    'H1':'Description',
    'I1':'URL',
    'J1':'XPATH',
    'K1':'MDR Phase'
}

setHeaderRow(workbook_Objects,worksheet_Objects,headerElements_Objects)
insertRows_Objects(worksheet_Objects,1, rows_IFS_Fields_Objects)
insertRows_Objects(worksheet_Objects,len(rows_IFS_Fields_Objects)+1, rows_XSD_Fields_Objects)

workbook_Mappings = xlsxwriter.Workbook('Mappings.xlsx')

#two different files as output
#worksheet_Mappings = workbook_Mappings.add_worksheet("Mapping Definition")

#one same file as output
worksheet_Mappings = workbook_Objects.add_worksheet("Mapping Definition")

headerElements_Mappings = {
    'A1':'Source System Name',
    'B1':'Source Instance Name',
    'C1':'Source Entity Name',
    'D1':'Source Attribute Name',
    'E1':'Target System Name',
    'F1':'Target Instance Name',
    'G1':'Target Entity Name',
    'H1':'Target Attribute Name',
    'I1':'Attribute Description',
    'J1':'Business Rule(in Business Language)',
    'K1':'Transformation / Mapping rule(in Technical Pseudocode)',
    'L1':'Comments',
    'M1':'Mapping Name',
    'N1':'Action',
    'O1':'Last_Update_Date',
    'P1':'Modified_By',
    'Q1':'MDR Phase'
}

rows_IFS_XSD_Mappings = sharepointListRows(site_url,'Mapping_IFS_XSD',username,password)
#rows_IFS_XSD_Mappings = sharepointListRows(site_url,'Mapping_IFS_XSD',username,password)

setHeaderRow(workbook_Mappings,worksheet_Mappings,headerElements_Mappings)

insertRows_Mappings(worksheet_Mappings,1, rows_IFS_XSD_Mappings)
#insertRows_Mappings(worksheet_Mappings,1, rows_IFS_XSD_Mappings)

workbook_Objects.close()
workbook_Mappings.close()

