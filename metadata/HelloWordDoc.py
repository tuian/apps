import urllib2
from sharepoint import SharePointSite
from ntlm import HTTPNtlmAuthHandler
from getpass import getpass
import xlsxwriter
import sys
import os
import base64


os.system('cls')  # for Windows

print "\n \n \t \t \t ##### Metadata Repository ##### \n \n"

#reload(sys)
#sys.setdefaultencoding('utf8')

output_excel_file_name = "Screen_Master.xlsx"
# Excel sheet details: Workbook Name, Worksheet Name, Header Columns Needed
workbook = xlsxwriter.Workbook(output_excel_file_name)
worksheet = workbook.add_worksheet("Object Definition")
bold = workbook.add_format({'bold': 1});
worksheet.write('A1', 'Screen Name', bold);
worksheet.write('B1', 'Attribute Name', bold)


arr = ['Hello','World']

#set row length to 1 (as the first row in the excel sheet has the header

rows_length = 1

for row in arr:
    #print to console, comment the print statement if not needed
    print row

    # Write to Excel Sheet
    # write_string(row,column, text)
    worksheet.write_string(rows_length, 0, row)


    rows_length = rows_length + 1

# print results
print "\n"
print "---Results---"

# row lenght - 1 becuase of the header
print "No of rows processed: ",rows_length-1

print "Excelsheet [",output_excel_file_name,"] created successfully."


#close the excel sheet workbook
workbook.close();
