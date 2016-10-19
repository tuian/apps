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

str1 = '<span class="columns-7"><strong>First payment due:</strong></span>'
#pattern1 = re.compile(r'(<div>)|(</div>)|(<strong>)|(</strong>)|(<font face=Calibri size=.>)|(</font>)')
#pattern1 = re.compile(r'<font.*|(<.?font>)|(<.?div>)|(<.?strong>)')
#pattern1 = re.compile('<span.*?>.*</span>|</.*>|<strong.*?>')
pattern1 = re.compile('<span.*?>.*</span>|<label.*?>.*</label>')
pattern2 = re.compile('<.?span.*?>|<.?label.*?>|<.?strong>')
matches = pattern1.findall(str1)
for tag in matches:
    print "Tag is:",tag
    output_string1 = pattern2.sub('', tag)
    print output_string1

str2 = "Renewal mission (High - Low)"
print "String 2 = ",str2

pattern2 = re.compile('.*\(.*-.*\)$')

matches = pattern2.findall(str2)
print "Matches",matches



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


def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c
    print out
    return out
#remove_html_markup("<p>This is a test string</p><stron>djfdk</strong>")