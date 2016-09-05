#encoding=utf-8
import re
from mdr_util import *
"""
site_url = "http://sharepoint.btfin.com/sites/trans/tech/architecture"
list_name = "Solution Design"

"""
site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"

#list_name = "Screen Master"
#list_name = "Screen Fields"

#list_name = "Visual Map Master"
#list_name = "Visual Map Fields"

list_name = "IFS Master"
#list_name = "IFS Fields"

#list_name = "XSD Master"
#list_name = "XSD Fields"

#list_name = "Mapping_Screen_VisualMap"
#list_name = "Mapping_VisualMap_IFS"
#list_name = "Mapping_IFS_XSD"



#screen master
list_column_name = "Entity_x0020_Name"

username = 'L083646'
password =  'TCS#2305'


displayRowFields(site_url,list_name,username,password)


'''
#print "Unique Items: ",len(UniqueListItemsByListName_AttributeName("Mapping_Screen_VisualMap","Source_Entity_Name_D"))

#for item in UniqueListItemsByListName_AttributeName(list_name,list_column_name): print "Entity Names: ", item


#displayLineage('Esimated Unrealised CGT Page','asset id')
#displayLineage('Tracking-ROAs UX','Account name')
#displayLineage('Tracking-ROAs UX','ROA Status')
#displayLineage('Adviser Dashboard','Total FUA')

#displayLineageByScreenEntityName('Tracking-ROAs UX')

#for item in getAttributesbyEntity(list_name,entity_name="Blue Tray"): print "Attribute Name: ", item


#cleanHTMLTags('<font face=Calibri size=2 style=\"background-color:#FDE9D9\">Direct')
# a = "This is Order’s page"
# print a

#cleanHTMLTags(a)

string = "acc$acc_bal"

print "Input String: ", string

#pattern = re.compile(r'$')
pattern = re.compile(r'\d\$,')

if pattern.findall(string):
    print('Found')
else:
    print('Not found')


if('$' in string):
    print "Output String: ", string.split("$")
    print "Output String type: ", type(string.split("$"))
    list_of_values = string.split("$")
    print "list_of_values: ",list_of_values
    print "Output String 0: ", string.split("$")[0], list_of_values[0]
    print "Output String 1: ", string.split("$")[1], list_of_values[1]
else:
    print "Output String: ", string
'''