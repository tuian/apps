'''

\s = space
\S = Not Space
\d = digits
\D = Non Digits
\w = letter or number

* = 0 or more
+ = 1 ore more
? = 0 or 1
{5} = exact number of occurance
{1,60} = range (min and max)


. = Any character

re.split(r'',string) > list
re.finall(r'',string) > list

re.findall(r'[][]',inputsting)

pattern = re.compiple(r'| | |')
parttern.sub('with',input_string)
() is used for grouping
[a-f]
Flags re.I | re.M
re.I = ignore case
re.M = Multiline
'''
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


string = "<p>This is a test string</p>"

#pattern2 = re.compile(r'<.?p>')
pattern2 = re.compile(r'</?p>')
string = pattern2.sub('',string)
print "re.compile: ",string

string = "<p>This is a test string</p>"
print "string.replace: ", string.replace('<p>','')


string = "<p>This is a test string</p>"
pattern = re.compile(r'</?p>',re.I)

string = pattern.sub('',string)

print "pattern. sub . re.I : ", string
print  string

print re.split(r'(a)',"kdafjdkfdjafkdjfdkj")
print re.split(r'([a-c])',"kdafcjdkfdcjafkcdjfdkj")
print re.split(r'([a-c])',"kdafcjdkfdcjafkcdjfdkj")

print re.findall(r'[k][a-d]',"kdafcjdkfdcjafkcdjfdkj")
