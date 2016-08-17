import re

"""
str = "<font face=Calibri size=2><div><strong>Hello</strong></div></font>"
pattern = re.compile(r'(<div>)|(</div>)|(<strong>)|(</strong>)|(<font face=Calibri size=.>)|(</font>)')
output_string = pattern.sub('', str)
print output_string
"""

str1 = '<font face=Calibri size=2><div><strong>Hello</strong></div></font>'
#pattern1 = re.compile(r'(<div>)|(</div>)|(<strong>)|(</strong>)|(<font face=Calibri size=.>)|(</font>)')
pattern1 = re.compile(r'(<div>)|(<strong>)')
output_string1 = pattern1.sub('', str1)
print output_string1