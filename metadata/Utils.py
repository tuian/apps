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

"""
line = line.strip()
line = line.replace('"C:\Development\ui-ip-layout\webapp\\app\pages\mvc-screens\\', '')
line = line.replace('.html"', '')
line = re.sub(r'\(\d.*\d\):', "@", line)
line = re.sub(r'@\s*', "@", line)
"""



def processXSDAttribute(input_str):

	"""START"""

	# strip the '/' character if present in the begining
	if(input_str[-1] == '/'):
		input_str = input_str[:-1]

	#clean the string with unwanted space characters in the middle
	pattern = re.compile(r'\s+')
	input_str = re.sub(pattern, '', input_str)

	#pattern 1: '/val'

	if(re.match(r'.*(/val)$', input_str) ):
		input_str = input_str[:-4]

	# pattern 2: '/annot/ctx/id'

	else:
			if (re.match(r'.*(/annot/ctx/id)$', input_str)):
				input_str = input_str[:-13]

	output_str =  (input_str.split('/'))[-1]

	"""END"""
	return output_str

"""
print processXSDAttribute('rebal_det_req/data/action')
print processXSDAttribute('rebal_det_req/data/rebal_det/justif/val')
print processXSDAttribute('rebal_det_req/req/exec/action/generic_action')
print processXSDAttribute('helodfd/hello/val/')
print processXSDAttribute('rep/data/user_list/user/user_head_list/user_head/sec_user_id/annot/ ctx/id')
print processXSDAttribute('rep/data/user_list/user/user_head_list/user_head/ job_auth_level_id/ annot/ctx/id')

print processXSDAttribute('//rep/data/report/report_foot_list/')
"""
print processXSDAttribute('user:user_req\data\sec_user\annot\ctx\id')
