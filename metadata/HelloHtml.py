
import re,os,sys
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf8')


def getFilesList_Html(folder_path):

    print "----------------getFilesList()----------------------------"
    print "\t Base Folder = {} \n".format(folder_path)
    #print "folder path = {} ".format(folder_path)
    list = []

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in [f for f in filenames if f.endswith(".html")]:
           list.append(os.path.join(dirpath, filename))

    print "\t Total matching files [htmls] = {} \n".format(len(list))
    #print "---------------------------------------------------------"
    return list
def getFilesList_Javascript(folder_path):

    print "----------------getFilesList()----------------------------"
    print "\t Base Folder = {} \n".format(folder_path)
    #print "folder path = {} ".format(folder_path)
    list = []

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in [f for f in filenames if f.endswith(".js")]:
           list.append(os.path.join(dirpath, filename))

    print "\t Total matching files [js] = {} \n".format(len(list))
    #print "---------------------------------------------------------"
    return list

def getFunctionality(input_string):
    #print input_string

    input_string = input_string.replace('.html', "")
    input_string = input_string.replace("C:/Development/ui-ip-layout/webapp/app/pages/mvc-screens/ip","")
    #print input_string
    input_string = input_string.split("\\")
    #print input_string
    # #input_string = input_string.replace("\\", "-")
    #print input_string[1:-1]
    input_string = "-".join(input_string[1:-1])
    #print input_string.upper()

    return input_string.upper()
def getScreeName(input_string):
    #print input_string
    input_string = (input_string.split('\\')[-1]).replace(".html","")
    #print input_string
    return input_string
def getTagName(input_string):
    #print input_string

    input_string = re.sub("<.?title.*?>|<.?span.*?>|<.?label.*?>|<.?strong>","",input_string)
    #pattern2 = re.compile('<.?span.*?>|<.?label.*?>|<.?strong>')
    #print input_string
    return input_string
def getTagName_JS(input_string):
    #print input_string

    #input_string = re.sub("'name':","",input_string)
    input_string = input_string.replace("'name': ","")
    input_string = input_string.replace("'", "")
    #pattern2 = re.compile('<.?span.*?>|<.?label.*?>|<.?strong>')
    #print input_string
    return input_string
def getHTML_Tag(input_string):
    #print input_string
    tag = ""

    if(input_string.__contains__("span")):
        tag = "<span>"

    if (input_string.__contains__("label")):
        tag = "<label>"

    if (input_string.__contains__("title")):
        tag = "<title>"

    #print tag
    return tag


def setValue(filename,tag):

    object_dict = {}

    object_dict["Functionality"] = getFunctionality(filename)
    object_dict["Screen_Name"] = getScreeName(filename)
    object_dict["Field_Name"] =  getTagName(tag)
    object_dict["HTML_Tag"] = getHTML_Tag(tag)
    #print object_dict
    return object_dict

def setValue_JS(filename,tag):

    object_dict = {}

    object_dict["Functionality"] = getFunctionality(filename)
    object_dict["Screen_Name"] = getScreeName(filename)
    object_dict["Field_Name"] =  getTagName_JS(tag)
    object_dict["HTML_Tag"] = "Default" #getHTML_Tag(tag)
    #print object_dict
    return object_dict

def processHTML(filename):
    #print "processing HTML file = {} ".format(filename)
    list_of_objects = []

    file = open(filename, "r")
    #regex = re.compile(r'<label>.*</label>|<span>.*</span>',re.MULTILINE | re.IGNORECASE)
    regex = re.compile('<title.*?>.*</title>|<span.*?>.*</span>|<label.*?>.*</label>')


    for line in file:
        #print line
        matches = regex.findall(line)
        for tag in matches:
            #print "Tag is:",tag
            list_of_objects.append(setValue(filename,tag))


    return list_of_objects

def processJS(filename):
    #print "processing HTML file = {} ".format(filename)
    list_of_objects = []

    file = open(filename, "r")
    #regex = re.compile(r'<label>.*</label>|<span>.*</span>',re.MULTILINE | re.IGNORECASE)
    regex = re.compile("'name':.*'")


    for line in file:
        #print line
        matches = regex.findall(line)
        for tag in matches:
            #print "Tag is:",tag
            list_of_objects.append(setValue_JS(filename,tag))


    return list_of_objects

def cleanDataFrame(df):

    drop_by_columns = ["Functionality", "Field_Name"]

    #df = df[df["Field_Name"].str.strip()]
    df = df[~((df["Field_Name"] == "") | (df["Field_Name"] == " "))]
    df = df[~( ( df["Field_Name"].str.contains("{{") ) | ( df["Field_Name"].str.contains("<") ) )]

    #Renewal commission (High - Low)
    filename_regex = r'.*\(.*-.*\)$'
    df = df[~(df['Field_Name'].str.contains(filename_regex, regex=True))]

    df = df[df["Screen_Name"] <> "filter"]

    #drop duplicates by Functionliaty and Field Name
    df.drop_duplicates(subset=drop_by_columns, keep='first', inplace=True)

    return df

def processHTMLs(list_of_html_files):
    print "----------------processHTMLs()----------------------------".format(len(list_of_html_files))

    list = []

    html_folder_path_output = "C:\\MDR\\Data\HTML\\Output\\"
    output_filename = "Screen_Attributes.xlsx"
    sort_by_columns = ["Functionality","Field_Name"]
    for file in list_of_html_files:
        df = pd.DataFrame(processHTML(file))
        list.append(df)

    df_all = pd.concat(list)

    writer = pd.ExcelWriter(html_folder_path_output + output_filename)

    #df_all.sort_values(by=sort_by_columns, inplace=True, na_position='first', ascending=[True,True])

    df_all.to_excel(writer, sheet_name="Screen_Attributes", index=False,
                    columns=["Functionality", "Screen_Name", "HTML_Tag","Field_Name"])

    df_cleaned = cleanDataFrame(df_all)
    #df_cleaned.sort_values(by=sort_by_columns, inplace=True, na_position='first', ascending=[True, True])


    df_cleaned.to_excel(writer, sheet_name="Screen_Attributes_Cleaned", index=False,
                    columns=["Screen_Name","Functionality", "Field_Name","HTML_Tag"])

    writer.close()

    #print df_big.info()
    print "\t Total Screens = {} \n".format(len(list_of_html_files))
    print "\t Total Screen Fields Extracted = {}\n".format(len(df_all))
    print "\t Total Screen Fields After Cleaning = {}\n".format(len(df_cleaned))
    print "\t Refer output file generated | {}\n".format(html_folder_path_output + output_filename)
    #print "------------------------------------------------------------------"
def processJavascripts(list_of_js_files):
    print "----------------processHTMLs()----------------------------".format(len(list_of_js_files))

    list = []

    html_folder_path_output = "C:\\MDR\\Data\HTML\\Output\\"
    output_filename = "Screen_Attributes_js.xlsx"
    sort_by_columns = ["Functionality","Field_Name"]
    for file in list_of_js_files:
        df = pd.DataFrame(processJS(file))
        list.append(df)

    df_all = pd.concat(list)

    writer = pd.ExcelWriter(html_folder_path_output + output_filename)

    #df_all.sort_values(by=sort_by_columns, inplace=True, na_position='first', ascending=[True,True])

    df_all.to_excel(writer, sheet_name="Screen_Attributes", index=False,
                    columns=["Functionality", "Screen_Name", "HTML_Tag","Field_Name"])

    df_cleaned = cleanDataFrame(df_all)
    #df_cleaned.sort_values(by=sort_by_columns, inplace=True, na_position='first', ascending=[True, True])


    df_cleaned.to_excel(writer, sheet_name="Screen_Attributes_Cleaned", index=False,
                    columns=["Screen_Name","Functionality", "Field_Name","HTML_Tag"])

    writer.close()

    #print df_big.info()
    print "\t Total Screens = {} \n".format(len(list_of_js_files))
    print "\t Total Screen Fields Extracted = {}\n".format(len(df_all))
    print "\t Total Screen Fields After Cleaning = {}\n".format(len(df_cleaned))
    print "\t Refer output file generated | {}\n".format(html_folder_path_output + output_filename)
    #print "------------------------------------------------------------------"

if __name__ == '__main__':

    # list_of_files_html = getFilesList_Html('C:/Development/ui-ip-layout/webapp/app/pages/mvc-screens/ip')
    # processHTMLs(list_of_files_html)

    list_of_files_js = getFilesList_Javascript('C:/Development/ui-ip-layout/webapp/app/pages/mvc-screens/ip')
    processJavascripts(list_of_files_js)


    #getFunctionality("C:/Development/ui-ip-layout/webapp/app/pages/mvc-screens/ip\yourdetails\updateusername\updateusername.html")
    #getScreeName("C:/Development/ui-ip-layout/webapp/app/pages/mvc-screens/ip\yourdetails\yourdetails.html")
    #getTagName("<span>span</span><label>label</label>")
    #getHTML_Tag("<span>span</span><label>label</label>")