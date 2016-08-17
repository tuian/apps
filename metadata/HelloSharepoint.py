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

#print base64.b64encode("")
#print base64.b64decode("VENTIzMxNjA=")


#reload(sys)
#sys.setdefaultencoding('utf8')

#my Windows credentials
site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"
list_name = "Screen Master"
output_excel_file_name = "Screen_Master.xlsx"

#optionally include the domain name with the staff number like 'AUAUTD0001\L083646'

""""""
#option 1: Read from console input
# Read User Name (i.e. L123456)
username = raw_input("Enter your staff number (eg. L082345): ")
password = getpass() # get the password. Enter the password when the prompt comes up

"""
# Option 2: Encode the password
username ='L083646'
password = base64.b64decode("ZENTIzMxNjA=")
"""


"""
#option 3: Read from command line arguments
username = sys.argv[1]
password = sys.argv[2]
"""




# Excel sheet details: Workbook Name, Worksheet Name, Header Columns Needed
workbook = xlsxwriter.Workbook(output_excel_file_name)
worksheet = workbook.add_worksheet("Object Definition")
bold = workbook.add_format({'bold': 1});
worksheet.write('A1', 'Screen Name', bold);
worksheet.write('B1', 'Attribute Name', bold)


# an opener for the NTLM authentication
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, site_url, username, password)
auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

# create and install the sharepoint site opener
opener = urllib2.build_opener(auth_NTLM)
urllib2.install_opener(opener)

# create a SharePointSite object
site = SharePointSite(site_url, opener)
sp_list = site.lists[list_name]

#set row length to 1 (as the first row in the excel sheet has the header

rows_length = 1

for row in sp_list.rows:
    #print to console, comment the print statement if not needed
    #print row.fields
    print row.Title ,row.Entity_x0020_Type

    # Write to Excel Sheet
    # write_string(row,column, text)
    worksheet.write_string(rows_length, 0, row.Title)
    worksheet.write_string(rows_length, 1, row.Entity_x0020_Type)

    rows_length = rows_length + 1

# print results
print "\n"
print "---Results---"
print "Sharepoint site name: ",site_url
print "Sharepoint list name: ",list_name

# row lenght - 1 becuase of the header
print "No of rows processed: ",rows_length-1

print "Excelsheet [",output_excel_file_name,"] created successfully."

#close the excel sheet workbook
workbook.close();
