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

#username ='AUAUTD0001\L083646'
username ='L083646'
#username = sys.argv[1]

#password = sys.argv[2]
password = base64.b64decode("VENTIzMxNjA=")
#password = getpass() # get the password. Enter the password when the prompt comes up

list_name = "Screen Master"
rows_length = 1

workbook = xlsxwriter.Workbook("Screen_Master.xlsx")
worksheet = workbook.add_worksheet("Object Definition")
bold = workbook.add_format({'bold': 1});
worksheet.write('A1', 'Screen Name', bold);
worksheet.write('B1', 'Attribute Name', bold)

bold = workbook.add_format({'bold': 1});


# an opener for the NTLM authentication
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, site_url, username, password)
auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

# create and install the opener
opener = urllib2.build_opener(auth_NTLM)
urllib2.install_opener(opener)

# create a SharePointSite object
site = SharePointSite(site_url, opener)
sp_list = site.lists[list_name]

#print sp_list.id, sp_list.meta['Title']

for row in sp_list.rows:

 #   print row.id, row.Title , row.Created,row.Author['name'],row.Entity_x0020_Type,row.L1
    #if (row.id==1):
        #print row.fields
  #  print row.Title ,row.Entity_x0020_Type , row._x004c_1 ,row._x004c_2 ,row._x004c_3
    worksheet.write_string(rows_length, 0, row.Title)
    worksheet.write_string(rows_length, 1, row.Entity_x0020_Type)

    rows_length = rows_length + 1

    #for row in sp_list.rows:
     #print "Hello"

print rows_length-1
workbook.close();



#for sp_list in site.lists:
#    print sp_list.id, sp_list.meta['Title']
# if current_project in row.Filename:
# basecase_rev = row.Rev

