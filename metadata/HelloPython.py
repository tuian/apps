""" 

Refer the ReadMe word document to set up the Python environment with docx and xlsxwriter modules

"""
from docx import Document
import os
import xlsxwriter 
import sys  
import re

reload(sys)  
sys.setdefaultencoding('utf8')



file = open("sourcefile.txt","r")
lines = file.readlines()
file.close()

countTotalLines = 0
substring_label ="<label>"
substring_span ="<span data-name="
workbook = xlsxwriter.Workbook("Screen_Attributes.xlsx")
worksheet = workbook.add_worksheet("Screen_Attributes")

bold = workbook.add_format({'bold': 1});

#worksheet.write('A1', 'Screen Name', bold);
#worksheet.write('B1', 'Attribute Name', bold)

for line in lines:
	line = line.strip()
	line = line.replace('"C:\Development\ui-ip-layout\webapp\\app\pages\mvc-screens\\','')
	line = line.replace('.html"','')
	line = re.sub(r'\(\d.*\d\):', "@", line)
	line = re.sub(r'@\s*', "@", line)
	#line = line.replace('<label>','')
	#line = line.replace('</label>','')
	#line_array = line.split(':')
	#print line_array[1]
	if substring_label in line:
		line = line.replace(substring_label,'')
		line = line.replace("</label>",'')
		#worksheet.write_string(countTotalLines ,0 , line_array[1])
		#worksheet.write_string(countTotalLines ,1 , line_array[2])
		worksheet.write_string(countTotalLines ,2 , line)
		worksheet.write_string(countTotalLines ,0 , "Label")
		worksheet.write_string(countTotalLines ,1 , "Label")
		#worksheet.write_string(countTotalLines ,3 , line_array[3])
		#worksheet.write_string(countTotalLines ,4 , line_array[4])
		#worksheet.write_string(countTotalLines ,5 , line_array[5])
 	else:
 	 if substring_span in line:
 	 	line = line.replace(substring_span,'')
 	 	line = line.replace("</span>",'')
		#worksheet.write_string(countTotalLines ,0 , line_array[1])
		#worksheet.write_string(countTotalLines ,1 , line_array[2])
		worksheet.write_string(countTotalLines ,2 , line)
		worksheet.write_string(countTotalLines ,0 , "Span")
		worksheet.write_string(countTotalLines ,1 , "Span")
		#worksheet.write_string(countTotalLines ,3 , line_array[3])
		#worksheet.write_string(countTotalLines ,4 , line_array[4])
		#worksheet.write_string(countTotalLines ,5 , line_array[5])
 
	countTotalLines = 	countTotalLines + 1

workbook.close();
